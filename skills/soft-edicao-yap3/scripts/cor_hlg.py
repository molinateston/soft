"""Cor HLG dos gráficos da YAP3 (extraído de nativo_branco.py, mesma matemática; só cor, composição e prévia).

sRGB do gráfico -> HLG BT.2020 10 bits faixa limitada (BT.2408, branco do gráfico = GRAF_BRANCO cd/m2, padrão 1000,
o mesmo branco da letra). compor() mistura o gráfico na câmera só onde alfa > 0; fora disso a câmera passa intacta.
preview_de_buf() é SÓ para prévia/mosaico (nunca entra na entrega).
"""
import os
import numpy as np

W, H = 1080, 1920
YS, CS = W * H, (W // 2) * (H // 2)
FS10 = (YS + 2 * CS) * 2
A_, B_, C_ = 0.17883277, 1 - 4 * 0.17883277, 0.5 - 0.17883277 * np.log(4 * 0.17883277)
M709_2020 = np.array([[0.6274, 0.3293, 0.0433], [0.0691, 0.9195, 0.0114], [0.0164, 0.0880, 0.8956]])
M2020_709 = np.linalg.inv(M709_2020)
KR, KB = 0.2627, 0.0593; KG = 1 - KR - KB
LW, SDR_BRANCO, GAMA = 1000.0, 203.0, 1.2
# Correção do dono 16/10 (letra cinza/gelo no HDR): branco do gráfico = pico HLG (1000 cd/m2, sinal 1,0, Y 940).
# Cores do gráfico sobem na mesma proporção em luz linear (tom preservado). SDR_BRANCO fica só na prévia.
GRAF_BRANCO = float(os.environ.get('GRAF_BRANCO', '1000'))


def hlg_oetf(e):
    e = np.maximum(e, 0)
    return np.where(e <= 1 / 12, np.sqrt(3 * e), A_ * np.log(np.maximum(12 * e - B_, 1e-12)) + C_)


def hlg_inv_oetf(v):
    v = np.clip(v, 0, 1)
    return np.where(v <= 0.5, v * v / 3, (np.exp((v - C_) / A_) + B_) / 12)


def srgb_para_hlg_ycc(c):
    """c: (...,3) cor de gráfico sRGB/BT.709 em [0,1] -> (Y,Cb,Cr) em códigos 10 bits faixa limitada BT.2020 HLG.
    BT.2408: SDR exibido em BT.1886 (gama 2,4) com branco = 203 cd/m2; 709->2020 em luz linear; OOTF inversa HLG (Lw 1000)."""
    lin = np.power(np.clip(c, 0, 1), 2.4) * (GRAF_BRANCO / LW)          # luz de exibição normalizada a 1000 cd/m2
    fd = lin @ M709_2020.T
    yd = np.maximum(fd @ np.array([KR, KG, KB]), 1e-12)[..., None]
    es = fd * np.power(yd, (1 - GAMA) / GAMA)                          # luz de cena (OOTF inversa)
    rgb = hlg_oetf(es)
    y = rgb @ np.array([KR, KG, KB]); cb = (rgb[..., 2] - y) / 1.8814; cr = (rgb[..., 0] - y) / 1.4746
    return np.stack([64 + 876 * y, 512 + 896 * cb, 512 + 896 * cr], -1)


def hlg_ycc_para_preview(Y, Cb, Cr):
    """SÓ PARA VISUALIZAÇÃO das comparações (não entra na entrega): inverso exato do mapeamento dos gráficos.
    HLG -> exibição Lw 1000 -> /203 -> 2020->709 -> recorte -> BT.1886^-1. Aplicado igual aos dois lados."""
    y = (Y.astype(np.float64) - 64) / 876; cb = (Cb.astype(np.float64) - 512) / 896; cr = (Cr.astype(np.float64) - 512) / 896
    r = y + 1.4746 * cr; b = y + 1.8814 * cb; g = (y - KR * r - KB * b) / KG
    es = hlg_inv_oetf(np.stack([r, g, b], -1))
    ys = np.maximum(es @ np.array([KR, KG, KB]), 0)[..., None]
    fd = es * np.power(np.maximum(ys, 1e-12), GAMA - 1) * (LW / SDR_BRANCO)
    s = np.clip(fd @ M2020_709.T, 0, 1)
    return (np.power(s, 1 / 2.4) * 255 + 0.5).astype(np.uint8)


def yuv_planos(buf):
    a = np.frombuffer(buf, '<u2')
    return a[:YS].reshape(H, W), a[YS:YS + CS].reshape(H // 2, W // 2), a[YS + CS:].reshape(H // 2, W // 2)


def up_croma(c):
    return np.repeat(np.repeat(c, 2, 0), 2, 1)


def preview_de_buf(buf):
    Y, U, V = yuv_planos(buf)
    return hlg_ycc_para_preview(Y, up_croma(U), up_croma(V))


def compor(cam, a, bp):
    """a: alfa (H,W); bp: cor pré-multiplicada sRGB 0-255 (render sobre preto). Retorna buf yuv420p10le.
    Só a caixa que contém alfa > 0 (alinhada a 2 px) é recalculada, em float32; o resto é a câmera intacta."""
    Y, U, V = yuv_planos(cam)
    ys, xs = np.nonzero(a > 0)
    if len(ys) == 0: return cam
    y0, y1 = ys.min() // 2 * 2, (ys.max() // 2 + 1) * 2; x0, x1 = xs.min() // 2 * 2, (xs.max() // 2 + 1) * 2
    Y, U, V = Y.copy(), U.copy(), V.copy()
    ab = a[y0:y1, x0:x1].astype(np.float32); m = ab > 0
    g = np.zeros(ab.shape + (3,), np.float32)
    c = np.clip(bp[y0:y1, x0:x1][m] / (255.0 * ab[m][:, None]), 0, 1)
    g[m] = srgb_para_hlg_ycc(c.astype(np.float64)).astype(np.float32)
    yb = Y[y0:y1, x0:x1].astype(np.float32)
    Y[y0:y1, x0:x1] = np.where(m, np.clip(np.rint(yb * (1 - ab) + ab * g[..., 0]), 0, 1023), yb).astype('<u2')
    hh, ww = ab.shape[0] // 2, ab.shape[1] // 2
    a2 = ab.reshape(hh, 2, ww, 2).mean((1, 3)); m2 = a2 > 0
    for P, i in ((U, 1), (V, 2)):
        pb = P[y0 // 2:y1 // 2, x0 // 2:x1 // 2].astype(np.float32)
        pc = (ab * g[..., i]).reshape(hh, 2, ww, 2).mean((1, 3))
        P[y0 // 2:y1 // 2, x0 // 2:x1 // 2] = np.where(m2, np.clip(np.rint(pb * (1 - a2) + pc), 0, 1023), pb).astype('<u2')
    return Y.tobytes() + U.tobytes() + V.tobytes()


# mesmos parâmetros do encoder das bases YAP3 (GOP 30 fechado, sem B-frames): segmentos recodificados colam na base
X265 = ['-c:v', 'libx265', '-preset', 'fast', '-crf', '16', '-pix_fmt', 'yuv420p10le', '-profile:v', 'main10', '-tag:v', 'hvc1',
        '-x265-params', 'colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc:range=limited:chromaloc=0:bframes=0:open-gop=0:'
        'keyint=30:min-keyint=30:scenecut=0:repeat-headers=0:pools=2:frame-threads=1:rc-lookahead=10:log-level=error',
        '-color_primaries', 'bt2020', '-color_trc', 'arib-std-b67', '-colorspace', 'bt2020nc', '-color_range', 'tv',
        '-chroma_sample_location', 'left']

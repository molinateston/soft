#!/usr/bin/env python3
'''Monitor preservado: quadro integral, cortes explícitos e legenda fixa.
Derivado do contrato geométrico de v203_compor, sem dados de projeto.
Uso: python3 compor_monitor.py trabalho/ajustes.json
Dependências: ffmpeg com libass/libx264, ffprobe, Python3 e Pillow.
'''
import argparse, hashlib, json, math, subprocess, time, re
from pathlib import Path
from PIL import ImageFont

def run(cmd):
    subprocess.run(cmd, check=True, timeout=3300)
def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('config');a=ap.parse_args()
    cfgpath=Path(a.config).resolve();base=cfgpath.parent
    c=json.loads(cfgpath.read_text()); resolve=lambda x: (base/x).resolve()
    src=resolve(c['fonte']); out=resolve(c['saida']); out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists(): raise ValueError('Saída já existe; escolha nova versão')
    fontpath=resolve(c['marca']['fonte_arquivo']); wordsfile=resolve(c['palavras'])
    if not c['marca'].get('fonte_uso_autorizado'):raise ValueError('Registre licença ou autorização da fonte')
    font=ImageFont.truetype(str(fontpath),72); family=font.getname()[0]
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(src)]))
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'])!=(1080,1920):raise ValueError('Monitor exige fonte 1080x1920; não reenquadrar silenciosamente')
    duration=float(probe['format']['duration']); segs=c['segmentos'];speed=1.15
    prev=0
    for lo,hi in segs:
        if not (prev<=lo<hi<=duration):raise ValueError('Segmentos inválidos, sobrepostos ou fora da fonte')
        prev=hi
    words=json.loads(wordsfile.read_text());mapped=[];acc=0
    for lo,hi in segs:
        for w in words:
            s,e,text=w[:3]
            if s<hi and e>lo:
                if s<lo or e>hi:raise ValueError('Corte atravessa palavra: '+text)
                mapped.append(((acc+s-lo)/speed,(acc+e-lo)/speed,text))
        acc+=hi-lo
    dur=acc/speed
    def ts(t):
        cs=math.floor(t*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
    ass=out.with_suffix('.ass');events=[]
    header=f'''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Leg,{family},72,&H00F5F9FA,&H00F5F9FA,&H80000000,&H96000000,0,0,0,0,100,100,0,0,1,3,2,6,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    for i,(s,e,text) in enumerate(mapped):
        if len(text.split())!=1 or any(ch in text for ch in '{}\\\n'):raise ValueError('Palavras devem ser literais, individuais e sem controle ASS')
        end=min(s+.7,mapped[i+1][0] if i+1<len(mapped) else e,dur)
        fs=72
        while fs>52 and ImageFont.truetype(str(fontpath),fs).getlength(text)>875:fs-=1
        width=ImageFont.truetype(str(fontpath),fs).getlength(text)
        if width>875:raise ValueError('Palavra não cabe com mínimo 52: '+text)
        if end<=s:raise ValueError('Tempos de palavras duplicados ou inválidos')
        events.append(f'Dialogue: 0,{ts(s)},{ts(end)},Leg,,0,0,0,,{{\\an6\\pos(940,1250)\\fs{fs}}}{text}')
    ass.write_text(header+'\n'.join(events)+'\n')
    # Nenhum filtro geométrico: cada trecho mantém o quadro completo da fonte.
    filters=[];inputs=[]
    for i,(lo,hi) in enumerate(segs):
        filters += [f'[0:v]trim=start={lo}:end={hi},setpts=(PTS-STARTPTS)/{speed}[v{i}]',f'[0:a]atrim=start={lo}:end={hi},asetpts=PTS-STARTPTS,atempo={speed},afade=t=in:d=0.004,afade=t=out:st={max(0,(hi-lo)/speed-.004)}:d=0.004[a{i}]']
        inputs.append(f'[v{i}][a{i}]')
    filters.append(''.join(inputs)+f'concat=n={len(segs)}:v=1:a=1[vc][ac]')
    def esc(path):return str(path).replace('\\','\\\\').replace(':','\\:').replace("'","\\'")
    filters.append(f"[vc]fps=30,subtitles=filename='{esc(ass)}':fontsdir='{esc(fontpath.parent)}'[vf]")
    gain=c.get('ganho_db')
    if gain is None:
        af=[]
        for i,(lo,hi) in enumerate(segs):
            af.append(f'[0:a]atrim=start={lo}:end={hi},asetpts=PTS-STARTPTS,atempo={speed}[m{i}]')
        af.append(''.join(f'[m{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,ebur128=peak=true[measure]')
        measure=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-i',str(src),'-filter_complex',';'.join(af),'-map','[measure]','-f','null','-'],capture_output=True,text=True,timeout=180)
        measure.check_returncode();out.with_suffix('.peak-entrada.log').write_text(measure.stderr)
        peaks=re.findall(r'Peak:\s+(-?[0-9.]+) dBFS',measure.stderr)
        if not peaks:raise ValueError('Medição de true peak ausente')
        gain=-1.5-float(peaks[-1])
    overlays=c.get('camadas',[])
    prevlabel='vc'
    extra=[]
    for i,item in enumerate(overlays):
        from PIL import Image
        png=resolve(item['arquivo']);im=Image.open(png).convert('RGBA');bbox=im.getbbox()
        if bbox is None:raise ValueError('Camada vazia')
        x,y=item.get('x',0),item.get('y',0);bb=[bbox[0]+x,bbox[1]+y,bbox[2]+x,bbox[3]+y]
        if bb[0]<65 or bb[2]>1015 or bb[1]<195 or bb[3]>1400:raise ValueError('Camada fora da zona de texto')
        for region in c['areas_protegidas']:
            if min(bb[2],region[2])>max(bb[0],region[0]) and min(bb[3],region[3])>max(bb[1],region[1]):raise ValueError('Camada toca área protegida')
        extra+=['-loop','1','-i',str(png)]
        filters.append(f'[{prevlabel}][{i+1}:v]overlay=x={x}:y={y}:enable=between(t\\,{item["inicio"]}\\,{item["fim"]}):shortest=1[ov{i}]')
        prevlabel=f'ov{i}'
    if overlays:
        filters=[f for f in filters if not f.startswith('[vc]fps=')]
        filters.append(f"[{prevlabel}]fps=30,subtitles=filename='{esc(ass)}':fontsdir='{esc(fontpath.parent)}'[vf]")

    filters.append(f'[ac]volume={float(gain)}dB[af]')
    graph=out.with_suffix('.filter');graph.write_text(';\n'.join(filters))
    cmd=['ffmpeg','-hide_banner','-nostdin','-v','warning','-n','-i',str(src),*extra,'-filter_complex_script',str(graph),'-map','[vf]','-map','[af]','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)]
    start=time.monotonic();run(cmd)
    manifest={'estado':'RENDERIZADO, CONFERÊNCIA PENDENTE','duracao_planejada':dur,'tempo_render_s':time.monotonic()-start,'comando':cmd,'hashes':{str(p.name):digest(p) for p in [src,fontpath,wordsfile,cfgpath,Path(__file__),out]+[resolve(x['arquivo']) for x in overlays]},'quadros':'fonte integral sem crop, zoom ou blur','palavras':len(mapped),'ganho_db':gain}
    out.with_suffix('.manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print(json.dumps(manifest,ensure_ascii=False))
if __name__=='__main__':main()

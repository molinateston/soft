#!/usr/bin/env python3
"""Regressão da noite de 25/09: checar_titulos.py chegou a 17 GB.

A missão apontou --insumos pra árvore inteira de trabalho. O script lia todos os
arquivos de texto da pasta pra memória de uma vez e ainda montava duas cópias
concatenadas (nomes e aspas): a memória crescia com a PASTA, não com a peça. O
conserto lê um arquivo por vez e põe três tetos (tamanho da pasta, tempo e
memória) que param com exit 3 e mensagem clara. O teto da pasta conta só texto
(o binário não entra) e tem padrão de 512 MB, medido contra os --insumos reais:
a pasta legítima maior tinha 56 MB de texto, a errada da noite tinha 3,1 GB.

Estes testes reproduzem a forma da entrada que explodia (muitos arquivos de
texto, com nome de pessoa e aspa que obrigam a ler a pasta toda) e provam que:
  1. a árvore maior que o teto para em segundos, com exit 3, sem ler;
  2. com o teto aberto, a memória fica do tamanho de UM arquivo, não da pasta;
  3. a pasta legítima grande (texto abaixo do teto e um deck binário pesado,
     como a do brain) passa com o teto PADRÃO e dá o veredito completo;
  4. o veredito de nome e de aspa é o mesmo da versão que lia tudo junto;
  5. o teto de tempo e o de memória disparam.

Rode: python3 tests/test_checar_titulos_memoria.py
"""
import importlib.util
import os
import resource
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / 'scripts' / 'checar_titulos.py'


def carregar():
    sys.dont_write_bytecode = True  # a pasta da skill não ganha __pycache__
    spec = importlib.util.spec_from_file_location('checar_titulos_mem', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ct = carregar()

MB = 1024 * 1024
# o exit do teto de defesa é contrato da linha de comando (a missão lê o exit),
# por isso fica fixo aqui e não é lido do módulo
EXIT_TETO = 3
# a peça cita uma pessoa pelo nome e traz uma aspa atribuída a ela: é o que
# obriga o script a ler a pasta de insumos inteira (nomes e lastro da aspa)
PECA = ('# Como a Marcela parou de perder cliente\n\n'
        'A cliente me mandou isto: "o agente respondeu antes de mim, de madrugada"\n\n'
        'Comenta AGENTE que eu te mando o passo a passo.\n')
LINHA = ('Marcela, 34: o agente respondeu antes de mim e eu nem acordei ainda, '
         'conta ela na conversa de ontem sobre o atendimento da loja.\n')


def montar_arvore(raiz, n_arquivos, mb_por_arquivo):
    """A forma da entrada que explodia: muitos arquivos de texto grandes, com a
    pessoa citada em linha de pessoa (o candidato sobrevive e força a leitura)."""
    insumos = Path(raiz) / 'trabalho'
    reps = max(1, int(mb_por_arquivo * MB) // len(LINHA.encode('utf-8')))
    bloco = LINHA * reps
    for i in range(n_arquivos):
        sub = insumos / f'pasta-{i % 7:02d}' / f'rodada-{i:03d}'
        sub.mkdir(parents=True, exist_ok=True)
        (sub / f'caixa-de-entrada-{i:03d}.md').write_text(bloco, encoding='utf-8')
    # a aspa só existe no ÚLTIMO arquivo, quebrada em duas linhas
    (insumos / 'zz-ultimo.md').write_text(
        'conversa com a cliente\n"o agente respondeu antes de mim,\nde madrugada"\n',
        encoding='utf-8')
    (insumos / 'perfil.md').write_text('# Perfil\nNome: Dono Exemplo\n', encoding='utf-8')
    saida = Path(raiz) / 'entrega'
    saida.mkdir()
    (saida / 'carrossel.md').write_text(PECA, encoding='utf-8')
    return insumos, saida / 'carrossel.md'


def rodar(args, env_extra, teto_as_mb=1024, timeout=120):
    """Roda o script num processo filho com teto de endereço e timeout, e devolve
    (exit, saída, pico de memória DESTE filho em MB, segundos). O pico vem do
    wait4 do próprio filho, não do acumulado dos filhos do teste."""
    env = dict(os.environ, **env_extra)

    def teto():
        resource.setrlimit(resource.RLIMIT_AS, (teto_as_mb * MB, teto_as_mb * MB))
        os.nice(19)

    t0 = time.time()
    with tempfile.TemporaryFile() as out:
        proc = subprocess.Popen([sys.executable, '-B', str(SCRIPT)] + args, env=env,
                                stdout=out, stderr=subprocess.STDOUT, preexec_fn=teto)
        while True:
            pid, status, uso = os.wait4(proc.pid, os.WNOHANG)
            if pid:
                break
            if time.time() - t0 > timeout:
                proc.kill()
                pid, status, uso = os.wait4(proc.pid, 0)
                break
            time.sleep(0.05)
        proc.returncode = os.waitstatus_to_exitcode(status)
        out.seek(0)
        saida = out.read().decode('utf-8', errors='replace')
    return proc.returncode, saida, uso.ru_maxrss / 1024, time.time() - t0


class ArvoreGrandeDeInsumos(unittest.TestCase):
    """A entrada que explodia: 40 arquivos de 2 MB (80 MB de texto)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.insumos, cls.peca = montar_arvore(cls.tmp.name, 40, 2)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def args(self):
        return ['--peca', str(self.peca), '--insumos', str(self.insumos),
                '--perfil', str(self.insumos / 'perfil.md')]

    def test_1_arvore_maior_que_o_teto_para_rapido_com_exit_3(self):
        # os 80 MB desta árvore ficam acima de um teto de 32 MB: é a mesma forma
        # da árvore de trabalho da noite (3,1 GB de texto contra o padrão de 512)
        code, saida, pico, seg = rodar(self.args(), {'CHECAR_TITULOS_TETO_INSUMOS_MB': '32'})
        self.assertEqual(code, EXIT_TETO, saida[-800:])
        self.assertIn('PAREI SEM CONFERIR', saida)
        self.assertIn('pasta de insumos', saida)
        self.assertLess(seg, 30)
        self.assertLess(pico, 120, f'pico {pico:.0f} MB só pra medir a pasta')

    def test_2_teto_aberto_memoria_do_tamanho_de_um_arquivo(self):
        # teto de pasta aberto: o script lê os 80 MB inteiros. A versão antiga
        # guardava tudo (e mais duas cópias concatenadas) e passava de 250 MB;
        # agora o pico fica perto da base do Python mais UM arquivo de 2 MB.
        code, saida, pico, seg = rodar(
            self.args(), {'CHECAR_TITULOS_TETO_INSUMOS_MB': '100000'}, teto_as_mb=512)
        self.assertNotEqual(code, EXIT_TETO, saida[-800:])
        self.assertNotIn('MemoryError', saida)
        self.assertIn('nomes candidatos achados pelo script: 1', saida)
        self.assertIn('Marcela · na peça', saida)
        self.assertIn('aspas de citação verificadas contra o insumo: 1 · sem lastro: 0', saida)
        self.assertLess(pico, 90, f'pico {pico:.0f} MB para 80 MB de insumo: cresce com a pasta')

    def test_3_teto_de_tempo_para_pela_linha_de_comando(self):
        # teto de pasta aberto e 1 segundo de tempo: ler 80 MB passa disso, e a
        # saída tem de ser o exit 3 com a explicação, não um processo que segue
        code, saida, pico, seg = rodar(
            self.args(), {'CHECAR_TITULOS_TETO_INSUMOS_MB': '100000',
                          'CHECAR_TITULOS_TETO_SEGUNDOS': '1'}, teto_as_mb=512)
        self.assertEqual(code, EXIT_TETO, saida[-800:])
        self.assertIn('teto de tempo', saida)
        self.assertLess(seg, 20)


class PastaLegitimaComBinarioPesado(unittest.TestCase):
    """A pasta real que o teto de 64 MB travava: /home/cloud/.leon/brain, com
    34 MB de texto e decks .pptx que somavam 68 MB. Aqui: 40 MB de texto e um
    deck binário de 600 MB (esparso, não ocupa disco). Com o teto PADRÃO a
    conferência roda inteira, e o deck nem é lido pra achar nome."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.insumos, cls.peca = montar_arvore(cls.tmp.name, 20, 2)
        deck = cls.insumos / 'zzz-deck-da-aula.pptx'
        with open(deck, 'wb') as h:
            h.write(b'PK\x03\x04\x14\x00\x06\x00' + b'\0' * 1024)
            h.truncate(600 * MB)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_teto_padrao_nao_trava_pasta_legitima(self):
        env = {k: '' for k in ('CHECAR_TITULOS_TETO_INSUMOS_MB',
                               'CHECAR_TITULOS_TETO_INSUMOS_ARQUIVOS')}
        code, saida, pico, seg = rodar(
            ['--peca', str(self.peca), '--insumos', str(self.insumos),
             '--perfil', str(self.insumos / 'perfil.md')], env, teto_as_mb=512)
        self.assertNotEqual(code, EXIT_TETO, saida[-800:])
        self.assertNotIn('PAREI SEM CONFERIR', saida)
        self.assertIn('nomes candidatos achados pelo script: 1', saida)
        self.assertIn('aspas de citação verificadas contra o insumo: 1 · sem lastro: 0', saida)
        self.assertLess(pico, 90, f'pico {pico:.0f} MB: o deck binário foi lido inteiro')


class MesmoVeredito(unittest.TestCase):
    """O conserto não muda o veredito: comparado com a leitura antiga, que
    juntava o texto de todos os insumos antes de procurar."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_aspa_atravessa_linha_e_arquivo_igual_a_concatenacao(self):
        # pela linha de comando, como a missão chama: roda igual na versão que
        # concatenava tudo e na que lê um arquivo por vez. A 1a aspa só existe
        # quebrada entre a.md e b.md, a 2a muda só a caixa, a 3a não existe.
        ins = self.dir / 'ins'
        ins.mkdir()
        (ins / 'a.md').write_text('ela falou assim: tudo mudou quando o\n', encoding='utf-8')
        (ins / 'b.md').write_text('agente   passou a responder\nde noite\n', encoding='utf-8')
        (ins / 'c.md').write_text('   \n', encoding='utf-8')
        peca = self.dir / 'carrossel.md'
        peca.write_text(
            '# Três clientes\n\n'
            'A cliente me disse: "tudo mudou quando o agente passou a responder de noite"\n\n'
            'Outra cliente disse: "Agente passou a responder de noite"\n\n'
            'Uma terceira cliente disse: "isto nunca foi dito por ninguém aqui"\n',
            encoding='utf-8')
        code, saida, _pico, _seg = rodar(['--peca', str(peca), '--insumos', str(ins)], {})
        self.assertIn('aspas de citação verificadas contra o insumo: 3 · sem lastro: 1', saida)
        self.assertIn('isto nunca foi dito', saida)

    def test_nome_de_conversa_privada_continua_achado(self):
        ins = self.dir / 'ins'
        (ins / 'sub').mkdir(parents=True)
        (ins / 'sub' / 'caixa-de-entrada.md').write_text(
            'Marcela, 34: o agente respondeu antes de mim\n', encoding='utf-8')
        (ins / 'notas.md').write_text('Roberto, 50: gostei\nfalei com o roberto\n',
                                      encoding='utf-8')
        peca = self.dir / 'carrossel.md'
        peca.write_text('# A Marcela e o Roberto\n\nA Marcela respondeu.\n', encoding='utf-8')
        achados = ct.candidatos_a_nome([peca], ins, None)
        # Roberto aparece em minúscula num insumo: palavra comum, some
        self.assertEqual(list(achados), ['Marcela'])
        self.assertTrue(achados['Marcela']['privado'])
        self.assertFalse(achados['Marcela']['autorizado'])
        self.assertEqual(len(achados['Marcela']['insumo']), 1)

    def test_ordem_dos_arquivos_igual_ao_rglob_ordenado(self):
        ins = self.dir / 'ins'
        for rel in ['a/x.md', 'a.txt', 'b/node_modules/y.md', 'b/z.md', 'b/w.png',
                    'out/saida.md', 'A/k.md', '.oculto/o.md']:
            p = ins / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('texto\n', encoding='utf-8')
        velho = [f for f in sorted(ins.rglob('*'))
                 if f.is_file() and f.suffix.lower() not in ct.IGNORAR_EXT
                 and not ct.IGNORAR_DIR.search('/' + f.relative_to(ins).as_posix())]
        self.assertEqual(ct.arquivos_de_insumo(ins), velho)


class TetosDeTempoEMemoria(unittest.TestCase):
    def rodar_trecho(self, codigo, env_extra):
        env = dict(os.environ, **env_extra)
        prog = (f'import importlib.util,sys\n'
                f'spec=importlib.util.spec_from_file_location("c",{str(SCRIPT)!r})\n'
                f'c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)\n'
                + codigo)
        return subprocess.run([sys.executable, '-B', '-c', prog], env=env, capture_output=True,
                              text=True, timeout=60)

    def test_teto_de_tempo_dispara(self):
        r = self.rodar_trecho(
            'c.armar_tetos()\n'
            'try:\n'
            '    while True: pass\n'
            'except c.TetoEstourado as e:\n'
            '    print("parou:", e)\n',
            {'CHECAR_TITULOS_TETO_SEGUNDOS': '1'})
        self.assertIn('parou: a conferência passou de 1 segundos', r.stdout, r.stderr)

    def test_teto_de_memoria_dispara(self):
        r = self.rodar_trecho(
            'c.armar_tetos()\n'
            'try:\n'
            '    x = bytearray(600 * 1024 * 1024)\n'
            '    print("alocou")\n'
            'except MemoryError:\n'
            '    print("parou na memoria")\n',
            {'CHECAR_TITULOS_TETO_MEMORIA_MB': '300'})
        self.assertIn('parou na memoria', r.stdout, r.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Valida contrato estrutural do storyboard; sem aprovação semântica ou audiovisual."""
import argparse, json, math

def validar(p):
    falhas=[]
    formato=p.get('formato')
    if formato not in ('talking_head_yap4','monitor_preservado','palestra_conceito'): falhas.append('formato ausente/inválido')
    dur=p.get('duracao_s',0)
    if not isinstance(dur,(int,float)) or not math.isfinite(dur) or dur<=0: falhas.append('duração inválida'); dur=0
    cenas=p.get('cenas',[]); end=0; ids=set()
    if not cenas: falhas.append('sem cenas')
    campos=['id','saida','fonte','fala','ancora','palavras_ids','material','composicao','legenda','transicao','cta_loop','criterio']
    for i,c in enumerate(cenas):
        for k in campos:
            if k not in c or c[k] in ('',None,[]): falhas.append(f'cena {i}: falta {k}')
        if c.get('id') in ids: falhas.append(f'cena {i}: ID repetido')
        ids.add(c.get('id'))
        ab=c.get('saida',[])
        if not isinstance(ab,list) or len(ab)!=2 or not all(isinstance(v,(int,float)) and math.isfinite(v) for v in ab) or ab[1]<=ab[0]:
            falhas.append(f'cena {i}: intervalo inválido'); continue
        a,b=ab
        if abs(a-end)>1/30+.0001: falhas.append(f'cena {i}: lacuna/sobreposição')
        end=b
        if formato=='monitor_preservado' and c.get('transformacao_camera')!='preservar': falhas.append(f'cena {i}: monitor exige preservar câmera')
    if abs(end-dur)>1/30+.0001: falhas.append('cenas não cobrem duração')
    if p.get('tipo_prova')=='completa' and formato=='palestra_conceito' and not 90<=dur<=300: falhas.append('palestra completa exige 90 a 300 s')
    if not isinstance(p.get('promessas_revisadas'),bool) or not p.get('promessas_revisadas'): falhas.append('revisão de promessas ausente')
    for loop in p.get('loops',[]):
        if not isinstance(loop.get('abre'),(int,float)) or not isinstance(loop.get('fecha'),(int,float)) or not 0<=loop['abre']<=loop['fecha']<=dur or not loop.get('evidencia'): falhas.append('loop aberto ou sem evidência')
    return falhas

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('arquivo'); a=ap.parse_args()
    try: p=json.load(open(a.arquivo)); f=validar(p)
    except (OSError,ValueError,TypeError,AttributeError) as e: print('REPROVA',e); return 1
    print(json.dumps(dict(status='REPROVA' if f else 'PASSA_ESTRUTURA',falhas=f),ensure_ascii=False,indent=2))
    return int(bool(f))
if __name__=='__main__': raise SystemExit(main())

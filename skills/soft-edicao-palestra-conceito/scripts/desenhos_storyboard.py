"""Apoio gráfico por estado do storyboard VPS. Sem marcas, nomes ASR ou dados do cliente.
C06/C07 são comentários laterais: tarja inferior vazia, conforme o plano.
C32 mantém o último estado. Escala comum por grupo evita saltos entre estados.
"""
from desenhos_exemplo import casa, computador, servidor
from linhas import T,X,ret,circ,seta

def flecha(x0,y0,x1,y1,cor='a'):
    return [T(p,cor,3) for p in seta(x0,y0,x1,y1)]
def agente(x=760,y=245):
    return [T(circ(x,y,30),'a'),X('agente',x,y+58,28,'a')]
def remoto():return servidor(760,235,1.1)+[X('VPS',760,370,32)]
def local():return casa(260,180,1.2)+computador(260,270,.65)+[X('local',260,385,28)]
def pergunta():return [T(ret(600,140,925,360,20)),X('?',760,190,40)]+agente(760,260)
def barra(x,y,label):return [X(label,x,y-24,25),T(ret(x-90,y,x+90,y+25)),T([(x,y),(x,y+25)],'a')]
def montar(cid):
    n=int(cid[1:]);d=[]
    if n in (6,7):return [],[]
    if n==4:d=pergunta()
    elif n==5:d=computador(540,240,1.8)+[X('computador',540,390,32)]
    elif n in (8,9):
        d=remoto()+agente()
        if n==9:d+=flecha(650,235,350,235)+[T(circ(270,235,55)),X('rede',270,330,28),X('assinatura',760,430,28)]
    elif n==10:d=remoto()+[X('segurança?',350,245,38,'a')]
    elif 11<=n<=15:
        d=local()
        if n>=12:d+=[X('proteção local',260,440,25)]+flecha(80,230,170,230)
        if n>=13:d+=remoto()+[X('empresa contratada',760,440,25)]
        if n==14:d+=[T([(335,290),(490,290)],'a',2),X('conhecimento',480,345,25)]
        if n==15:d=local()+remoto()+[X('comparação relativa',540,450,28)]
    elif 16<=n<=19:
        d=remoto()
        if n>=16:d+=[X('assinatura',760,430,28)]
        if n>=17:d+=barra(300,220,'memória RAM')+barra(300,330,'capacidade')
        if n>=18:d+=agente()
        if n==19:d+=[T(circ(510,140,38),'a'),T([(510,140),(510,115)],'a'),T([(510,140),(530,155)],'a'),X('24 h / 7 dias',450,490,30,'a')]
    elif 20<=n<=24:
        d=local()+remoto()+agente(260,270)
        if n==21:d+=[X('desligado',260,440,28,'a')]
        if n in (22,23):d+=[T(ret(110,110,260,170)),T(ret(280,110,430,170)),X('programas',270,80,25)]+barra(760,440,'memória compartilhada')
        if n==23:d+=barra(760,135,'processamento')
        if n==24:d=local()+remoto()+agente()+[X('recursos do agente',760,440,28,'a')]
    elif n>=25:
        d=remoto()+agente()
        d+=[T(ret(250,170,430,300,14),'a'),X('modelo',340,235,30,'a')]+flecha(450,235,660,235)
        if n==26:d+=[X('A / B / C / D',340,345,27)]
        if n==27:d+=[X('A → B',340,345,32,'a')]
        if n==28:d+=[T(ret(90,380,330,440)),X('comando',210,410,26)]+flecha(350,410,650,300)
        if n>=29:d+=flecha(760,180,510,100)+[X('orquestração',490,70,28)]
        if n>=30:d+=[T(circ(340,420,30),'a'),X('auxiliar',340,480,28)]+flecha(690,300,380,400)
    return [],d

def existe(cid):return cid.startswith('C') and cid[1:].isdigit() and 4<=int(cid[1:])<=32


def montar_tempo(cid, t):
    """Tempos relativos ao início do estado; âncoras do exemplo em palavras auditadas.
    Contrato opcional: None conserva stroke reveal padrão.
    """
    from linhas import arco
    if cid == 'C19':
        _, d = montar('C18')
        # ligado -> relógio progride; 24 -> aro completo; 7 -> sete marcas.
        progresso = min(1., max(.01, t / 1.634))
        d += [T(arco(510,140,38,-90,-90+360*progresso),'a'),
              T([(510,140),(510+25*__import__('math').sin(t*2),140-25*__import__('math').cos(t*2))],'a')]
        if t >= 1.634: d += [X('24 h',450,450,30,'a')]
        if t >= 2.4:
            d += [T([(440+i*16,365),(440+i*16,385)],'a') for i in range(7)]
            d += [X('7 dias',450,490,30,'a')]
        return [], d
    if cid == 'C26':
        _, d = montar('C25')
        i=sum(t >= x for x in (.487,1.478,2.017))
        d += [X('ABCD'[i],340,345,32,'a')]
        return [], d
    if cid == 'C27':
        _, d = montar('C25')
        u=min(1.,max(0.,t/.7))
        d += [X('A' if u<.5 else 'B',340+int(70*(u if u<.5 else u-1)),345,32,'a')]
        return [], d
    return None

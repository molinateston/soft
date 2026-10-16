#!/usr/bin/env python3
"""Browser regression of the two fictional examples, with no external transmission.
Requires Python Playwright and Chromium. Generates isolated output and evidence.
"""
import argparse,itertools,json,subprocess,sys,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
skill=Path(__file__).resolve().parent.parent
for filename,folder in [('organizacao-checkout.json','organizacao'),('biblioteca-reuniao.json','biblioteca')]:
 subprocess.run([sys.executable,str(skill/'scripts/build_quiz.py'),str(skill/'examples'/filename),'--out',str(out/folder)],check=True)
results=[];errors=[];requests=[]
def record(name):results.append(name)
def check(ok,name):
 if not ok:raise AssertionError(name)
 record(name)
def click(page,text):page.get_by_role('button',name=text,exact=True).click()
def next_(page):click(page,'Continuar')
def root(page,name):page.goto((out/name/'index.html').as_uri())
def answer(page,text):click(page,text);next_(page)
def org(page,a,b,materials=('Contas',),capture=False):
 root(page,'organizacao');answer(page,a);next_(page);answer(page,b)
 for m in materials:click(page,m)
 next_(page)
 if capture:
  page.locator('#contact').fill('teste-quiz@example.invalid');page.locator('#consent').check();click(page,'Ver resultado com o contato nesta sessão')
 else:click(page,'Continuar sem contato')
def lib(page,a,tool='Ainda não usamos uma ferramenta',experience=None,responsible='Sim, participo das decisões',n='120'):
 root(page,'biblioteca');answer(page,a);answer(page,tool)
 if experience:answer(page,experience)
 page.locator('#answer').fill(n);next_(page);page.locator('#answer').fill('Consulta fictícia <script>window.unwanted=true</script>');next_(page);click(page,responsible)
def nooverflow(page,label):check(page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),label)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for viewport in [dict(width=1365,height=900),dict(width=390,height=844)]:
  ctx=browser.new_context(viewport=viewport);ctx.route('**/*',lambda route: route.continue_() if route.request.url.startswith('file:') else (requests.append(route.request.url),route.abort())[-1]);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));tag=str(viewport['width'])
  org(page,'Esqueço em qual pasta guardei','Uso poucas pastas',capture=True)
  check(page.locator('#screen').get_attribute('data-profile')=='localizar',tag+' org result localiza')
  check(page.get_by_text('Contato mantido apenas nesta sessão. Nenhum envio realizado.',exact=True).is_visible(),tag+' capture honest')
  check(page.locator('[data-testid=media-absent]').is_visible(),tag+' video absent honest')
  nooverflow(page,tag+' org no overflow');page.screenshot(path=str(out/f'org-{tag}.png'),full_page=True)
  check(page.locator('[data-testid=cta]').get_attribute('href')=='destinos/checkout.html',tag+' checkout href')
  page.locator('[data-testid=cta]').click();check(page.get_by_role('heading',name='Checkout de demonstração').is_visible(),tag+' checkout reached without purchase')
  lib(page,'Encontrar títulos já registrados')
  check(page.locator('#screen').get_attribute('data-profile')=='busca',tag+' library result busca')
  check(page.locator('#screen').get_attribute('data-eligible')=='true',tag+' eligible')
  check(page.evaluate('window.unwanted===undefined'),tag+' free text escaped')
  nooverflow(page,tag+' library no overflow');page.screenshot(path=str(out/f'biblioteca-{tag}.png'),full_page=True)
  page.locator('[data-testid=cta]').click();check(page.get_by_role('heading',name='Agenda de demonstração').is_visible(),tag+' agenda reached without booking')
  lib(page,'Cadastrar os títulos de forma consistente',responsible='Não, preciso envolver outra pessoa')
  check(page.locator('[data-testid=cta]').get_attribute('href')=='destinos/orientacao.html',tag+' ineligible alternative')
  page.locator('[data-testid=cta]').click();check(page.get_by_role('heading',name='Orientação alternativa').is_visible(),tag+' alternative reached')
  ctx.close()
 # Exhaustive discrete combinations for each example. Text/number are equivalence classes below.
 ctx=browser.new_context();ctx.route('**/*',lambda r:r.continue_() if r.request.url.startswith('file:') else (requests.append(r.request.url),r.abort())[-1]);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 materials=[('Contas',),('Contratos',),('Notas de compra',),('Contas','Contratos'),('Contas','Notas de compra'),('Contratos','Notas de compra')]
 for a,b,ms in itertools.product(range(3),range(3),materials):
  org(page,['Esqueço em qual pasta guardei','Os assuntos estão misturados','As duas situações acontecem'][a],['Uso poucas pastas','Uso várias caixas','Guardo tudo em arquivos digitais'][b],ms)
  left=(2 if a==0 else 0)+(1 if b==0 else 0);right=(2 if a==1 else 0)+(1 if b==1 else 0)
  expected='localizar' if left>=right else 'separar'
  check(page.locator('#screen').get_attribute('data-profile')==expected,f'org combination {a}/{b}/{ms} -> {expected}')
  if left==right:check(page.get_by_text('Suas respostas apontam prioridades próximas.',exact=False).is_visible(),'org tie disclosed')
 for a,branch,eligible in itertools.product(range(3),range(3),[True,False]):
  lib(page,['Cadastrar os títulos de forma consistente','Encontrar títulos já registrados','As duas tarefas precisam de atenção'][a],tool='Ainda não usamos uma ferramenta' if branch==0 else 'Sim, já usamos uma ferramenta',experience=None if branch==0 else ['Começamos recentemente','Já usamos há bastante tempo'][branch-1],responsible='Sim, participo das decisões' if eligible else 'Não, preciso envolver outra pessoa')
  left=(2 if a==0 else 0)+(1 if branch==1 else 0);right=(2 if a==1 else 0)+(1 if branch==2 else 0)
  check(page.locator('#screen').get_attribute('data-profile')==('cadastro' if left>=right else 'busca'),f'library combination {a}/{branch}/{eligible}')
  check(page.locator('[data-testid=cta]').get_attribute('href')==('destinos/agenda.html' if eligible else 'destinos/orientacao.html'),'library eligibility CTA')
 # Required input, multi bounds, keyboard.
 root(page,'organizacao');next_(page);check(page.get_by_role('alert').is_visible(),'single required');page.get_by_role('button',name='Esqueço em qual pasta guardei',exact=True).focus();page.keyboard.press('Enter');next_(page);next_(page);answer(page,'Uso poucas pastas');next_(page);check(page.get_by_role('alert').is_visible(),'multi minimum');click(page,'Contas');click(page,'Contratos');click(page,'Notas de compra');check(page.get_by_role('alert').is_visible(),'multi maximum');check(page.get_by_role('button',name='Notas de compra',exact=True).get_attribute('aria-pressed')=='false','multi maximum not accepted');next_(page)
 page.locator('#contact').fill('email-invalido');click(page,'Ver resultado com o contato nesta sessão');check(page.locator('#contact').is_visible(),'invalid email stays');page.locator('#contact').fill('teste@example.invalid');click(page,'Ver resultado com o contato nesta sessão');check(page.locator('#consent').is_visible(),'consent required');click(page,'Continuar sem contato');check(page.get_by_text('Você continuou sem informar contato.',exact=True).is_visible(),'capture skip');click(page,'Recomeçar e limpar respostas');check(page.get_by_role('button',name='Esqueço em qual pasta guardei',exact=True).get_attribute('aria-pressed')=='false','restart clears answers')
 # Back preserves valid answers; changing parent removes stale dependent answer and score.
 lib(page,'As duas tarefas precisam de atenção',tool='Sim, já usamos uma ferramenta',experience='Já usamos há bastante tempo')
 click(page,'Voltar');check(page.locator('#answer').input_value().startswith('Consulta fictícia'),'back retains text');click(page,'Voltar');check(page.locator('#answer').input_value()=='120','back retains number');click(page,'Voltar');check(page.get_by_role('button',name='Já usamos há bastante tempo',exact=True).get_attribute('aria-pressed')=='true','back retains branch');click(page,'Voltar');answer(page,'Ainda não usamos uma ferramenta');check(page.get_by_role('heading',name='Quantos títulos estão no catálogo hoje?').is_visible(),'branch skipped after changing parent');next_(page);next_(page);click(page,'Sim, participo das decisões');check(page.locator('#screen').get_attribute('data-profile')=='cadastro','hidden branch score removed');check(page.get_by_text('Há quanto tempo a biblioteca usa essa ferramenta?',exact=False).count()==0,'hidden answer removed from summary')
 # Number boundaries and text validation.
 root(page,'biblioteca');answer(page,'Cadastrar os títulos de forma consistente');answer(page,'Ainda não usamos uma ferramenta');next_(page);check(page.get_by_role('alert').is_visible(),'empty number rejected');page.locator('#answer').fill('-1');next_(page);check(page.get_by_role('alert').is_visible(),'negative number rejected');page.locator('#answer').fill('100001');next_(page);check(page.get_by_role('alert').is_visible(),'number above max rejected');page.locator('#answer').fill('0.5');next_(page);check(page.get_by_role('alert').is_visible(),'fractional count rejected');page.locator('#answer').fill('0');next_(page);next_(page);check(page.get_by_role('alert').is_visible(),'empty text rejected');click(page,'Voltar');page.locator('#answer').fill('100000');next_(page);page.locator('#answer').fill('Teste fictício');next_(page);check(page.locator('[data-testid=cta]').count()==0,'no agenda before qualification');click(page,'Sim, participo das decisões');check(page.locator('[data-testid=cta]').is_visible(),'agenda after qualification')
 # Exercise actual local media without inventing a commercial recording.
 aux=out/'media-fixture';aux.mkdir(exist_ok=True);shutil.copytree(skill/'examples/destinos',aux/'destinos',dirs_exist_ok=True)
 subprocess.run(['ffmpeg','-y','-f','lavfi','-i','color=c=white:s=160x120:d=0.3','-c:v','libx264','-pix_fmt','yuv420p',str(aux/'fixture.mp4')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 fixture=json.loads((skill/'examples/organizacao-checkout.json').read_text());fixture['capture']={'mode':'none'}
 fixture['steps']=[{'id':'video-intro','type':'video','title':'Vídeo técnico fictício de teste','purpose':'Testar player local, sem alegação comercial.','media':{'title':'Arquivo sintético para teste','src':'fixture.mp4','transcript':'Arquivo sintético branco, sem fala nem prova comercial.'}}]+fixture['steps']
 fixture['resultMedia']['src']='fixture.mp4'
 (aux/'fixture.json').write_text(json.dumps(fixture,ensure_ascii=False));subprocess.run([sys.executable,str(skill/'scripts/build_quiz.py'),str(aux/'fixture.json'),'--out',str(aux/'build')],check=True,stdout=subprocess.DEVNULL)
 page.goto((aux/'build/index.html').as_uri());page.wait_for_function('document.querySelector("video").readyState>=2');check(page.locator('video').is_visible(),'interstitial local video decoded');page.evaluate('document.querySelector("video").muted=true;document.querySelector("video").play()');page.wait_for_function('document.querySelector("video").currentTime>0');check(True,'local video playback advanced');next_(page);answer(page,'Esqueço em qual pasta guardei');next_(page);answer(page,'Uso poucas pastas');click(page,'Contas');next_(page);page.wait_for_function('document.querySelector("video").readyState>=2');check(page.locator('video').is_visible(),'result local video decoded');check(page.locator('[data-testid=cta]').is_visible(),'CTA with actual media')
 check(page.evaluate('document.fonts.check("16px Inter")'),'bundled Inter available');page.screenshot(path=str(out/'media-fixture-desktop.png'),full_page=True)
 (aux/'invalid.mp4').write_text('not a video');fixture['steps'][0]['media']['src']='invalid.mp4';(aux/'fixture-error.json').write_text(json.dumps(fixture));subprocess.run([sys.executable,str(skill/'scripts/build_quiz.py'),str(aux/'fixture-error.json'),'--out',str(aux/'error')],check=True,stdout=subprocess.DEVNULL);page.goto((aux/'error/index.html').as_uri());page.get_by_text('O vídeo não carregou. Leia a versão em texto abaixo.',exact=True).wait_for();check(True,'broken video honest fallback');next_(page);check(page.get_by_role('heading',name='O que mais dificulta encontrar seus documentos?',exact=True).is_visible(),'broken video does not block progression')
 # Refresh evidence after final font/validation changes, then verify the narrow layout.
 page.set_viewport_size({'width':320,'height':740});org(page,'Os assuntos estão misturados','Uso várias caixas');nooverflow(page,'320px final page no overflow');page.evaluate('document.fonts.ready');check(page.evaluate('document.fonts.check("16px Inter")'),'320px Inter loaded');page.screenshot(path=str(out/'org-320-final.png'),full_page=True)
 page.set_viewport_size({'width':1365,'height':900});org(page,'Esqueço em qual pasta guardei','Uso poucas pastas',capture=True);page.screenshot(path=str(out/'org-1365.png'),full_page=True);lib(page,'Encontrar títulos já registrados');page.screenshot(path=str(out/'biblioteca-1365.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});org(page,'Esqueço em qual pasta guardei','Uso poucas pastas',capture=True);page.screenshot(path=str(out/'org-390.png'),full_page=True);lib(page,'Encontrar títulos já registrados');page.screenshot(path=str(out/'biblioteca-390.png'),full_page=True)
 check(not requests,'no external requests');check(not errors,'no browser page errors')
 ctx.close();browser.close()
(out/'resultados.json').write_text(json.dumps(dict(passed=len(results),cases=results,external_requests=requests,page_errors=errors),ensure_ascii=False,indent=2)+'\n')
(out/'testes.md').write_text('# Testes reais de navegador\n\nChromium headless via Python Playwright. Duas rotas e dois nichos fictícios. Sem transmissão externa.\n\n'+f'{len(results)} verificações aprovadas. Organização: 54 combinações discretas; biblioteca: 18 combinações discretas. Números e textos por fronteiras/classes, sem alegação de exaustão. Desktop 1365x900; celular 390x844.\n\n'+'\n'.join('- '+x for x in results)+'\n\nLimites: os vídeos dos exercícios não foram produzidos e aparecem como ausentes com texto alternativo. Checkout e agenda são destinos locais. Nenhum backend foi implementado. Nenhuma compra, reserva, lead ou mensagem enviados.\n')
print(json.dumps(dict(passed=len(results),external_requests=requests,page_errors=errors)))

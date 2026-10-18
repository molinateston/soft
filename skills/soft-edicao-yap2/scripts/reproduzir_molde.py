from pathlib import Path
import json,hashlib,os,sys
p=json.loads((Path(__file__).resolve().parents[1]/'references/perfil-tipografico.json').read_text())
# Os caminhos do perfil sao relativos a pasta do molde aprovado. Informe a pasta do molde (ou a pasta que contem
# a pasta "source" do perfil) no primeiro argumento ou em YAP_MOLDES_DIR.
base=sys.argv[1] if len(sys.argv)>1 else os.environ.get('YAP_MOLDES_DIR','')
if not base:
 sys.exit(f"Informe a pasta do molde aprovado ({p.get('source','')}): python3 scripts/reproduzir_molde.py <pasta> ou YAP_MOLDES_DIR=<pasta>. Sem ela os arquivos e os SHA256 do perfil nao sao conferidos.")
molde=Path(base).expanduser()
if (molde/p.get('source','')).is_dir() and p.get('source'): molde=molde/p['source']
for name,expected in (p['font_files'] | p.get('source_files',{})).items():
 f=molde/name
 assert f.is_file(),f'Arquivo ausente: {f}'
 assert hashlib.sha256(f.read_bytes()).hexdigest()==expected,f'Arquivo alterado: {f}'
print(json.dumps(p,ensure_ascii=False,indent=2))

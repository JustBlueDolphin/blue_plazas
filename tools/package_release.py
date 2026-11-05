"""Build separate main-MLO and opt-in companion archives; no vendor data."""
from pathlib import Path
import hashlib,json,re,zipfile
from resource_layout import organize

ROOT=Path(__file__).resolve().parents[1]
version=re.search(r"^version\s+'([^']+)'",(ROOT/'fxmanifest.lua').read_text(),re.M)[1]
assert organize(ROOT)['moved']==0,'Organize stream/ before packaging'
OUT=ROOT/'dist';OUT.mkdir(exist_ok=True)

def archive(name,root_name,files):
    path=OUT/name
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for file,relative in sorted(files,key=lambda x:str(x[1])):
            z.write(file,root_name+'/'+relative.as_posix())
    return {'file':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}

def included(p):return p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'
main=[]
for name in ('README.md','TESTING.md','fxmanifest.lua'):main.append((ROOT/name,Path(name)))
for folder in ('stream','audio','docs','tools','integration'):
    main.extend((p,p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*') if included(p))
companion=ROOT/'optional/blue_plazas_doortuning'
reports=[archive(f'blue_plazas-v{version}.zip','blue_plazas',main),
         archive(f'blue_plazas_doortuning-v{version}.zip','blue_plazas_doortuning',[(p,p.relative_to(companion)) for p in companion.rglob('*') if included(p)])]
(OUT/'SHA256SUMS.txt').write_text(''.join(x['sha256']+'  '+x['file']+'\n' for x in reports))
(OUT/'package_report.json').write_text(json.dumps({'version':version,'packages':reports,'runtime_test':'pending'},indent=2))
print(json.dumps(reports,indent=2))

"""Organize the plaza's stream directory without changing asset names or bytes.

Usage: python tools/resource_layout.py <resource-directory> [--apply]
Default: validate and show planned moves. Close the server before --apply.
"""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,os

def relative_asset_path(name):
    if Path(name).name!=name:raise ValueError('Expected an asset basename: '+name)
    if name=='_manifest.ymf':return Path(name)
    unit=re.match(r'^(bp_dp\d{2})(?:[_.])',name)
    if unit and Path(name).suffix in {'.ydr','.ybn','.ymap'}:
        return Path('interiors')/unit[1]/name
    if name in {'bp_delperro.ytyp','bp_interior.ytd','bp_shop_door.ydr'}:
        return Path('shared')/name
    if re.fullmatch(r'\d+\.ymt',name):return Path('audio')/name
    if name.startswith('hei_sm_occl_') and name.endswith('.ymap'):
        return Path('occlusion')/name
    if name.startswith(('sm_','hi@sm_')):
        folder={'.ydr':'models','.ydd':'lod','.ybn':'collision'}.get(Path(name).suffix)
        if folder:return Path('exterior')/folder/name
    raise ValueError('Unclassified asset; assign its folder explicitly: '+name)

def index_stream(stream):
    result={}
    for p in sorted(Path(stream).rglob('*')):
        if not p.is_file():continue
        key=p.name.lower()
        if key in result:raise ValueError(f'Duplicate streamed basename: {result[key]} and {p}')
        result[key]=p
    return result

def fingerprints(stream):
    return {n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in index_stream(stream).items()}

def organize(resource,apply=False):
    root=Path(resource).resolve();stream=root/'stream'
    assert (root/'fxmanifest.lua').is_file() and stream.is_dir(),root
    before=fingerprints(stream);files=index_stream(stream);moves=[]
    # Resolve and check every target before the first filesystem change.
    for name,src in files.items():
        dest=stream/relative_asset_path(src.name)
        assert src.resolve().is_relative_to(stream.resolve()) and dest.resolve().is_relative_to(stream.resolve())
        if src!=dest:
            assert not dest.exists(),dest
            moves.append((src,dest))
    if apply:
        for src,dest in moves:
            dest.parent.mkdir(parents=True,exist_ok=True);src.rename(dest)
        assert fingerprints(stream)==before,'Asset content changed during organization'
    return {'asset_count':len(files),'moved':len(moves),'applied':apply,
            'moves':[{ 'from':str(a.relative_to(root)), 'to':str(b.relative_to(root))} for a,b in moves]}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('resource',type=Path);parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    if args.apply and os.name=='nt':
        status=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match 'FiveM|GTAProcess|FXServer' }).Count"],capture_output=True,text=True,check=True)
        if status.stdout.strip()!='0':raise SystemExit('Close FiveM and FXServer before moving streamed files.')
    print(json.dumps(organize(args.resource,args.apply),indent=2))

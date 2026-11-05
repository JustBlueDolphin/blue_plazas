"""Add the plaza's conservative door profile to the server's existing tuning file.

Stages by default. Never creates another gta5.meta replacement or compiles YMT.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,copy,hashlib,json,os,re,subprocess,xml.etree.ElementTree as E

PROFILE='bp_shop_standard'
MODEL='bp_shop_door'
BASE='DefaultStandard'

def normalized(node):
    return node.tag,dict(node.attrib),(node.text or '').strip(),[normalized(c) for c in node]

def matching(parent,field,value):
    return [n for n in parent.findall('Item') if (n.findtext(field) or '').casefold()==value.casefold()]

def validate(root):
    assert root.tag=='CDoorTuningFile','Expected readable CDoorTuningFile XML'
    profiles=root.find('NamedTuningArray');models=root.find('ModelToTuneMapping')
    assert profiles is not None and models is not None,'Missing tuning arrays'
    names=[(n.findtext('Name') or '').casefold() for n in profiles]
    assert all(names) and len(names)==len(set(names)),'Duplicate/empty tuning profile name'
    for n in models:
        assert (n.findtext('ModelName') or '').strip(),'Empty door model name'
        assert (n.findtext('TuningName') or '').casefold() in names,'Unresolved tuning reference'
    assert len(matching(profiles,'Name',PROFILE))<=1,'Duplicate custom profile'
    assert len(matching(models,'ModelName',MODEL))<=1,'Duplicate custom mapping'
    return profiles,models

def merge(data):
    root=E.fromstring(data);profiles,models=validate(root)
    baseline=matching(profiles,'Name',BASE)
    assert len(baseline)==1,'Missing unique DefaultStandard baseline'
    profile=copy.deepcopy(baseline[0]);profile.find('Name').text=PROFILE;profile.tail=None
    mapping=E.Element('Item');E.SubElement(mapping,'ModelName').text=MODEL;E.SubElement(mapping,'TuningName').text=PROFILE
    additions=[]
    for parent,field,key,desired,closing in ((profiles,'Name',PROFILE,profile,b'</NamedTuningArray>'),
                                           (models,'ModelName',MODEL,mapping,b'</ModelToTuneMapping>')):
        current=matching(parent,field,key)
        if current:
            assert normalized(current[0])==normalized(desired),'Existing custom entry differs; review instead of overwriting: '+key
        else:
            assert data.count(closing)==1,'Ambiguous XML closing tag'
            E.indent(desired,space='  ',level=2)
            block=E.tostring(desired,encoding='utf-8')
            newline=b'\r\n' if b'\r\n' in data else b'\n'
            block=block.replace(b'\n',newline)
            additions.append((data.index(closing),b'  '+block+newline+b'  '))
    result=data
    for pos,block in sorted(additions,reverse=True):result=result[:pos]+block+result[pos:]
    merged=E.fromstring(result);validate(merged)
    # Removing only newly inserted entries must reconstruct the original structure.
    check=copy.deepcopy(merged)
    for tag,field,key in [('NamedTuningArray','Name',PROFILE),('ModelToTuneMapping','ModelName',MODEL)]:
        if not matching(root.find(tag),field,key):
            parent=check.find(tag);parent.remove(matching(parent,field,key)[0])
    assert normalized(check)==normalized(root),'An unrelated entry changed'
    # Existing source bytes, comments and formatting are preserved exactly.
    undo=result
    offset=0
    for pos,block in sorted(additions):
        at=pos+offset;assert undo[at:at+len(block)]==block
        # Undo from last to first below; offset here accounts for earlier insertions.
        offset+=len(block)
    offset=sum(len(block) for _,block in additions)
    for pos,block in sorted(additions,reverse=True):
        offset-=len(block);at=pos+offset;undo=undo[:at]+undo[at+len(block):]
    assert undo==data,'Source bytes were not preserved'
    duplicates={}
    for n in models:
        name=n.findtext('ModelName');duplicates[name]=duplicates.get(name,0)+1
    return result,{'added_entries':len(additions),'profile':PROFILE,'model':MODEL,
                  'existing_profiles_preserved':len(profiles),'existing_mappings_preserved':len(models),
                  'existing_duplicate_model_names':[n for n,count in duplicates.items() if count>1],
                  'unrelated_entries_unchanged':True}

def check_loader(resource):
    manifest=(resource/'fxmanifest.lua').read_text(encoding='utf-8-sig')
    assert re.search(r"replace_level_meta\s*['\"]gta5['\"]",manifest),'No existing gta5 level-meta loader'
    for name in ('gta5.meta','doortuning.ymt'):
        assert re.search(r"['\"]"+re.escape(name)+r"['\"]",manifest),'Loader manifest missing '+name
    meta=(resource/'gta5.meta').read_bytes()
    # Some GTA metadata uses xi:include without declaring that namespace.
    root=E.fromstring(meta.replace(b'<xi:include',b'<include').replace(b'</xi:include',b'</include'))
    paths=[n.findtext('filename') for n in root.iter('Item') if n.findtext('fileType')=='DOOR_TUNING_FILE']
    assert paths==['resources:/'+resource.name+'/doortuning'],('Unexpected central tuning path',paths)
    return paths[0]

def offline_guard():
    assert os.name=='nt','Automatic installation is Windows-only; stage and install offline manually on other platforms.'
    result=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match 'FiveM|GTAProcess|FXServer' }).Count"],capture_output=True,text=True,check=True)
    assert result.stdout.strip()=='0','Close FiveM and FXServer before installing level metadata.'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resource',required=True,type=Path,help='Existing central loader, e.g. cfx-gabz-mapdata')
    parser.add_argument('--output',required=True,type=Path,help='Staged readable doortuning.ymt outside the live resource')
    parser.add_argument('--install',action='store_true');parser.add_argument('--backup-dir',type=Path)
    args=parser.parse_args();resource=args.resource.resolve();target=resource/'doortuning.ymt';output=args.output.resolve()
    assert not output.is_relative_to(resource),'Stage outside the live resource'
    loader=check_loader(resource);original=target.read_bytes();merged,report=merge(original)
    assert merge(merged)[0]==merged,'Merge must be idempotent'
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(merged)
    report.update({'loader':loader,'staged_file':str(output),'installed':False,
        'source_sha256':hashlib.sha256(original).hexdigest(),'merged_sha256':hashlib.sha256(merged).hexdigest()})
    if args.install:
        offline_guard();assert args.backup_dir,'--backup-dir is required for installation'
        backup_dir=args.backup_dir.resolve();assert not backup_dir.is_relative_to(resource),'Back up outside the resource'
        backup_dir.mkdir(parents=True,exist_ok=True)
        backup=backup_dir/('doortuning_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')+'.ymt')
        backup.write_bytes(original);assert target.read_bytes()==original,'Central tuning changed while staging'
        try:
            target.write_bytes(merged);assert target.read_bytes()==merged
        except BaseException:
            target.write_bytes(original);raise
        report.update({'installed':True,'backup':str(backup),'activation':'Full server start and fresh client connection required'})
    output.with_suffix('.report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

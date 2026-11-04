"""Apply the author's requested attribution refresh to the frozen release input.

The verified firmware workers remain unchanged. Historical inputs are retained;
current install/download/source artifacts receive the new author credit.
"""
import hashlib,io,json,re,subprocess,zipfile
from pathlib import Path
AUTHOR='1010B3rika'
OLD_ELF='3e290ba158f06f8048c312d6b3e2e415f2118ccb9c74de0decb2ccd1037539ea'
TEXT={'.txt','.md','.json','.cs','.c','.h','.py','.ps1','.cmd','.bat','.html','.js','.css','.iss','.yml','.yaml'}
def renamed(value):
    value=re.sub(r'(?i)https://github.com/tenten1824/', 'https://github.com/1010b3rika/',value)
    return re.sub(r'(?i)tenten1824',AUTHOR,value)
def refresh(package,repository):
    package=Path(package);repository=Path(repository)
    manifest=json.loads((repository/'release.json').read_text(encoding='utf-8'))
    native=(repository/manifest['payload_file']).read_bytes();new_sha=hashlib.sha256(native).hexdigest()
    assert new_sha==manifest['files'][manifest['payload_file']]['sha256']
    def change(name,data,depth=0):
        if name.lower().endswith('.elf') and hashlib.sha256(data).hexdigest()==OLD_ELF:return native
        if name.lower().endswith('.zip'):
            if depth>12:raise ValueError('Unexpected nested source archive depth')
            target=io.BytesIO()
            with zipfile.ZipFile(io.BytesIO(data)) as old,zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as new:
                for entry in old.infolist():new.writestr(entry,change(entry.filename,old.read(entry.filename),depth+1) if not entry.is_dir() else b'')
            return target.getvalue()
        if Path(name).suffix.lower() in TEXT:
            try:value=data.decode('utf-8')
            except UnicodeError:return data
            return renamed(value).replace(OLD_ELF,new_sha).encode('utf-8')
        return data
    for p in package.rglob('*'):
        if p.is_file():
            old=p.read_bytes();new=change(p.name,old)
            if new!=old:p.write_bytes(new)
    (package/manifest['payload_file']).write_bytes(native)
    # Recompile the public installed launcher; no portable EXE is published.
    source=package/'Source.zip'
    with zipfile.ZipFile(source) as z:
        candidates=[n for n in z.namelist() if n.endswith('launcher/HonchoLauncher.cs')]
        assert len(candidates)==1,candidates
        code=z.read(candidates[0])
    work=package.parent/'credit-build';work.mkdir(exist_ok=True)
    cs=work/'HonchoLauncher.cs';cs.write_bytes(code)
    csc=Path('C:/Windows/Microsoft.NET/Framework64/v4.0.30319/csc.exe')
    args=[str(csc),'/nologo','/target:winexe','/optimize+','/warnaserror+','/codepage:65001','/win32icon:'+str(package/'assets/gwen.ico')]
    args += ['/reference:'+n+'.dll' for n in ['System.Windows.Forms','System.Drawing','System.Web.Extensions','System.IO.Compression','System.IO.Compression.FileSystem']]
    subprocess.run([*args,'/out:'+str(package/manifest['pc_launcher']),str(cs)],check=True)
    proof=dict(author=AUTHOR,developer=AUTHOR,change='Attribution-only rebuild',elf_sha256=new_sha,baseline_elf_sha256=OLD_ELF,firmware_workers_unchanged=True,hardware_retested=False,baseline_verified_firmwares=['7.01','10.01','13.20 Pro','13.60'])
    (package/'GWEN-VERIFICATION.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Attribution refreshed in runtime, compiled launcher, native metadata and complete nested source archives.',flush=True)

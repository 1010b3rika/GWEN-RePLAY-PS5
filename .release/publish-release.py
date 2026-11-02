"""Assemble and publish GWEN's audited v0.9.0 runtime. By tenten1824."""
import argparse,hashlib,json,os,shutil,subprocess,time,urllib.request,zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--wheel-cache',type=Path);p.add_argument('--docs-root',type=Path);p.add_argument('--no-publish',action='store_true');a=p.parse_args()
w=Path(__file__).resolve().parent;out=w/'build';out.mkdir(exist_ok=True);dist=out/'dist';dist.mkdir(exist_ok=True)
sha=lambda data:hashlib.sha256(data).hexdigest()
manifest=json.loads((w/'seed.json').read_text());parts=[]
for info in manifest['parts']:
    body=(w/'seed'/info['path']).read_bytes();assert len(body)==info['bytes'] and sha(body)==info['sha256'];parts.append(body)
seed=b''.join(parts);assert len(seed)==manifest['bytes'] and sha(seed)==manifest['sha256']
(out/'release-seed.zip').write_bytes(seed)
package=out/'GWEN_RePLAY_v0.9.0_PS5_MultiFirmware';package.mkdir(exist_ok=True)
with zipfile.ZipFile(out/'release-seed.zip') as z:
    for name in z.namelist():
        target=(package/name).resolve();assert target.is_relative_to(package.resolve())
    z.extractall(package)
docs=a.docs_root or w.parent
for name in ('README.md','CREDITS.txt','RELEASE-NOTES.md','release.json','NOTICE.txt','READ-ME-FIRST.txt'):
    if (docs/name).is_file():shutil.copy2(docs/name,package/name)
# Include current acknowledgements in the source download as well.
source_archive=package/'Source.zip';pending=package/'Source.updated.zip'
with zipfile.ZipFile(source_archive) as old,zipfile.ZipFile(pending,'w',zipfile.ZIP_DEFLATED) as new:
    for info in old.infolist():
        if info.filename not in ('README.md','CREDITS.txt','NOTICE.txt','installer/installer.iss'):new.writestr(info,old.read(info.filename))
    for name in ('README.md','CREDITS.txt','NOTICE.txt'):new.write(package/name,name)
    new.write(w/'installer.iss','installer/installer.iss')
os.replace(pending,source_archive)
m=json.loads((package/'release.json').read_text());native=package/m['payload_file'];assert sha(native.read_bytes())==manifest['elf_sha256']==m['files'][m['payload_file']]['sha256']
assert m['author']==m['developer']=='tenten1824' and m['firmware_verified']==['7.01','10.01','13.20','13.60']
wheels=package/'Cloud/wheels';wheels.mkdir(exist_ok=True)
def download(info):
    cached=a.wheel_cache/info['filename'] if a.wheel_cache else None
    if cached and cached.is_file():body=cached.read_bytes()
    else:
        for attempt in range(3):
            try:
                req=urllib.request.Request('https://pypi.org/pypi/'+info['project']+'/'+info['version']+'/json',headers={'User-Agent':'GWEN-RePLAY-release/0.9.0'})
                with urllib.request.urlopen(req,timeout=30) as f:metadata=json.load(f)
                item=next(item for item in metadata['urls'] if item['filename']==info['filename'] and item['digests']['sha256']==info['sha256'])
                assert item['url'].startswith('https://files.pythonhosted.org/')
                with urllib.request.urlopen(item['url'],timeout=90) as f:body=f.read()
                break
            except Exception:
                if attempt==2:raise
                time.sleep(2)
    assert sha(body)==info['sha256'],info['filename'];(wheels/info['filename']).write_bytes(body)
with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(download,json.loads((w/'wheels.json').read_text())))
for label,exe in [('regular',package/m['pc_launcher'])]:
    receipt=out/(label+'-check.json');subprocess.run([str(exe.resolve()),'--check',str(receipt.resolve())],check=True)
    checked=json.loads(receipt.read_text());assert checked['ok'] and checked['sha256']==manifest['elf_sha256']
compiler=Path('C:/Program Files (x86)/Inno Setup 6/ISCC.exe')
if not compiler.is_file():
    found=shutil.which('iscc.exe');assert found,'Inno Setup compiler unavailable';compiler=Path(found)
iss=out/'installer.iss';iss.write_text((w/'installer.iss').read_text(encoding='utf-8-sig'),encoding='utf-8-sig')
subprocess.run([str(compiler),'/Qp','/DPackageDir='+str(package.resolve()),'/DDistDir='+str(dist.resolve()),str(iss.resolve())],check=True)
setup=dist/'GWEN-RePLAY-PS5-Setup.exe';assert setup.is_file()
# Exercise a genuine install/uninstall in an isolated runner-temp directory.
import tempfile,uuid
test=Path(tempfile.gettempdir())/('GWEN-Installer-Check-'+uuid.uuid4().hex)
subprocess.run([str(setup.resolve()),'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/NOICONS','/DIR='+str(test)],check=True,timeout=180)
assert sha((test/m['payload_file']).read_bytes())==manifest['elf_sha256']
check=out/'installed-check.json';subprocess.run([str((test/m['pc_launcher']).resolve()),'--check',str(check.resolve())],check=True)
assert json.loads(check.read_text())['sha256']==manifest['elf_sha256']
subprocess.run([str((test/'unins000.exe').resolve()),'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART'],check=True,timeout=120)
assert not (test/m['pc_launcher']).exists(),'Installer uninstall check failed'
archive=dist/'GWEN_RePLAY_v0.9.0_PS5_MultiFirmware.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    z.write(setup,Path(package.name)/setup.name)
    for name in ['Source.zip',m['payload_file'],'CREDITS.txt','NOTICE.txt','LICENSE','README.md','READ-ME-FIRST.txt','RELEASE-NOTES.md','GWEN-VERIFICATION.json']:
        z.write(package/name,Path(package.name)/name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert sha(z.read(package.name+'/'+m['payload_file']))==manifest['elf_sha256']
    assert not any(any(value in name.lower() for value in ('private-inputs','library.sqlite','.venv/','library-location.txt')) for name in z.namelist())
for source,target in [(native,'GWEN-RePLAY-PS5.elf'),(package/'Source.zip','Source.zip'),(package/'CREDITS.txt','CREDITS.txt'),(package/'NOTICE.txt','NOTICE.txt'),(package/'README.md','INSTALL-AND-USE.md'),(package/'GWEN-VERIFICATION.json','GWEN-VERIFICATION.json')]:shutil.copy2(source,dist/target)
files=sorted(f for f in dist.iterdir() if f.is_file() and f.name!='SHA256SUMS.txt' and 'portable' not in f.name.lower())
assert not any('portable' in f.name.lower() for f in files)
(dist/'SHA256SUMS.txt').write_text(''.join(sha(f.read_bytes())+'  '+f.name+'\n' for f in files),encoding='utf-8');files.append(dist/'SHA256SUMS.txt')
print('Validated release assets:',', '.join(f.name for f in files),flush=True)
if not a.no_publish:
    target=os.environ['GITHUB_SHA'];repo=os.environ['GITHUB_REPOSITORY']
    assert repo=='Tenten1824/GWEN-RePLAY-PS5'
    subprocess.run(['gh','release','create','v0.9.0',*[str(f) for f in files],'--repo',repo,'--target',target,'--title','GWEN ▶ RePLAY™ PS5 — v0.9.0','--notes-file',str(package/'RELEASE-NOTES.md'),'--latest'],check=True)

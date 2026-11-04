"""Build the public installed app's private Python runtime. By 1010B3rika.

No Python installation, pip, PATH changes, or downloads are needed on users' PCs.
Build on Windows with CPython 3.12 x64 and the hash-verified release wheels.
"""
import hashlib,json,os,shutil,struct,subprocess,sys,zipfile
from pathlib import Path

def assemble(package,helper_root):
    package=Path(package);helper_root=Path(helper_root)
    assert sys.version_info[:2]==(3,12) and struct.calcsize('P')==8 and os.name=='nt'
    base=Path(sys.base_prefix);runtime=package/'Python';runtime.mkdir(exist_ok=True)
    for name in ['python.exe','pythonw.exe','python3.dll','python312.dll','vcruntime140.dll','vcruntime140_1.dll','LICENSE.txt']:
        shutil.copy2(base/name,runtime/name)
    with zipfile.ZipFile(runtime/'python312.zip','w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted((base/'Lib').rglob('*')):
            rel=f.relative_to(base/'Lib')
            if f.is_file() and rel.parts[0] not in ('site-packages','test','tkinter','idlelib','ensurepip','turtledemo') and '__pycache__' not in rel.parts and f.suffix!='.pyc':z.write(f,rel.as_posix())
    for f in (base/'DLLs').iterdir():
        if f.is_file() and f.suffix.lower() in ('.pyd','.dll'):
            (runtime/'DLLs').mkdir(exist_ok=True);shutil.copy2(f,runtime/'DLLs'/f.name)
    (runtime/'python312._pth').write_text('python312.zip\nDLLs\nLib/site-packages\n.\n../Cloud\nimport site\n',encoding='ascii')
    deps=runtime/'Lib/site-packages';deps.mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,'-m','pip','install','--disable-pip-version-check','--no-index','--find-links',str(package/'Cloud/wheels'),'--target',str(deps),'-r',str(package/'Cloud/requirements.txt')],check=True)
    # Always use this isolated bundled interpreter, never a Store alias, developer
    # cache, system Python, virtual environment, or user's PYTHONPATH.
    ps=package/'Start-Cloud-Sync.ps1';code=ps.read_text(encoding='utf-8-sig')
    start=code.index('    $cached=');end=code.index('    if($SetupOnly)',start)
    code=code[:start]+'''    $python=Join-Path $PSScriptRoot 'Python\\python.exe'
    if(-not (Test-Path -LiteralPath $python)){throw 'Bundled runtime missing. Reinstall the complete GWEN package.'}
    $probe=Invoke-GwenPython -Executable $python -Arguments @('-c','import flask,waitress,argon2,boto3,requests,imageio_ffmpeg,ssl,sqlite3')
    if($probe.ExitCode -ne 0){throw 'Bundled runtime check failed. See CLOUD-SETUP.log; reinstall GWEN.'}
'''+code[end:]
    ps.write_text(code,encoding='utf-8-sig')
    # The smoke check starts the real library server with no console connections.
    run=package/'Cloud/run_sync.py';code=run.read_text(encoding='utf-8')
    code=code.replace("    p.add_argument('--once',action='store_true')","    p.add_argument('--library-only',action='store_true',help='Run the local library without contacting consoles')\n    p.add_argument('--once',action='store_true')")
    code=code.replace("    try: repository=start_repository(","    try: repository=None if a.library_only else start_repository(")
    code=code.replace("        consoles.register(db,'honcho-local-library',a.ps5,a.firmware,a.name)","        if not a.library_only: consoles.register(db,'honcho-local-library',a.ps5,a.firmware,a.name)")
    code=code.replace("    bridge=SharedSync(a.data,url=f'http://127.0.0.1:{a.port}',primary=legacy_primary)","    bridge=None if a.library_only else SharedSync(a.data,url=f'http://127.0.0.1:{a.port}',primary=legacy_primary)")
    code=code.replace("            print(json.dumps(bridge.once()),flush=True)","            if bridge: print(json.dumps(bridge.once()),flush=True)")
    code=code.replace("        bridge.close(); service.close(); lock.close()","        if bridge: bridge.close()\n        service.close(); lock.close()")
    run.write_text(code,encoding='utf-8')
    with zipfile.ZipFile(package/'Source.zip') as z:
        name=next(n for n in z.namelist() if n.endswith('launcher/HonchoLauncher.cs'));cs=z.read(name).decode('utf-8-sig')
    cs=cs.replace('cloud_script=File.Exists(Path.Combine(Root,"Start-Cloud-Sync.ps1"))','cloud_script=File.Exists(Path.Combine(Root,"Start-Cloud-Sync.ps1")),bundled_python=File.Exists(Path.Combine(Root,"Python\\\\python.exe"))')
    begin=cs.index('        string python=Path.Combine(Root,"Cloud\\\\.venv\\\\Scripts\\\\python.exe");')
    end=cs.index('        var info=new ProcessStartInfo(python);',begin)
    cs=cs[:begin]+'''        string python=Path.Combine(Root,"Python\\\\python.exe");
        if(!File.Exists(python))throw new IOException("Bundled runtime missing. Reinstall GWEN.");
'''+cs[end:]
    cs=cs.replace('throw new IOException("Cloud could not start. See CLOUD-START.log for details.");','throw new IOException("Local library could not start. "+(output.IsCompleted?output.Result.Trim():"See CLOUD-START.log for details."));')
    cs=cs.replace('or use the portable EXE.','reinstall GWEN.')
    cs=cs.replace('AssemblyVersion("0.9.0.0")','AssemblyVersion("0.9.2.0")').replace('AssemblyFileVersion("0.9.0.0")','AssemblyFileVersion("0.9.2.0")')
    build=package.parent/'bundled-launcher-build';build.mkdir(exist_ok=True);source=build/'HonchoLauncher.cs';source.write_text(cs,encoding='utf-8')
    manifest=json.loads((package/'release.json').read_text(encoding='utf-8'))
    compiler=Path('C:/Windows/Microsoft.NET/Framework64/v4.0.30319/csc.exe')
    subprocess.run([str(compiler),'/nologo','/target:winexe','/optimize+','/warnaserror+','/codepage:65001','/win32icon:'+str(package/'assets/gwen.ico'),*['/reference:'+n+'.dll' for n in ['System.Windows.Forms','System.Drawing','System.Web.Extensions','System.IO.Compression','System.IO.Compression.FileSystem']],'/out:'+str(package/manifest['pc_launcher']),str(source)],check=True)
    updates={name:cs.encode('utf-8'),'Start-Cloud-Sync.ps1':ps.read_bytes(),'Cloud/run_sync.py':run.read_bytes()}
    for f in helper_root.glob('*.py'):updates['installer/'+f.name]=f.read_bytes()
    pending=package/'Source.new.zip'
    with zipfile.ZipFile(package/'Source.zip') as old,zipfile.ZipFile(pending,'w',zipfile.ZIP_DEFLATED) as new:
        for i in old.infolist():
            if i.filename not in updates:new.writestr(i,old.read(i.filename))
        for n,data in updates.items():new.writestr(n,data)
    os.replace(pending,package/'Source.zip')
    (runtime/'RUNTIME-NOTICE.txt').write_text('CPython is redistributed under the Python Software Foundation license; see LICENSE.txt. Dependency licenses are retained in Lib/site-packages. Application developer: 1010B3rika.\n',encoding='utf-8')
    manifest['bundled_python']=True;manifest['python_install_required']=False
    manifest['files'][manifest['pc_launcher']]={'bytes':(package/manifest['pc_launcher']).stat().st_size,'sha256':hashlib.sha256((package/manifest['pc_launcher']).read_bytes()).hexdigest()}
    (package/'release.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Private Python runtime and all dependencies bundled; no user setup required.',flush=True)

if __name__=='__main__':assemble(Path(sys.argv[1]).resolve(),Path(__file__).resolve().parent)

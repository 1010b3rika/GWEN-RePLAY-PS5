"""Exercise installed GWEN without Python on PATH or developer configuration."""
import argparse,json,os,socket,subprocess,tempfile,time,urllib.request
from pathlib import Path

def check(package):
    package=Path(package).resolve();py=package/'Python/python.exe'
    env=os.environ.copy();env['PATH']=str(Path(os.environ['SystemRoot'])/'System32');env['PYTHONHOME']='Z:/not-installed';env['PYTHONPATH']='Z:/not-installed'
    env['PYTHONUTF8']='1';env['PYTHONIOENCODING']='utf-8'
    with tempfile.TemporaryDirectory(prefix='GWEN-clean-start-') as tmp:
        tmp=Path(tmp);env['USERPROFILE']=str(tmp/'empty-profile');env['LOCALAPPDATA']=str(tmp/'appdata');Path(env['LOCALAPPDATA']).mkdir()
        subprocess.run([str(py),'-c','import sys,flask,waitress,argon2,boto3,requests,ssl,sqlite3,imageio_ffmpeg; assert sys.flags.isolated; print(sys.executable)'],env=env,check=True,timeout=30)
        ps=Path(os.environ['SystemRoot'])/'System32/WindowsPowerShell/v1.0/powershell.exe'
        setup=subprocess.run([str(ps),'-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(package/'Start-Cloud-Sync.ps1'),'-SetupOnly','-NoReuse'],env=env,capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
        assert setup.returncode==0,(setup.stdout,setup.stderr)
        with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        log=open(tmp/'service.log','w',encoding='utf-8');data=tmp/'library'
        child=subprocess.Popen([str(py),'-u',str(package/'Cloud/run_sync.py'),'--library-only','--data',str(data),'--port',str(port)],env=env,cwd=package,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
            health=None
            for _ in range(100):
                if child.poll() is not None:raise RuntimeError((tmp/'service.log').read_text())
                try:
                    with opener.open(f'http://127.0.0.1:{port}/api/health',timeout=1) as response:health=json.load(response)
                    break
                except OSError:time.sleep(.1)
            assert health and health['multiConsole'],(tmp/'service.log').read_text()
            with opener.open(f'http://127.0.0.1:{port}/',timeout=5) as response:assert response.status==200 and len(response.read())>100
            (data/'stop-sync.request').write_text('smoke-check')
            assert child.wait(timeout=15)==0,(tmp/'service.log').read_text()
        finally:
            if child.poll() is None:child.terminate();child.wait(timeout=10)
            log.close()
    print('PASS: installed library starts, serves gallery and shuts down without system Python, pip, developer cache or console access.',flush=True)

if __name__=='__main__':check(Path(__import__('sys').argv[1]))

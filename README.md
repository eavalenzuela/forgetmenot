# forgetmenot
local looting script in python

05/03/2018: Added ability to exfil files via breaking them into chunks, encoding them in base64, and sending them as GET requests to the specified address. This can take a long time with a large file (though you can change the 'chunk size' from its current 10 lines to something larger if you don't mind very large b64 strings).

Catching the requests with a netcat loop... you could also send it to a web server and extract it from the logs.

![base64_send](https://i.imgur.com/t86UBFf.png)

What the requests looks like:

![get_requests](https://i.imgur.com/8BUyZWn.png)

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

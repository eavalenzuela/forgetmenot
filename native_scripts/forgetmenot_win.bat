@echo off

rem
rem	fogetmenot_win.bat
rem	Windows-only standalone local looter. No client/server funtion.
rem	
rem	Eric Valenzuela, eevn.io
rem	07/03/2017
rem

title forgetmenot_win 

echo "This script does not save on its own. Pipe it to a file to save the output."

hostname

wmic os
wmic product
wmic logicaldisk
wmic netlogin
wmic startup

powershell set-executionpolicy unrestricted
powershell get-ciminstance win32_operatingsystem | FL *

net user
wmic UserAccount get Name
wmic rdaccount

ifconfig
netstat
wmic nicconfig
wmic netuse
wmic share

powershell get-netipconfiguration
arp /a

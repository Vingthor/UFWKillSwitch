# VPN Kill Switch Automator
This project automates the creation of UFW rules from a folder of OVPN files. 
These automated rules act as a kill switch to turn off all Internet connections, 
if a connection to one of the VPN files listed in the folder fails.

Many VPN companies supply downloads of these files. 
## Installation
### STEP 1:
Firstly you should disable IPV6, in the configuration files for both the OS and UFW.
This will ensure no IPv6 traffic is passed through unencrypted.
How to do this may vary from distribution to distribution, 
so it was automated in this script.
 
For Ubuntu:

Add the following lines to ```/etc/sysctl.conf```
```
net.ipv6.conf.all.disable_ipv6=1
net.ipv6.conf.default.disable_ipv6=1
net.ipv6.conf.lo.disable_ipv6=1
```
Add the following to ```/etc/default/ufw```

```
IPV6=no
```
### STEP 2:
Gather the information required to install the kill switch, you will need:
1. Your local subnet (with CIDR notation). This can usually be found with ```ip addr```
2. The device that connects to the Internet. This can also usually be found with ```ip addr```
3. The folder that contains your OVPN files.

### STEP 3:
Run the Kill switch Automator: ```sudo python kill.py subnet device folder```

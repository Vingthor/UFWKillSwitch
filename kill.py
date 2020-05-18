#!/usr/bin/env python

import os
import socket
import argparse
import sys

LOCAL_SUBNET = ""
DEVICE = ""
DIRECTORY = ""
DEV_NULL = ""


def get_options(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description="""
    Generates a UFW Kill Switch for a folder of ovpn files.
    """)
    parser.add_argument("subnet", help="local subnet, e.g. 192.168.1.0/24")
    parser.add_argument("device", help="device that attaches to the internets, such as eth0, eno1")
    parser.add_argument("folder", help="The folder that the files are located in")
    parser.add_argument("-v", "--verbose", dest='verbose', action='store_true', help="Verbose mode.")
    return parser.parse_args(args)


if __name__ == "__main__":
    options = get_options()

    if not options.verbose:
        DEV_NULL = " > /dev/null"

    LOCAL_SUBNET = options.subnet
    DEVICE = options.device
    DIRECTORY = options.folder

    os.system("ufw disable")
    os.system("ufw reset")
    os.system("ufw default deny outgoing" + DEV_NULL)
    os.system("ufw allow out on tun0 from any to any" + DEV_NULL)
    os.system("ufw allow in on tun0 from any to any" + DEV_NULL)
    os.system("ufw allow in to " + LOCAL_SUBNET + DEV_NULL)
    os.system("ufw allow out to " + LOCAL_SUBNET + DEV_NULL)

    for file in os.listdir(DIRECTORY):
        if file.endswith(".ovpn"):
            with open(DIRECTORY + "/" + file) as fp:

                line = fp.readline()
                while line:
                    if "proto " in line:
                        protocol = " " + line.rstrip()
                    if "remote " in line:
                        remote_server = line.split(' ')
                        try:
                            address = remote_server[1]
                            port = remote_server[2].rstrip()
                        except IndexError:
                            print("ERROR: " + file + " is malformed")
                            line = fp.readline()
                            continue

                        resolved_address = ""
                        try:
                            resolved_address = socket.gethostbyname(address)
                        except socket.gaierror:
                            print("Could not resolve: " + address)
                            line = fp.readline()
                            continue

                        if resolved_address == "" or port == "" or protocol == "":
                            print("ERROR: " + file + " is malformed")
                            line = fp.readline()
                            continue

                        os.system('ufw allow out to ' + resolved_address + ' port ' + port + protocol + DEV_NULL)
                        os.system('ufw allow in to ' + resolved_address + ' port ' + port + protocol + DEV_NULL)

                        os.system('ufw allow out on ' + DEVICE + ' from ' + LOCAL_SUBNET + ' to ' + resolved_address +
                                  DEV_NULL)
                        os.system('ufw allow in on ' + DEVICE + ' from ' + resolved_address + ' to ' + LOCAL_SUBNET +
                                  DEV_NULL)
                        resolved_address = ""
                        port = ""
                        protocol = ""
                    line = fp.readline()

    os.system("ufw enable")

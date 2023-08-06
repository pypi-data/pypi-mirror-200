# requires openvpn to be installed on the machine
#   > sudo apt-get update
#   > sudo apt-get install openvpn

import os
import subprocess
import logging
import signal
import threading

########################################################################
# Connect to vpn via bash cmd.
########################################################################
def connect(file): 
    try:
        subprocess.run(f'pkill openvpn'.split())
        subprocess.run(f'openvpn --daemon --config {file}'.split())
    except Exception as e:
        raise VpnConnectError(e)

########################################################################
# Disconnect to vpn via bash cmd.
########################################################################
def disconnect():
    try:
        subprocess.run('pkill openvpn'.split())
    except Exception as e:
        raise VpnDisconnectError(e)

# custom exceptions
class VpnConnectError(Exception): pass
class VpnDisconnectError(Exception): pass
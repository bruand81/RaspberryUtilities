import os
import time
import socket
#from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
from netifaces import AF_INET, AF_INET6, AF_LINK
import netifaces as ni

def pid_is_running(pid):
    try:
        os.kill(pid,0)
    except OSError:
        return
    else:
        return pid

def write_pidfile_or_die(path_to_pidfile):
    if os.path.exists(path_to_pidfile):
        pid = int(open(path_to_pidfile).read())
        if pid_is_running(pid):
            print("Sorry, found a pidfile! Process {0} is still running.".format(pid))
            raise SystemExit
        else:
            os.remove(path_to_pidfile)

    open(path_to_pidfile, 'w').write(str(os.getpid()))
    return path_to_pidfile

def get_host_ip(iface):
    # return socket.gethostbyname(socket.gethostname())
    # return socket.gethostbyname(socket.getfqdn())
    return ni.ifaddresses(iface)[AF_INET][0]['addr']

def check_changed_ip(iface, path_to_ifacefile):
    old_ip=''
    if os.path.exists(path_to_ifacefile):
        old_ip = open(path_to_ifacefile).read()
    ip = get_host_ip(iface)
    if old_ip == ip:
        return True
    else:
        open(path_to_ifacefile, 'w').write(ip)
        return False
    
def send_mail_for_changed_ip(destination, new_ip):
    return True

def get_interface_info():
    interfaces = ni.interfaces()
    print(interfaces)
    for iface in interfaces:
        print(iface)
        try:
            print(ni.ifaddresses(iface)[AF_INET][0]['addr'])
        except KeyError:
            print("No AF_INET")
        print(ni.ifaddresses(iface))
    #print(ni.ifaddresses('en0')[AF_INET][0]['addr'])

if __name__ == '__main__':
    write_pidfile_or_die('/tmp/IPChecker.pid')
    time.sleep(5)
    path_to_ifacefile = '/tmp/IPChecker.oldip'
    iface = 'wlan0'
    check_interval = 5
    print(get_host_ip(iface))
    # print('process {0} finished work!'.format(os.getpid()))
    while(True):
        print(check_changed_ip(iface, path_to_ifacefile))
        time.sleep(check_interval)

import os
import socket
# from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
from netifaces import AF_INET, AF_INET6, AF_LINK
import netifaces as ni
import smtplib
from email.message import EmailMessage

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

def get_host_ips(ifaces):
    ips = dict()
    for iface in ifaces:
        try:
            ips[iface] = get_host_ip(iface)
        except KeyError:
            ips[iface] = 'No ip'
    return ips

def check_changed_ip(iface, path_to_ifacefile):
    old_ip=''
    #print(path_to_ifacefile)
    if os.path.exists(path_to_ifacefile):
        old_ip = open(path_to_ifacefile).read()
    ip = get_host_ip(iface)
    if old_ip == ip:
        return False
    else:
        open(path_to_ifacefile, 'w').write(ip)
        return True

def check_changed_ips(ifaces, base_path_to_iface_file, destination):
    for iface in ifaces:
        path_to_ifacefile = base_path_to_iface_file % iface
        try:
            if check_changed_ip(iface, path_to_ifacefile):
                iface_ip = get_host_ip(iface)
                print('IP for interface %s changed to %s' % (iface, iface_ip))
                send_mail_for_changed_ip(destination, iface_ip, iface)
        except KeyError:
            continue

    
def send_mail_for_changed_ip(destination, new_ip, iface):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        sent_from = 'andrea.bruno@antaresnet.org'
        server.login(sent_from, 'xqsmxbilxhrffouw')
        to = [destination]
        subject = 'IP changed on %s' % socket.getfqdn()
        body = 'New IP assinged to %s is %s.' % (socket.getfqdn(), new_ip)
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = sent_from
        msg['To'] = to

        email_text = """\  
        From: %s  
        To: %s  
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)
        # server.sendmail(sent_from, to, email_text)
        server.send_message(msg)
        server.close()
        print('Email sent!')
        # print(email_text)
        return True
    except Exception as e:
        print('Error in sending mail: %s' % str(e))
        return False

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
    # write_pidfile_or_die('/tmp/IPChecker.pid')
    # time.sleep(5)
    path_to_ifacefile = '/tmp/IPChecker.oldip'
    base_path_to_ifacefile = '/tmp/IPChecker_%s.oldip'
    iface = 'en0'
    ifaces =  ['en0', 'en1', 'en2']
    dest_address = 'andbruno@unisa.it'
    check_interval = 5
    #ips = get_host_ips(ifaces)
    #for ifc in ips:
    #    print("Ip for interface %s is %s"%(ifc, ips[ifc]))
    check_changed_ips(ifaces, base_path_to_ifacefile, dest_address)
    #host_ip = get_host_ip(iface)
    #if not check_changed_ip(iface, path_to_ifacefile):
    #    send_mail_for_changed_ip(dest_address, host_ip)
    #print(host_ip)
    #print(send_mail_for_changed_ip('andbruno@unisa.it', get_host_ip(iface)))
    # print('process {0} finished work!'.format(os.getpid()))
    # while(True):
    #    print(check_changed_ip(iface, path_to_ifacefile))
    #    time.sleep(check_interval)

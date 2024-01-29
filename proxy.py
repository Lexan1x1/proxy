import sys 
import os

def main():
    username="userproxy"
    password_proxy="root"
    os.system("apt-get update")
    os.system("apt-get -y install build-essential libwrap0-dev libpam0g-dev libkrb5-dev libsasl2-dev")
    os.system("wget --no-check-certificate https://ahmetshin.com/static/dante.tgz")
    os.system("tar -xvpzf dante.tgz")
    os.system("apt-get -y install libwrap0 libwrap0-dev")
    os.system("apt-get -y install gcc make")
    os.system("mkdir /home/dante")
    os.system("""cd dante && ./configure --prefix=/home/dante && make && make install""")
    os.system("""
            echo '
            logoutput: stderr
            internal: eth0 port = 1080
            external: eth0
             
            socksmethod: username
            user.privileged: root
            user.unprivileged: nobody
             
            client pass {
                from: 0.0.0.0/0 to: 0.0.0.0/0
                log: error
            }
             
            socks pass {
                from: 0.0.0.0/0 to: 0.0.0.0/0
                command: connect
                log: error
                method: username
            }' > /home/dante/danted.conf
                """)
    os.system("useradd --shell /usr/sbin/nologin -m %s" % username)
    os.system("apt-get -y install ufw")
    os.system("ufw status")
    os.system("ufw allow ssh")
    os.system("ufw allow proto tcp from any to any port 1080")
    os.system("ufw status numbered")
    os.system("""
echo '#!/bin/sh -e
sleep 20
/home/dante/sbin/sockd -f /home/dante/danted.conf -D
exit 0
' > /etc/rc.local
""")
    os.system("chmod +x /etc/rc.local")
    os.system("chmod +x /home/dante/sbin/sockd")
    os.system("/home/dante/sbin/sockd -f /home/dante/danted.conf -D")

if __name__ == "__main__":
    main()

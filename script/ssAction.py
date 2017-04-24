import json
from util.ssh import SSH


ss_file_sample = 'ss.json'
ss_file = '/etc/shadowsocks.json'


class Shadowsocks(object):
    def __init__(self):
        self.ssh = SSH()

    def _ss_install(self):
        self.ssh.execute('pip install shadowsocks')

    def _ss_config(self):
        with open(ss_file_sample, 'r') as f:
            ss_info = json.load(f)
            print 'ss_info=%s' % ss_info
        with open(ss_file, 'w') as wf:
            wf.write(json.dumps(ss_info))

    def _ss_start(self):
        self.ssh.execute('ssserver -c /etc/shadowsocks.json -d start')

    def start_ss_server(self):
        self.ssh.connect('12.212.12.1','root','123')
        self._ss_install()
        self._ss_config()
        self._ss_start()
        self.ssh.close()

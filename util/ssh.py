import paramiko


class SSH(object):
    def __init__(self):
        self.ssh = None

    def connect(self, ip, user, passwd, port=22):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(ip, port, user, passwd, timeout=3)
        except:
            print("ssh connect err.")

    def execute(self, cmd):
        result = ""
        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            result = stdout.read()
        except:
            print("ssh_cmd err.")

        return result

    def close(self):
        try:
            self.ssh.close()
        except:
            print("ssh close err.")

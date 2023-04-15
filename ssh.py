import paramiko, socket, threading

class SSHLogger(paramiko.ServerInterface):
    def init(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED if kind == 'session' else paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == "user" and password == "pass":
            return paramiko.AUTH_SUCCESSFUL
        else:
            print(f"Логин: {username}, пароль: {password}")
            return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'

ssh_host, ssh_port = '31.28.27.75', 22

# Создаем серверный сокет, связываем его с нашим хостом и портом
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((ssh_host, ssh_port))
sock.listen(5)

print(f"Сервер запущен на {ssh_host}:{ssh_port}")

while True:
    client, addr = sock.accept()
    print(f"Подключение из {addr[0]}:{addr[1]}")
    ssh_transport = paramiko.Transport(client)
    ssh_transport.set_gss_host(socket.getfqdn(""))
    ssh_transport.load_server_moduli()
    ssh_transport.add_server_key(paramiko.RSAKey.generate(2048))
    try:
        ssh_transport.start_server(server=SSHLogger())
        print(f"Соединение установлено: {addr[0]}:{addr[1]}")
    except:
        pass

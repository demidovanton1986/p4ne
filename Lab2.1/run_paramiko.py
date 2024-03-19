import paramiko
import time
import re

ssh_conn = paramiko.SSHClient()
ssh_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_conn.connect("10.31.70.209", username="restapi", password="j0sg1280-7@", look_for_keys=False, allow_agent=False)

session = ssh_conn.invoke_shell()
time.sleep(1)
session.send("terminal length 0\n".encode())
time.sleep(1)
session.send("show interface\n".encode())
time.sleep(1)

result = session.recv(65536).decode()

for line in result.split('\n'):
    if m := re.match(r"^([A-Z].+?) is", line):
        print(f'Interface: {m.group(1)}')
    if m := re.match(r"^.+?([0-9]+) packets input, ([0-9]+) bytes", line):
        print(f'Packets/bytes input: {m.group(1)} / {m.group(2)}')
    if m := re.match(r"^.+?([0-9]+) packets output, ([0-9]+) bytes", line):
        print(f'Packets/bytes output: {m.group(1)} / {m.group(2)}')
        print()

ssh_conn.close()

import argparse
import json
from paramiko.client import SSHClient
from paramiko import AutoAddPolicy

with open('secrets.json') as user_file:
  credentials = json.load(user_file)

client = SSHClient()
client.set_missing_host_key_policy(AutoAddPolicy())

client.connect(credentials["domain"], username=credentials["username"], password=credentials["password"])
stdin, stdout, stderr = client.exec_command('ls -l')

stdin.close()
print(stdout.read().decode('utf-8'))
client.close()
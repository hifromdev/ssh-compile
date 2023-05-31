import argparse
import json
from paramiko.client import SSHClient
from paramiko import AutoAddPolicy

# From file_to_compile, its corresponding output file name is generated in file_to_recieve.
#   Ex: main.cpp generates main.o and main.min.cpp generates main.min.o
file_to_compile = "main.cpp"
file_to_recieve = f"{''.join(file_to_compile.split('.')[:-1])}.o"

# Loads virtual machine credentials into dictionary 'credentials'
with open('secrets.json') as secrets:
  credentials = json.load(secrets)

# Create and connect to the SSH connection
client = SSHClient()
client.set_missing_host_key_policy(AutoAddPolicy())
client.connect(credentials["domain"], username=credentials["username"], password=credentials["password"])

###
# Transfer the file to compile, compile said file, and recieve compiled binary.
sftp = client.open_sftp()
sftp.put(file_to_compile, f"/home/{credentials['username']}/{file_to_compile}")

stdin, stdout, stderr = client.exec_command(f'g++ {file_to_compile} -o {file_to_recieve}')
stdin.close()

sftp.get(f"/home/{credentials['username']}/{file_to_recieve}", file_to_recieve)
###

print(stdout.read().decode('utf-8')) # This is not working right now.
client.close()

import asyncio
import sys

def ssh_format(ip_address: str, username: str, password: str, port: int = 22, legacy: bool = True) -> str:
    cmd = f'sshpass -p {password} ssh'
    
    if legacy:
        cmd += ' -oHostKeyAlgorithms=+ssh-dss'
        
    cmd += f' {username}@{ip_address} -p {port}'
    
    return cmd
""" 
    TTY Instead Of PIPE
ip_address = '192.168.56.101'
username = 'msfadmin'
password = 'msfadmin'

cmd = ssh_format(ip_address, username, password)
"""
    
async def anything_but_ssh(cmd: str = 'ls -al /'):    
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    while (result := await proc.stdout.readline()):
        print(result.decode('utf-8'), end="")
 
# entry point
asyncio.run(anything_but_ssh())

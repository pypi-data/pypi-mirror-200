import asyncio
import asyncssh
import logging
import os
import time

from aiofile import AIOFile
from abc import ABC, abstractmethod

"""
class MySSHClient(asyncssh.SSHClient):
    def connection_made(self, conn: asyncssh.SSHClientConnection) -> None:
        print('Connection made to %s.' % conn.get_extra_info('peername')[0])

    def auth_completed(self) -> None:
        print('Authentication successful.')
        
    async def connect_to_virtual_machine(self, host: str, username: str, password: str):
        return asyncssh.connect(host, username=username, password=password, known_hosts=None)
"""

async def file_append(file_location: str, text: str):
    async with AIOFile(file_location, 'a') as file:
        await file.write(text)
        await file.fsync()
        
class AsyncSshMeta(type):
    log_location: str = "/home/freedom/cyber_connections.txt"
    
    @staticmethod
    async def run_client():
        async with asyncssh.connect('192.168.56.101', username='msfadmin', password='msfadmin', known_hosts=None) as conn:
            result = await conn.run('echo "Hello!"', check=True)
            print(result.stdout, end='')
            
    @staticmethod
    def get_time() -> int:
        return int(time.time())
        
    @staticmethod
    def format_message(file_name: str, class_name: str, local_connection: str, foreign_connection: str, username: str, password: str, successful: bool) -> str:
        return f'[{self.get_time()}] file - {file_name}, class/function - {class_name},  local_connection - {local_connection}, foreign_connection - {foreign_connection}, username - {username}, password - {password}, successful - {successful}'
        
    @classmethod
    async def log_class(cls, *args) -> bool:
        try:
            await file_append(cls.log_location, cls.format_message(*args))
            return True
        except:
            return False
    
    async def __new__(mcs, name, bases, dictionary):
        try:
            file_name = dictionary['file_name']
            class_name = dictionary['class_name']
            local_connection = dictionary['local_connection']
            foreign_connection = dictionary['foreign_connection']
            username = dictionary['username']
            password = dictionary['password']
        except Exception as e:
            raise Exception(f"Couldn't parse **kwargs -> {e}")
        try:
            # Other way -> conn, client = await asyncssh.create_connection(MySSHClient, 'localhost')
            mcs.conn = await asyncssh.connect(local_connection, username=username, password=password, known_hosts=None)
            successful = True
        except:
            successful = False
            
        mcs.log_class(file_name, class_name, local_connection, foreign_connection, username, password, successful)
        
        if not successful:
            raise Exception(f"Couldn't connect to {foreign_connection} using the username {username} and password {password}!")

class Frogger:
    log_location: str = os.path.abspath(os.path.dirname(__file__))
    
    def __init__(self, log_location: str = "", log_filename: str = "logged.txt", log_level = logging.INFO, _format: str = '%(asctime)s : %(message)s)':
        self.log_location = log_location if log_location[-1] == '/' else log_location + '/'
        self.log_filename = log_filename
        self.log_level = log_level
        self.format = _format
        
        self.build_logger()
        
    def build_logger(self):
        log_name = f'{self.log_location}{self.log_filename}'
        
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(self.log_level)
        
    @abstractmethod
    def format_message(self, **kwargs):
        pass
        
    def log_entry(self, level: str, need_to_format = False, **kwargs):
        if need_to_format:
            msg = self.format_message(**kwargs)
        else:
            msg = kwargs['msg']
        
        if level == 'debug':
            self.logger.debug(msg)
        elif level == 'info':
            self.logger.info(msg)
        elif level == 'warning':
            self.logger.warning(msg)
        elif level == 'error':
            self.logger.error(msg)
        elif level == 'critical':
            self.logger.critical(msg)
        else:
            raise Exception(f'Level {level} not acceptable for the logger class!')
            
class Cache:
    pass
    
class SQLCache:
    pass
    
class CyberLogger(Frogger, Cache, SQLCache):
    def __init__(self, log_location: str = "", log_filename: str = "logged.txt", log_level = logging.INFO, _format: str = '%(asctime)s - %(message)s):
        super().__init__(log_location, log_filename, log_level, _format)
        
    def format_message(self, **kwargs):
        local_connection = kwargs['local_connection']
        foreign_connection = kwargs['foreign_connection']
        ssh_user = kwargs['ssh_user']
        cmd_input = kwargs['input']
        cmd_response = kwargs['output']
        
        # Cache and SQLCache for terminal history!!! here!!!
        
        return f'local_connection - {local_connection}, foreign_connection - {foreign_connection}, ssh_user - {ssh_user}, cmd - {cmd_input}, response - {cmd_response}'
            
class CyberClient(CyberLogger, metaclass=AsyncSshMeta):
    def __init__(self, local_connection: str, foreign_connection: str, username: str, password: str):
        self.file_name = __file__
        self.class_name = type(self).__name__
        self.local_connection = local_connection
        self.foreign_connection = foreign_connection
        self.username = username
        self.password = password
        
    def run_command(self, cmd: str) -> str | bool:
        try:
            with self.conn:
                result = await conn.run(cmd, check=True)
                response = result.stdout
                
                self.log_entry('info', need_to_format=True, local_connection=self.local_connection, foreign_connection=self.foreign_connection, ssh_user=self.username, cmd=cmd, cmd_response=response)
                
                return response
        except Exception as e:
            self.log_entry('warning', msg="Couldn't run command {cmd} successfully! {e}")        
        
        return False
    

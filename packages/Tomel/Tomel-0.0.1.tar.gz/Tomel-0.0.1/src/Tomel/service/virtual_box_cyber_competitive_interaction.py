import virtualbox as vb

from aiofile import AIOFile

class VBox:
    # Test if bytes!!!
    @staticmethod
    async def screenshot(file_location: str, image: bytes):
        async with AIOFile(file_location, 'wb') as file:
            await file.write(image)
            await file.fsync()
            
    def __init__(self):
        self.vbox = vb.VirtualBox()
        self.logged_in = False
        
    def identify_machines(self) -> list[str]:
        return self.vbox.machines
    
    def launch_session(self, vm):
        # Changed this from -> vb.Session()
        self.session = vm.create_session()
        
    def signed_in(self) -> bool:
        return self.logged_in
        
    def sign_in(self):
        self.logged_in = True
        
    def sign_out(self):
        self.logged_in = False
        
class VbSession(VBox):
    def __init__(self, machine_name: str):
        super().__init__()
        
        self.machine_name = machine_name
        
        if self.machine_name not in self.identify_machines():
            raise Exception(f"Can't find {machine_name}")
        
        self.get_vm()
        self.launch_session(self.vm)
        
    def get_vm(self):
        self.vm = self.vbox.find_machine(self.machine_name)
        
    def launch_gui(self):
        self.gui_process = self.vm.launch_vm_process(self.session, 'gui', '')
        
    def get_gui_screen_size(self) -> tuple[float | int]:
        h, w, *rest_of_args = self.session.console.display.get_screen_resolution(0)
        
        return (h, w)
        
    async def gui_screen_shot(self, save_location: str) -> bool:
        try:
            h, w = self.get_gui_screen_size()
            
            # Need to test to see if bytes!
            png = self.session.console.display.take_screen_shot_to_array(0, h, w, vb.library.BitmapFormat.png)
            
            self.screenshot(save_location, png)
            
            return True
        except Exception as e:
            print(f'Tried to save the screenshot! {e}')
            
        return False
        
    def log_in(self, username: str, password: str) -> bool:
        try:
            self.session_shell = self.session.console.guest.create_session(username, password)
            self.sign_in()
            
            return True
        except Exception as e:
            print(f'Tried to get a guest shell: {e}')
        
        return False
        
    def execute_command(self, cmd: list[str], shell_type: str = '/usr/bin/bash') -> tuple:
        # Returns stdout, stderr as a tuple
        if self.signed_in():
            return tuple(self.session_shell.execute(shell_type, cmd)[1:])

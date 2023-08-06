import multiprocessing as mp
import json
import subprocess
import resource
import os

######################
####  SQL tables  ####
######################
###################
####  Problem  ####
####           #######
####  test_cases  ####
####              #########
####  sample_solution  ####
####                   ###################################
####  RLIMIT_VALUES...CPU_STCK_DATA_RSS_MEMLOCK_VMEM  ####
####                    ##################################
####  NOFILE=0_DEFAULT  ####
############################

def timer(func):
    def total_code_run(*args, **kwargs):
        # Need to do research before finishing this section
        # use resource to set memory and cpu limits for user code
        # RLIMIT_NOFILE -> max number of open file descriptors = 0
        # RLIMIT_RSS -> set max resident size
        # RLIMIT_DATA -> heap bytes
        # RLIMIT_STACK -> stack bytes
        # RLIMIT_CPU -> processor time
        # RLIMIT_MEMLOCK -> maximum address space locked in memory
        # RLIMIT_VMEM -> largest area of mapped memory which the process may occupy
        start = resource.getrusage(resource.RUSAGE_SELF)
        result = func(*args, **kwargs)
        end = resource.getrusage(resource.RUSAGE_SELF)
        
        metrics = {"memory": end.ru_maxrss - start.ru_maxrss, "user_time": end.ru_utime - start.ru_utime, "system_time": end.ru_stime - start.ru_stime} 
        
        return result, metrics
    return total_code_run

class Runner:
            
    def __init__(self, test_case_path: str, code_path: str, answer_case_path: str, nproc: int = os.cpu_count()):
        self.nproc = nproc
        self.test_case_path = test_case_path
        self.answer_case_path = answer_case_path
        self.code_path = code_path

        self.test_case_list = self.extract_file(self.test_case_path)
        self.test_case_length = len(self.test_case_list)

        self.answer_case_list = self.extract_file(answer_case_path)
        self.answer_case_length = len(self.answer_case_list)
        
        if self.test_case_length != self.answer_case_length:
            raise Exception("The test case and answer case files do not match!")
            
    def run(self, cmd: list):
        ret = subprocess.run(cmd, capture_output=True, timeout=5)
        return ret.stdout.decode().strip().split('\n')
            
    def extract_file(self, path: str, delimiter: str = "\n") -> str:
        _list = []

        with open(path) as reader:
            for item in reader.read().strip().split(delimiter):
                _list.append(json.loads(item))
        
        return _list
                   
    def test(self, test_case_idx: int):
        test_case = f'{self.test_case_list[test_case_idx]}'
        answer_case = self.answer_case_list[test_case_idx]
        
        cmd = ["python3", self.code_path, test_case]
        
        answer = False

        try:
            result = json.loads(self.run(cmd)[0])
            if answer_case == result:
                return test_case_idx, True
        except:
            print("Could not run test_case or it run out of time!")
        return test_case_idx, False
        
    # In-case you only need to test 20% or so. Based off of HackerRank
    @timer
    def test_cases(self, test_case_indices: list[int]):
        for test_case_idx in test_case_indices:
            if test_case_idx < 0 or test_case_idx >= self.test_case_length:
                raise Exception("Test case index is out of range!")
        
        results = {}
                    
        with mp.Pool(self.nproc) as pool:
            processes = [pool.apply_async(self.test, args=(idx,)) for idx in test_case_indices]
            
            for p in processes:
                test_case_idx, passed = p.get()
                
                results[test_case_idx] = passed
                
        return results

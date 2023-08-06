import tkinter as tk
from tkinter import ttk

import tkinter.messagebox as messagebox

import tempfile
import os
import subprocess
import sys
import uuid
import time

from Tomel.components.editor_frame import Editor
from Tomel.components.accordion_frame import Accordion
from Tomel.components.rich_text import RichText
from Tomel.components.video_player_frame import TkinterVideoPlayer
from Tomel.service.runner import Runner

from dataclasses import dataclass

@dataclass
class ClickableText:
    problem_number: int
    values: list[int]
    answer: list[int]
    
    def __str__(self):
        return f'Test Case Values: {",".join([str(value) for value in self.values])}\nAnswer Values: {",".join([str(value) for value in self.answer])}'
        
class BulletFrame:
    def __init__(self, root):
        self.labels = []
        self.problems = []
        self.counter = 0
        
        self.bullet_frame = ttk.Frame(root, padding=10)
        
    def add_bullet(self, problem_number, _text, answer, _foreground="green", _font=("Ubuntu", 14)):
        self.labels.append(tk.Label(self.bullet_frame, text=problem_number, cursor="hand2", foreground=_foreground, font=_font))
        
        self.problems.append(ClickableText(problem_number, _text, answer))
        
        self.labels[-1].grid(row=self.counter, column=0)        
        self.labels[-1].bind("<Button-1>", lambda e, i=self.counter: self.open_problem(i))
        
        self.counter += 1
    
    def open_problem(self, bullet_number):
        print(bullet_number)
        messagebox.showinfo(f'{bullet_number}', self.problems[bullet_number])
        
    def set_grid(self, _row: int = 0, _column: int = 0):
        self.bullet_frame.grid(row=_row, column=_column)

class SubmissionInterface:
    def __init__(self, root, information: dict):
        self.cbs = []
        self.information = information
        self.interface_frame = ttk.Frame(root, padding=5)
        self.variables = {}
        
        ##############################
        ####  Editor (Top Right)  ####
        ##############################
        self.restart()
        
        self.first_tab_group()
        self.second_tab_group()
        self.button_group()
        self.accordion_group()
        
        # bound accordion in function
    
    def set_grid(self, _row: int = 0, _column: int = 0):
        self.interface_frame.grid(row=_row, column=_column)
        
    ##################################
    ####  Tab group (Upper Left)  ####
    ##################################
    #####################################################################
    ####  Problem, test cases, solution, link to top user solutions  ####
    #####################################################################
    def first_tab_group(self):
        first_paned_group = ttk.PanedWindow(self.interface_frame)
        first_paned_group.grid(row=0, column=0, pady=(25,5), sticky="nsew")
        
        pane_1 = ttk.Frame(first_paned_group)
        first_paned_group.add(pane_1, weight=3)
        
        notebook = ttk.Notebook(pane_1)
        notebook.grid(row=0, column=0)
        
        tab_1 = ttk.Frame(notebook)
        notebook.add(tab_1, text="Problem Description")
        
        problem_text = RichText(20, tab_1, width=40, height=15)
        problem_text.pack(fill="both", expand=True)
        
        problem_text.insert("end", self.information['problem_description_heading'] + "\n", "h1")
        problem_text.insert("end", self.information['problem_description_heading'])
        
        tab_2 = ttk.Frame(notebook)
        notebook.add(tab_2, text="Test Cases")
        
        testcase_heading = ttk.Label(tab_2, text=self.information['testcase_heading']) 
        bullets = BulletFrame(tab_2)
        
        for problem_number, values in self.information['testcases'].items():
            # Bake in a test case __str__ method -> create a class
            testcase = values['testcase']
            answer = values['answer']
            print(testcase)
            bullets.add_bullet(problem_number, testcase, answer)
        
        testcase_heading.grid(row=0, column=0)
        bullets.set_grid(_row=1, _column=0)
        
    ###################################
    ####  Tab group (Middle Left)  ####
    ###################################
    #####################################################################################
    ####  Metrics on problem, link to real life related topics, experience expected  ####
    #####################################################################################
    def second_tab_group(self):
        second_paned_group = ttk.PanedWindow(self.interface_frame)
        second_paned_group.grid(row=1, column=0, pady=(25,5), sticky="nsew")
        
        pane_2 = ttk.Frame(second_paned_group)
        second_paned_group.add(pane_2, weight=3)
        
        notebook = ttk.Notebook(pane_2)
        notebook.grid(row=0, column=0)
        
        tab_1 = ttk.Frame(notebook)
        notebook.add(tab_1, text="Metrics on problem")
        
        metrics_text = RichText(10, tab_1, width=40, height=15)
        metrics_text.pack(fill="both", expand=True)
        
        metrics_text.insert("end", self.information['metrics_heading'] + "\n", "h1")
        metrics_text.insert("end", self.information['metrics_formatted'])  
        
    def submit(self):        
        temp_file_location = f"/tmp/{uuid.uuid4()}.py"
        
        mypy_result = False
        pylint_result = False
        pylint_score = None
        radon_result = False
        radon_score = None
        testcases_result = None
        
        # Insert function_signature into text editor on load!!!
        code = self.get_code()
        
        function_signature = self.information['function_signature']
        function_name = self.information['function_name']
        
        with open(temp_file_location, "w") as writer:
            first_part = 'import json\nimport sys\nfrom typing import Union\ndef func_tester(fun):\n    def runner(*args, **kwargs):\n        try:\n            result = fun(*args, **kwargs)\n        except:\n            result = None\n        return result\n    return runner\n'
            last_part = f"\n\nprint({function_name}(*[json.loads(arg) for arg in sys.argv[1:]]))\nsys.exit()"
            new_code = f"{first_part}\n@func_tester\n{code}{last_part}"
            print(new_code)
            writer.write(new_code)
        
        try:                
            mypy_result = subprocess.run(['mypy', "--warn-no-return", temp_file_location], capture_output=True, timeout=5).stdout.decode().strip() 
            
            if "Success: no issues found" in mypy_result:
                mypy_result = "Successful"
        except Exception as e:
            print(e)
            
        try:
            pylint_result = subprocess.run(['pylint', temp_file_location], capture_output=True, timeout=5).stdout.decode().strip()
            # Use later
            pylint_score = pylint_result.split('\n')[-1].split()[-1]
        except Exception as e:
            print(e)
            
        try:
            radon_result = subprocess.run(['radon', 'cc', temp_file_location, '--total-average'], capture_output=True, timeout=5).stdout.decode().strip()
            radon_score = radon_result.split('\n')[-1].split()[-1][1:-1]
        except Exception as e:
            print(e)
                 
        if mypy_result != "Successful":
            print(mypy_result)
        elif pylint_score == None:
            print(pylint_result)
        elif radon_score == None:
            print(radon_result)
        else:
            print(f"Scores: pylint {pylint_score}, radon {radon_score}")
            print("Now send to runner!")
        
            try:
                testcases_result = self.run_code(self.information['test_case_location'], temp_file_location, self.information['answers_location'])
                print(testcases_result)
            except Exception as e:
                print(e)

        if testcases_result:
            # Add extensions later!!!
            solved = True
            
            """
            for key, val in sorted(testcases_result[0].items(), key = lambda x: x[0]):
                if val == False:
                    solved = False
                    messagebox.showinfo("Failure!", f"Testcase {key} failed!")
                    break
            """
            failed = self.populate_testcase_results(testcases_result)
            
            if failed != False:
                messagebox.showinfo("Failure!", f"Testcase {failed} failed!")
            else:
                metrics_result = testcases_result[1]
                messagebox.showinfo("Champion!", f"You solved this problem!!!\nCPU Load: {metrics_result['user_time'] * 10**3:0.3} ms\nMemory: {metrics_result['memory']} kilobytes")
        
        os.remove(temp_file_location)
        
    def populate_testcase_results(self, testcases_result):
        failed = False
        
        for key, val in sorted(testcases_result[0].items(), key = lambda x: x[0]):
            # key should be number, corresponds with self.cb list
            if val == True:
                self.cbs[key].config(bg="blue")
            else:
                self.cbs[key].config(bg="red")
                failed = key
                
        return failed
        
    def hint(self):
        messagebox.showinfo("Hint", self.information['hint'])
        
    def solution(self):
        # insert text into the editor
        self.editor_frame = Editor(self.interface_frame, starter_text = self.information['solution'])
        self.editor_frame.set_grid(_row=0, _column=1)
        
    def restart(self):
        self.editor_frame = Editor(self.interface_frame, starter_text = self.information['function_signature'])
        self.editor_frame.set_grid(_row=0, _column=1)
        
        for idx in range(len(self.information['testcases'])):
            try:
                self.cbs[idx].config(bg='gray')
            except:
                pass
                
    #####################################
    ####  Button group (Lower Left)  ####
    #####################################
    ######################################################################
    ####  Submit, hint, solution (lose points for hint and solution)  ####
    ######################################################################
    def button_group(self):
        # Hold off on the submission test cases button right now!
        button_frame = ttk.LabelFrame(self.interface_frame)
        button_frame.grid(row=1, column=1)
        
        restart_button = ttk.Button(button_frame, text="Restart", command=self.restart)
        submit_button = ttk.Button(button_frame, text="Submit", command=self.submit)
        hint_button = ttk.Button(button_frame, text="Hint (5 Pts)", command=self.hint)
        solution_button = ttk.Button(button_frame, text="Solution (15 Pts)", command=self.solution)
        
        cpane = Accordion(button_frame, 'Submission Test Cases', 'Results')
        cpane.grid(row = 2, column=0, columnspan=2, pady=15)
        
        for row_idx in range(len(self.information['testcases'])):
            self.cbs.append(tk.Button(cpane.frame, text="Test Case One", bg="gray", fg="white"))
            self.cbs[-1].grid(row=row_idx, column=3, pady=5)
        
        restart_button.grid(row=0, column=1, padx=5, pady=5)
        submit_button.grid(row=0, column=0, padx=5, pady=5)
        hint_button.grid(row=1, column=0, padx=5, pady=5)
        solution_button.grid(row=1, column=1, padx=5, pady=5)
        
        
    ####################################
    ####  Accordion (Bottom Right)  ####
    ####################################
    #############################################################
    ####  Submission with the test cases that passed/failed  ####
    ####                                                     #####
    ####  View submission test case for negative points (HR)  ####
    ####                               ###########################
    ####  Speed and memory comparison  ####
    #######################################
    def accordion_group(self):
        pass
        
    # bind accordion to button_submit
    def populate_accordion_group(self):
        # results = self.run_code()
        # CollaspiblePane here!
        pass        
        
    def get_code(self):
        return self.editor_frame.get_text()
        
    # Decorate was for fun!! @pylint_dynamic_code
    def run_code(self, test_case_location, temp_file_location, answers_location):
        test_result = None
        
        try:
            runner = Runner(test_case_location, temp_file_location, answers_location)
            test_case_indices = [0, 1, 2]
            
            # Modify the runner code to take a blank/empty list to mean all test indices
            test_result = runner.test_cases(test_case_indices) 
        except Exception as e:
            print(e)
            
        # Interpret results or better yet post them in the accordian below!!!
        return test_result

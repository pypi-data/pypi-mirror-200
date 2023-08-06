from pyriscv_client.service.submission_interface import SubmissionInterface

import tkinter as tk

def main() -> None:
    root = tk.Tk()
    
    information = {"problem_description_heading": "Problem 1", "problem_description": "Placeholder for the description of problem 1", "testcase_heading": "Test Cases", "testcases": {0: {'testcase': [11, 23, 1, 32, 2], "answer": [1, 5]}, 1: {"testcase": [1, 2, 3, 4], "answer": [1, 4]}, 2: {"testcase": [2, 3, 4], "answer": [2, 3]}}, "metrics_heading": "Problem 1 Metrics", "metrics_formatted": "METRICS HERE!\nCPU Load Avg: \nMemory Avg: ", "top_user_solutions_heading": "User Solutions", "test_case_location": "/home/freedom/Desktop/Helpful_Code/Elysium/tkinter/RunningLeetCodeCompetitor/test_cases/test_case_problem_1.txt", "answers_location": "/home/freedom/Desktop/Helpful_Code/Elysium/tkinter/RunningLeetCodeCompetitor/answers/answers_problem_1.txt", "function_signature": "def function(arg_list: list[int]) -> Union[bool, list[int]]:\n\t", "function_name": "function", "hint": "In a list, please put the minium number in the arg list and the length of the arg list", "solution": "def function(arg_list: list[int]) -> Union[bool, list[int]]:\n\treturn [min(arg_list), len(arg_list)]"}
    
    submission_interface = SubmissionInterface(root, information)
    submission_interface.set_grid()
    
    root.mainloop()
    
if __name__ == "__main__":
    main()

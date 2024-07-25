import time
from uC_SerialCommunication import uC_SerialCommunication

class bcolors:
    HEADER = '\033[35m'
    OKBLUE = '\033[34m'
    OKCYAN = '\033[36m'
    OKGREEN = '\033[32m'
    WARNING = '\033[33m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


uC = uC_SerialCommunication("/dev/ttyUSB0", 9600)

PARSING_STRINGS_TEST = [
    # (command_str, success_status_expected)
    # command not correctly delimited
    ("||", False),
    ("|||", False),
    # empty command
    ("||||", False),
    # command without arguments nor options
    ("||ping||", True),
    ("||ping|||", False),           # empty argument
    # command with arguments
    ("||ping|2-arg1-arg2||", True),
    ("||ping|2-arg1-arg2-arg3||", False),
    ("||ping|2-arg1||", False),
    ("||ping|11-arg1-arg2-arg3-arg4-arg5-arg6-arg7-arg8-arg9-arg10-arg11||", False),
    ("||ping|0||", False),          # no arguments
    # command with options
    ("||ping-opt1||", True),
    ("||ping-||", False),           # empty option
    ("||ping-opt1-opt2||", True),   # multiple options
    # command with arguments and options
    ("||ping-opt1|2-arg1-arg2||", True),
    ("||ping-opt1|2-arg1-arg2-arg3||", False),
    ("||ping-opt1|2-arg1||", False),
    ("||ping-opt1|0||", False),
    ("||ping-opt1-opt2|2-arg1-arg2||", True),
    ("||ping-|2-arg1-arg2||", False),
]

def run_test(test):
    command_str, success_status = test
    print(f"Running test: {command_str}")
    uC.execute_custom_command(command_str)
    
    response_debug = uC.rx_message() == "Success"
    print(f"Response debug: {"Success" if response_debug else "Error"}")
    
    if not response_debug:
        response_error = uC.rx_message()
        print(f"Response error: {response_error}")
    return  response_debug == success_status

def run_tests(test_set):
    nb_tests = len(test_set)    
    nb_fails = 0
    
    fail_set = []
    
    for i, test in enumerate(test_set):
        print(f"Running test {i+1}/{nb_tests}")
        result = run_test(test)
        if not result:
            nb_fails += 1
            fail_set.append((result, test))
        print(f"Expected: {test[1]}")
        print(f"{bcolors.OKGREEN}PASSED{bcolors.ENDC}" if result else f"{bcolors.FAIL}FAILED{bcolors.ENDC}", end="\n\n")
            
    print(f"Tests failed: {nb_fails}/{nb_tests}")
    
    if nb_fails > 0:
        print("Failed tests:")
        for test in fail_set:
            print(test)
        
    
def test_parsing_strings():
    print("## Testing parsing strings")
    
    uC.execute_custom_command("||debug-parser||")
    run_tests(PARSING_STRINGS_TEST)
    uC.execute_custom_command("||debug-parser||")
    
    print("## Testing parsing strings done")
    
    
if __name__ == "__main__":
    print("## uC Test")
    
    test_parsing_strings()
    
    print("## uC Test done")
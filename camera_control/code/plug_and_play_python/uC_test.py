import time
from uC_SerialCommunication import uC_SerialCommunication
import random

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
    ### command not correctly delimited
    ("||", False),
    ("|||", False),
    ### empty command
    ("||||", False),
    ### ping command
    ("||ping||", True),
    ("|ping|", False),
    ("ping", False),
    ("||ping-opt||", False),
    ("||ping|2-arg1-arg2||", False),
    ### info command
    ("||info||", True),
    ("||info-custom_name||", True),
    ("||info-board||", True),
    ("||info-mcu_type||", True),
    ("||info-ucid||", True),
    ("||info-unknown||", False),
    ("||info|1-unknown||", False),
    ("||info-ucid|1-unknown||", False),
    ### trigger command    
    ("||trigger-all||", True),
    ("||trigger||", False),
    ("||trigger|1-cam1||", False),
    ("||trigger-||", False),
    ## trigger-selective command
    ("||trigger-selective|1-cam1||", True),
    ("||trigger-selective|2-cam1-cam2||", True),
    ("||trigger-selective|1-cam1-cam2||", False),
    ("||trigger-selective|4-cam1-cam2||", False),
    ("||trigger-selective|11-cam1-cam2-cam3-cam4-cam5-cam6-cam7-cam8-cam9-cam10-cam11||", False),
    ## trigger-show command
    ("||trigger-show||", True),
    ("||trigger-show|1-cam1||", False),
    ### help command
    ("||help||", True),
    ("||help-ping||", True),
    ("||help-info||", True),
    ("||help-trigger||", True),
    ("||help-debug||", True),
    ("||help-help||", True),
    ("||help-unknown||", False),
    ("||help|1-unknown||", False),
    ("||help-ping|1-unknown||", False),    
]

random.shuffle(PARSING_STRINGS_TEST)


def run_test(test):
    command_str, success_status = test
    print(f"Running test: {command_str}")
    uC.tx_message(command_str)
    
    response_message = uC.rx_message()
    response_debug = uC.rx_message() == "Success"
    
    print(f"Response debug: {"Success" if response_debug else "Error"}")
    
    if not response_debug:
        response_error = uC.rx_message()
        print(f"Response error: {response_error if response_error else "No error message"}")
    print(f"Expected: {"Success" if test[1] else "Error"}")
    return  response_debug == success_status

def run_tests(test_set):
    nb_tests = len(test_set)    
    nb_fails = 0
    
    fail_set = []
    
    uC.tx_message("||debug||")
    uC.rx_message()
    for i, test in enumerate(test_set):
        print(f"Running test {i+1}/{nb_tests}")
        result = run_test(test)
        if not result:
            nb_fails += 1
            fail_set.append((result, test))
        print(f"{bcolors.OKGREEN}PASSED{bcolors.ENDC}" if result else f"{bcolors.FAIL}FAILED{bcolors.ENDC}", end="\n\n")
            
    print(f"Tests failed: {nb_fails}/{nb_tests}")
    
    if nb_fails > 0:
        print("Failed tests:")
        for test in fail_set:
            print(test)
        
    uC.tx_message("||debug||")
    uC.rx_message()
    
    
        
    
def test_parsing_strings():
    print("## Testing parsing strings")
    
    run_tests(PARSING_STRINGS_TEST)
    
    print("## Testing parsing strings done")
    
    
if __name__ == "__main__":
    print("## uC Test")
    
    test_parsing_strings()
    
    print("## uC Test done")
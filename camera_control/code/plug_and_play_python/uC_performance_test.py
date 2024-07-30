from uC_SerialCommunication import uC_SerialCommunication
from uC_Commands import *
from tqdm import tqdm

COMMANDS = [
    # Single word commands
    "||ping||",
    "||info||",
    # Commands with options
    "||info-hello||",
    "||info-custom_name||",
    "||info-board||",
    "||info-mcu_type||",
    "||info-ucid||",
    "||trigger-all||",
    # Complete commands
    "||trigger-selective|1-c1||",
    "||trigger-selective|2-c1-c2||",
    "||trigger-selective|3-c1-c2-c3||",
    "||trigger-selective|4-c1-c2-c3-c4||",
    "||trigger-selective|5-c1-c2-c3-c4-c5||",
    "||trigger-selective|6-c1-c2-c3-c4-c5-c6||",
    "||trigger-selective|7-c1-c2-c3-c4-c5-c6-c7||",
    "||trigger-selective|8-c1-c2-c3-c4-c5-c6-c7-c8||",
    "||trigger-selective|9-c1-c2-c3-c4-c5-c6-c7-c8-c9||",
    "||trigger-selective|10-c1-c2-c3-c4-c5-c6-c7-c8-c9-c10||",
]

deserialization_time = []

def execute_commands():
    # Start debug mode to retrieve deserialization time
    uC.execute_command(DebugCommand(), do_print=False)
    # Execute all commands
    test_set = []
    for command in tqdm(COMMANDS):
        uC.tx_message(command)
        status, message, debug_message = uC.rx_message()
        #print(f"<- Received: ({status}) {message}" + (f" | {debug_message}" if debug_message != None else "") +"\n\n")
        test_set.append(float(debug_message))
        
    deserialization_time.append(test_set)
    uC.execute_command(DebugCommand(), do_print=False)


if __name__ == "__main__":
    print("## uC Performance Test")
    

    for command in tqdm(range(5)):
        uC = uC_SerialCommunication("/dev/ttyUSB0", 9600)
        execute_commands()
        uC.close()
        
    # Compute the average time for each test
    avg_test_time = []
    for test in deserialization_time:
        avg_test_time.append(sum(test)/len(test))
        
    # compute the average time for all tests
    avg_time = sum(avg_test_time)/len(avg_test_time)
    
    # Execute the test five times and save results in a file in the format:
    # command, length, time_1, time_2, time_3, time_4, time_5
    # For each new test, close and open the connection
    
    with open("deserialization_time.csv", "w") as f:
        f.write("command,length,time_1,time_2,time_3,time_4,time_5\n")
        for command in range(len(COMMANDS)):
            f.write(COMMANDS[command] + "," + str(len(COMMANDS[command])) + ",")
            for test_set in range(5):
                f.write(str(deserialization_time[test_set][command]) + ",")
            f.write("\n")
        
    print("## End of uC Performance Test")
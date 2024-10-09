from software.uC_Manager import uC_Manager
from software.colors import bcolors
from software.uC_Commands import PingCommand, TriggerCommand

import os

manager = uC_Manager(9600)

print("=" * 50)

while True:
    print("#" * 50)
    print("## Available ports:")
    for port in manager.uC_connections:
        print(f"- {port}")
    print("-" * 50)
    user = input("Press ENTER to trigger the cameras (or q to quit): ")
    if user == "q":
        break

    os.system('cls' if os.name == 'nt' else 'clear')

    print(bcolors.OKCYAN)
    print("## Sending command...")
    response = manager.send_command_to_uC(TriggerCommand())
    print(f"## {response if not None else 'Failed'}")
    print(bcolors.ENDC)

    
print("=" * 50)

manager.close()
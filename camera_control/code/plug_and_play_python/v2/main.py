import uC_Manager
import uC_Commands


if __name__ == "__main__":
    
    print("Creating manager...")
    manager = uC_Manager.uC_Manager()
    ports = manager.get_uC_ports()
    print(f"Available ports:")
    for i, port in enumerate(ports):
        print(f"{i+1}. {port}")
    
    print("Creating connection...")
    port = ports[0]
    manager.connect_to_uC(port)
    
    print("Using connection...")
    connection = manager.get_uC_connection(port)
    
    commands = [
        uC_Commands.PingCommand(),
        uC_Commands.InfoCommand(),
    ]
    
    for command in commands:
        response = connection.send_command(command)
        print(f"Response: {response}")
        
    print("Disconnecting...")
    manager.disconnect_from_uC(port)
    
    print("Closing manager...")
    manager.close()
    
    print("Done.")
    
#include <Arduino.h>

#define STRING_PING "ping"
#define STRING_INFO "info"
#define STRING_TRIGGER "trigger"
#define STRING_DEBUG "debug"
#define STRING_HELP "help"

#define COMMAND_DELIMITER "||"
#define DELIMITER "|"
#define SEPARATOR "-"

#define TRIGGER_OPTION_ALL "all"
#define TRIGGER_OPTION_SELECTIVE "selective"
#define TRIGGER_OPTION_SHOW "show"

#define INFO_ARG_CUSTOM_NAME "custom_name"
#define INFO_ARG_BOARD "board"
#define INFO_ARG_MCU_TYPE "mcu_type"
#define INFO_ARG_UCID "ucid"

#define ARGUMENT_LIST_MAXSIZE 10

//======== STRUCT DEFINITION ========//
struct CommandArgs {
    String fullString = "";
    String command = "";
    String option = "";
    String arguments = "";
    int argNumber = 0;
    String args[ARGUMENT_LIST_MAXSIZE];
    
    String errorMessage = "Error (Deserializer): ";
    int status = 0;
};

class Deserializer {
    static void errorParser(CommandArgs &deserialized_, String errorMsg);
    static void deserializeArgBlock(CommandArgs &deserialized_);
    static void validateCommandArg(CommandArgs &deserialized_);
    static void validatePingCommand(CommandArgs &deserialized_);
    static void validateInfoCommand(CommandArgs &deserialized_);
    static void validateTriggerCommand(CommandArgs &deserialized_);
    static void validateDebugCommand(CommandArgs &deserialized_);
    static void validateHelpCommand(CommandArgs &deserialized_);
    static void deserializeCommand(CommandArgs &deserialized_, String &serialMessage);

public:
    Deserializer();
    static CommandArgs deserialize(String serialMessage);
};

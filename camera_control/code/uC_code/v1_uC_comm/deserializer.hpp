#include <Arduino.h>

#define STRING_PING F("ping")
#define STRING_INFO F("info")
#define STRING_TRIGGER F("trigger")
#define STRING_DEBUG F("debug")

#define COMMAND_DELIMITER F("||")
#define DELIMITER F("|")
#define SEPARATOR F("-")

#define TRIGGER_OPTION_ALL F("all")
#define TRIGGER_OPTION_SELECTIVE F("selective")
#define TRIGGER_OPTION_SHOW F("show")

#define INFO_OPTION_CUSTOM_NAME F("custom_name")
#define INFO_OPTION_BOARD F("board")
#define INFO_OPTION_MCU_TYPE F("mcu_type")
#define INFO_OPTION_UCID F("ucid")

#define ARGUMENT_LIST_MAXSIZE 10

//======== STRUCT DEFINITION ========//
struct CommandArgs {
    String fullString = "";
    String command = "";
    String option = "";
    String arguments = "";
    int argNumber = 0;
    String args[ARGUMENT_LIST_MAXSIZE];
    
    String errorMessage = "Deserializer: ";
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
    static void deserializeCommand(CommandArgs &deserialized_, String &serialMessage);

public:
    Deserializer();
    static CommandArgs deserialize(String serialMessage);
};

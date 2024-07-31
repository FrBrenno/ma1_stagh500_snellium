#include "deserializer.hpp"

//======== DESERIALIZING FUNCTIONS ========//

Deserializer::Deserializer() {}

void Deserializer::errorParser(CommandArgs &deserialized_, String errorMsg)
{
    deserialized_.errorMessage += errorMsg;
    deserialized_.status = 1;
}

CommandArgs Deserializer::deserialize(String serialMessage)
{
    // Initialize the deserialized struct
    CommandArgs deserialized_;

    deserialized_.fullString = serialMessage;

    // Check if string is correctly delimited || <COMMAND> ||
    if (!serialMessage.startsWith(COMMAND_DELIMITER))
    {
        errorParser(deserialized_, F("Command is not correctly delimited."));
        return deserialized_;
    }
    serialMessage = serialMessage.substring(2);

    if (!serialMessage.endsWith(COMMAND_DELIMITER))
    {
        errorParser(deserialized_, F("Command is not correctly delimited"));
        return deserialized_;
    }
    serialMessage = serialMessage.substring(0, serialMessage.length() - 2);

    // Check if string is empty: ||||
    if (serialMessage.equals(COMMAND_DELIMITER))
    {
        errorParser(deserialized_, F("Empty command block."));
        return deserialized_;
    }

    // Process <COMMAND> variable
    deserializeCommand(deserialized_, serialMessage);
    // Check if there was an error during deserialization.
    // If there was, stop processing
    if (deserialized_.status == 1)
    {
        return deserialized_;
    }

    // Verify if options and arguments are valid to the command
    validateCommandArg(deserialized_);

    return deserialized_;
}

void Deserializer::deserializeCommand(CommandArgs &deserialized_, String &serialMessage)
{
    // Find which type de command is: single word, word-option or word-option-arguments or word-arguments
    int idxOptionSeparator = serialMessage.indexOf(SEPARATOR);
    int idxBlockDelimiter = serialMessage.indexOf(DELIMITER);

    // Single word command : ||<COMMAND>||
    if (idxOptionSeparator == -1 && idxBlockDelimiter == -1)
    {
        deserialized_.command = serialMessage;
    }
    // Command with option : ||<COMMAND>-<OPTION>||
    else if (idxOptionSeparator != -1 && idxBlockDelimiter == -1)
    {
        deserialized_.command = serialMessage.substring(0, idxOptionSeparator);
        deserialized_.option = serialMessage.substring(idxOptionSeparator + 1);
    }
    // Command with option and arguments : ||<COMMAND>-<OPTION>|<ARGBLOCK>||
    else if (idxOptionSeparator != -1 && idxBlockDelimiter != -1)
    {
        deserialized_.command = serialMessage.substring(0, idxOptionSeparator);
        deserialized_.option = serialMessage.substring(idxOptionSeparator + 1, idxBlockDelimiter);
        deserialized_.arguments = serialMessage.substring(idxBlockDelimiter + 1);
        deserializeArgBlock(deserialized_);
    }
    // Command with arguments : ||<COMMAND>|<ARGBLOCK>||
    else if (idxOptionSeparator == -1 && idxBlockDelimiter != -1)
    {
        deserialized_.command = serialMessage.substring(0, idxBlockDelimiter);
        deserialized_.arguments = serialMessage.substring(idxBlockDelimiter + 1);
        deserializeArgBlock(deserialized_);
    }
    else
    {
        errorParser(deserialized_, F("Command is not correctly delimited."));
    }
}

void Deserializer::deserializeArgBlock(CommandArgs &deserialized_)
{
    // <ARGBLOCK> rule is : <ARGNUMBER><ARGLIST>
    // <ARGNUMBER> is the number of arguments
    // <ARGLIST> rule is: <SEP><ARG><ARGLIST> or <SEP><ARG>
    // <SEP> is the separator character

    // Find the number of arguments
    int idxSeparator = deserialized_.arguments.indexOf(SEPARATOR);
    if (idxSeparator == -1)
    {
        errorParser(deserialized_, F("Arguments block is not correctly delimited."));
        return;
    }

    String argNumberStr = deserialized_.arguments.substring(0, idxSeparator);
    int argNumber = argNumberStr.toInt();

    // Check is the number of arguments is valid
    if (argNumber <= 0 || argNumber > ARGUMENT_LIST_MAXSIZE)
    {
        errorParser(deserialized_, F("Too many arguments."));
        return;
    }
    deserialized_.argNumber = argNumber;

    // Find the arguments and put them on the array
    //<SEP><ARG><ARGLIST> or <SEP><ARG>
    String arguments = deserialized_.arguments.substring(idxSeparator + 1);
    deserialized_.arguments = arguments;
    int argCounter = 0;
    while (arguments.length() > 0)
    {
        int idxSeparator = arguments.indexOf(SEPARATOR);
        if (idxSeparator == -1)
        {
            deserialized_.args[argCounter] = arguments;
            break;
        }
        deserialized_.args[argCounter] = arguments.substring(0, idxSeparator);
        arguments = arguments.substring(idxSeparator + 1);
        argCounter++;
    }


    // Check if the number of arguments is the same as the number of arguments found
    if (argCounter + 1 != argNumber)
    {
        errorParser(deserialized_, F("Incorrect number of arguments."));
        return;
    }


    return;
}

void Deserializer::validateCommandArg(CommandArgs &deserialized_)
{
    if (deserialized_.command.equals(STRING_PING))
    {
        validatePingCommand(deserialized_);
    }

    else if (deserialized_.command.equals(STRING_INFO))
    {
        validateInfoCommand(deserialized_);
    }

    else if (deserialized_.command.equals(STRING_TRIGGER))
    {
        validateTriggerCommand(deserialized_);
    }

    else if (deserialized_.command.equals(STRING_DEBUG))
    {
        validateDebugCommand(deserialized_);
    }
    // Command is not recognized
    else
    {
        errorParser(deserialized_, "Command \"" + deserialized_.fullString + "\"" + " unknown.");
    }
}

void Deserializer::validatePingCommand(CommandArgs &deserialized_)
{
    // ||ping||
    // PING COMMAND is a single-word command accepting no options or arguments
    if (deserialized_.option != "" || deserialized_.arguments != "")
    {
        errorParser(deserialized_, F("Ping command does not accept options or arguments."));
    }
}

void Deserializer::validateInfoCommand(CommandArgs &deserialized_)
{
    // ||info|| or ||info-<OPTION>||
    // <OPTION> for info command can be: custom_name, board, mcu_type, ucid

    // It takes no arguments
    if (deserialized_.argNumber > 0)
    {
        errorParser(deserialized_, F("Info command does not accept arguments."));
    }

    // It can take no options or the options are valid
    if (deserialized_.option != "" &&
        deserialized_.option != INFO_OPTION_CUSTOM_NAME &&
        deserialized_.option != INFO_OPTION_BOARD &&
        deserialized_.option != INFO_OPTION_MCU_TYPE &&
        deserialized_.option != INFO_OPTION_UCID)
    {
        errorParser(deserialized_, F("Info command has invalid options."));
    }
}

void Deserializer::validateTriggerCommand(CommandArgs &deserialized_)
{
    // ||trigger-<OPTION>|| or ||trigger-selective|<ARGBLOCK>||
    // <OPTION> for trigger command can be: all, selective, show
    // all: trigger all cameras
    // selective: trigger only cameras passed as arguments
    // show: show the cameras that are available
    // <ARGBLOCK> rule is : <ARGNUMBER><ARGLIST>
    // <ARGLIST> rule is: <SEP><ARG><ARGLIST> or <SEP><ARG>
    // <SEP> is the separator character
    // <ARGNUMBER> is the number of arguments
    // <ARG> is the camera name

    // TRIGGER COMMAND takes options that are trigger modes and arguments that are the camera names

    if (deserialized_.option != TRIGGER_OPTION_ALL &&
        deserialized_.option != TRIGGER_OPTION_SELECTIVE &&
        deserialized_.option != TRIGGER_OPTION_SHOW)
    {
        errorParser(deserialized_, F("Invalid trigger option."));
    }

    // If the option is show or all, it takes no arguments
    if (deserialized_.option == TRIGGER_OPTION_SHOW || deserialized_.option == TRIGGER_OPTION_ALL)
    {
        if (deserialized_.argNumber > 0)
        {
            errorParser(deserialized_, "Trigger " + deserialized_.option + " does not accept arguments.");
        }
    }

    // If the option is selective, it takes arguments
    if (deserialized_.option == TRIGGER_OPTION_SELECTIVE)
    {
        if (deserialized_.argNumber == 0)
        {
            errorParser(deserialized_, "Trigger " + deserialized_.option + " takes at least one argument.");
        }
    }
    
    // TODO: Check if the cameras names passed as arguments are valid
}

void Deserializer::validateDebugCommand(CommandArgs &deserialized_){
    // ||debug||
    // debug command takes no options nor arguments

    if (deserialized_.option != "" || deserialized_.arguments != "")
    {
        errorParser(deserialized_, F("Debug command does not accept options or arguments."));
    }
}


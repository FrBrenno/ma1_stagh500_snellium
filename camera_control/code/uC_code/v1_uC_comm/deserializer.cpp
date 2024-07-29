#include "deserializer.hpp"

//======== DESERIALIZING FUNCTIONS ========//

Deserializer::Deserializer() {}

void Deserializer::errorParser(CommandArgs &deserialized_, String errorMsg)
{
    deserialized_.errorMessage +=   errorMsg;
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
        errorParser(deserialized_, "Command is not correctly delimited: Not starting with ||.");
        return deserialized_;
    }
    serialMessage = serialMessage.substring(2);

    if (!serialMessage.endsWith(COMMAND_DELIMITER))
    {
        errorParser(deserialized_, "Command is not correctly delimited: Not ending with ||.");
        return deserialized_;
    }
    serialMessage = serialMessage.substring(0, serialMessage.length() - 2);

    // Check if string is empty: ||||
    if (serialMessage.equals(COMMAND_DELIMITER))
    {
        errorParser(deserialized_, "Empty command block.");
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
        errorParser(deserialized_, "Command is not correctly delimited.");
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
        errorParser(deserialized_, "Arguments block is not correctly delimited.");
        return;
    }

    String argNumberStr = deserialized_.arguments.substring(0, idxSeparator);
    int argNumber = argNumberStr.toInt();
    deserialized_.argNumber = argNumber;

    // Check is the number of arguments is valid
    if (argNumber <= 0 || argNumber > ARGUMENT_LIST_MAXSIZE)
    {
        errorParser(deserialized_, "Number of arguments is not valid.");
        return;
    }

    // Find the arguments and put them on the array
    String arguments = deserialized_.arguments.substring(idxSeparator + 1);
    int argCount = 0;
    for (argCount = 0; argCount < argNumber; argCount++)
    {
        int idxSeparator = arguments.indexOf(SEPARATOR);
        if (idxSeparator == -1)
        {
            deserialized_.args[argCount] = arguments;
            break;
        }
        else
        {
            deserialized_.args[argCount] = arguments.substring(0, idxSeparator);
            arguments = arguments.substring(idxSeparator + 1);
        }
    }

    if (argCount + 1 != argNumber)
    {
        errorParser(deserialized_, "There is not the same number of arguments as mentioned!");
    }

    return;
}

void Deserializer::validateCommandArg(CommandArgs &deserialized_)
{
    // PING COMMAND is a single-word command accepting no options or arguments
    if (deserialized_.command.equals(STRING_PING))
    {
        validatePingCommand(deserialized_);
    }

    // INFO COMMAND only takes arguments and its arguments are the information to be retrieved
    else if (deserialized_.command.equals(STRING_INFO))
    {
        validateInfoCommand(deserialized_);
    }

    // TRIGGER COMMAND takes options that are trigger modes and arguments that are the camera names
    else if (deserialized_.command.equals(STRING_TRIGGER))
    {
        validateTriggerCommand(deserialized_);
    }

    // HELP COMMAND can take no options or arguments but can take arguments with the command name to get help
    else if (deserialized_.command.equals(STRING_HELP))
    {
        validateHelpCommand(deserialized_);
    }

    // Command is not recognized
    else
    {
        errorParser(deserialized_, "Command \"" + deserialized_.fullString + "\"" + " unknown.");
    }
}

void Deserializer::validateHelpCommand(CommandArgs &deserialized_)
{
    if (deserialized_.option != "")
    {
        errorParser(deserialized_, "Help command does not accept options.");
    }

    if (deserialized_.argNumber > 1)
    {
        errorParser(deserialized_, "Help command takes at most one argument.");
    }

    if (deserialized_.argNumber == 1)
    {
        String arg = deserialized_.args[0];
        if (arg != STRING_PING &&
            arg != STRING_INFO &&
            arg != STRING_TRIGGER &&
            arg != STRING_HELP)
        {
            errorParser(deserialized_, "Help command has invalid arguments.");
        }
    }
}

void Deserializer::validateTriggerCommand(CommandArgs &deserialized_)
{
    if (deserialized_.option != TRIGGER_OPTION_SELECTIVE &&
        deserialized_.option != TRIGGER_OPTION_SHOW)
    {
        errorParser(deserialized_, "Trigger command has invalid options.");
    }

    if (deserialized_.arguments == "")
    {
        errorParser(deserialized_, "Trigger command requires arguments.");
    }

    if (deserialized_.argNumber == 0)
    {
        errorParser(deserialized_, "Trigger command requires at least one argument.");
    }
}

void Deserializer::validateInfoCommand(CommandArgs &deserialized_)
{
    if (deserialized_.option != "")
    {
        errorParser(deserialized_, "Info command does not accept options.");
    }

    if (deserialized_.arguments == "")
    {
        errorParser(deserialized_, "Info command requires arguments.");
    }

    if (deserialized_.argNumber == 0)
    {
        errorParser(deserialized_, "Info command requires at least one argument.");
    }

    for (int i = 0; i < deserialized_.argNumber; i++)
    {
        String arg = deserialized_.args[i];
        if (arg != INFO_ARG_CUSTOM_NAME &&
            arg != INFO_ARG_BOARD &&
            arg != INFO_ARG_MCU_TYPE &&
            arg != INFO_ARG_UCID)
        {
            errorParser(deserialized_, "Info command has invalid arguments.");
        }
    }
}

void Deserializer::validatePingCommand(CommandArgs &deserialized_)
{
    if (deserialized_.option != "" || deserialized_.arguments != "")
    {
        errorParser(deserialized_, "Ping command does not accept options or arguments.");
    }
}

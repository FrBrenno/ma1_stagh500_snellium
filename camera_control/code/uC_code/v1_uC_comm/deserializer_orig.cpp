/* void deserilizeArgumentsBlock(CommandArgs& deserialized){
  String arguments = deserialized.arguments;
  // Parse argument number
  int idxFirstSeparator = arguments.indexOf(COMMAND_SEPARATOR);

  if (idxFirstSeparator == -1){ // Empty argument block or bad-formatted.
    errorParser("Arguments block is empty or not well formatted.");
  }
  else{
    int argNumber = arguments.substring(0, idxFirstSeparator).toInt();
    arguments = arguments.substring(idxFirstSeparator + 1);
    deserialized.argNumber = argNumber;

    // See if argNumber is lower than argument list capacity
    if (argNumber > ARGUMENT_LIST_MAXSIZE){
      errorParser("There are too many arguments.");
    }

    // Parse arguments and put them in the array
    int argCount = 0;
    for (argCount = 0; argCount < argNumber; argCount++){
      int idxSeparator = arguments.indexOf(COMMAND_SEPARATOR);
      
      // grab arg and set into the array
      String arg = arguments.substring(0, idxSeparator);
      deserialized.args[argCount] = arg;
      // reduce input
      arguments = arguments.substring(idxSeparator + 1); 
    }
    if (argCount + 1 != argNumber)
      errorParser("There is not the same number of arguments as mentioned!");
  }
}

CommandArgs deserialize(){
  String input = Serial.readString();
  CommandArgs deserialized;
  deserialized.fullString = input;
  
  if (input.startsWith(COMMAND_DELIMITER) ){ 
    input = input.substring(2);

    if (input.endsWith(COMMAND_DELIMITER)){
      input = input.substring(0, input.length()-2);
      // Empty command: ||||
      if (input.equals(COMMAND_DELIMITER)){
        errorParser("Empty command block.");
        return deserialized;
      }

      //=== Separate COMMAND-OPTIONS from #ARGS-ARGUMENTS
      int idxBlockDelimiter = input.indexOf(BLOCK_DELIMITER);

      if (idxBlockDelimiter == -1){     // No block delimitation, no arguments
        deserialized.arguments = "";
      }
      else{                             // Arguments
        String arguments = input.substring(idxBlockDelimiter + 1);
        deserialized.arguments = arguments;
        // break down arguments into array
        deserilizeArgumentsBlock(deserialized);
      }

      //=== Separate COMMAND from OPTION
      input = input.substring(0, idxBlockDelimiter);
      int idxOptionSeparator = input.indexOf(COMMAND_SEPARATOR);

      if (idxOptionSeparator == -1){  // No separator on command block, single command word
        deserialized.option = "";
      }
      else{
        String option = input.substring(idxOptionSeparator + 1);
        if (option.length() == 0){ // option block is empty : command-
          errorParser("Empty option block.");
        }
        else{
          deserialized.option = option;
        } 
      }
      deserialized.command = input.substring(0, idxOptionSeparator);
    }
    else{
      errorParser("Command is not correctly delimited: Not ending with ||.");
    }
  }else{
    errorParser("Command is not correctly delimited: Not starting with ||.");
  }

  return deserialized;
}
 */
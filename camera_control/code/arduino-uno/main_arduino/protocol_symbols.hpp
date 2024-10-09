#pragma once

// =========== DELIMITERS ===========//
/* #define START_COMMAND_CHAR (char) '\x02'
#define END_COMMAND_CHAR (char) '\x03'
#define BLOCK_SEPARATOR_CHAR (char) '\x1D'
#define ELEMENT_SEPARATOR_CHAR (char) '\x1F' */

#define START_COMMAND_CHAR (char) '<'
#define END_COMMAND_CHAR (char) '>'
#define BLOCK_SEPARATOR_CHAR (char) '#'
#define ELEMENT_SEPARATOR_CHAR (char) '$'

// =========== COMMANDS ===========//

#define CMD_PING "ping"
#define CMD_INFO "info"

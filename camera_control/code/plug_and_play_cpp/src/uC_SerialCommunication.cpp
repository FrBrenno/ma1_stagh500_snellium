#include "uC_SerialCommunication.hpp"

uC_SerialCommunication::uC_SerialCommunication(){
    serialName = "Serial Communication";
}

std::string uC_SerialCommunication::getName() {
    return serialName;
}
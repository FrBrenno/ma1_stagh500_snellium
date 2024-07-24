#include <iostream>
#include "uC_SerialCommunication.hpp"


int main(){

    uC_SerialCommunication serial;

    std::cout << "Hello " << serial.getName() << std::endl;

    return 0;
}
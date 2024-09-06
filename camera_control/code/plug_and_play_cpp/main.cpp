#include <iostream>
#include <string>


const std::string extract_token(std::string &response, std::string delimiter) {
    if (response == "")
    {
        return "";
    }

    std::string token;
    int idx_separator = response.find(delimiter);
    if (idx_separator == -1){
        token = response;
        response = "";
    } else {
        token = response.substr(0, idx_separator);
        response = response.substr(idx_separator + 1);
    }

    return token;
}

int main(){
    // Parsing

    std::string response = "||Success|pong||";

    std::string delimiter = "|";

    if (!response.starts_with("||") ||
        !response.ends_with("||"))
    {
        std::cout << "Invalid response format" << std::endl;
        return 1;
    }

    response = response.substr(2, response.size() - 4);
    std::cout << response << std::endl;

    std::string status = extract_token(response, delimiter);
    std::string message = extract_token(response, delimiter);
    std::string debug = extract_token(response, delimiter);

    if (debug == message)
        debug = "";

    std::cout << "Status: " << status << std::endl;
    std::cout << "Message: " << message << std::endl;
    std::cout << "Debug: " << debug << std::endl;

    return 0;
}
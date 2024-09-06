cmake_minimum_required(VERSION 3.5)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(NAME test_parsing)

project(${NAME})

include(GNUInstallDirs)
find_package(PkgConfig REQUIRED)
pkg_check_modules(SYSTEMD REQUIRED libsystemd)

add_executable(${NAME} main.cpp)

target_link_libraries(${NAME} ${SYSTEMD_LIBRARIES})
target_include_directories(${NAME} PUBLIC ${SYSTEMD_INCLUDE_DIRS})

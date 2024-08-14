cmake_minimum_required(VERSION 3.5)

project(test_libsystemd)

include(GNUInstallDirs)
find_package(PkgConfig REQUIRED)
pkg_check_modules(SYSTEMD REQUIRED libsystemd)

add_executable(test_libsystemd main.cpp)

target_link_libraries(test_libsystemd ${SYSTEMD_LIBRARIES})
target_include_directories(test_libsystemd PUBLIC ${SYSTEMD_INCLUDE_DIRS})

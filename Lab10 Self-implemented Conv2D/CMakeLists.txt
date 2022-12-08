cmake_minimum_required(VERSION 3.17)
project(Conv)

set(CMAKE_CXX_STANDARD 14)

add_executable(Conv main.cpp conv_oop.h conv_pop.h timer.h)

find_package(OpenCV REQUIRED)

target_link_libraries(Conv ${OpenCV_LIBS})
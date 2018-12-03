cmake_minimum_required(VERSION 3.10)

project(pointcloud2mesh CXX)

find_package(CGAL REQUIRED)
add_executable(pointcloud2mesh.out main.cpp)
target_link_libraries(pointcloud2mesh.out CGAL::CGAL)

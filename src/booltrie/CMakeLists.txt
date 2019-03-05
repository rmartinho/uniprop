cmake_minimum_required (VERSION 3.10)

file (GLOB_RECURSE booltrie_SRC "*.c++")

add_library (booltrie STATIC ${booltrie_SRC})

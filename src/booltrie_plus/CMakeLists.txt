cmake_minimum_required (VERSION 3.10)

file (GLOB_RECURSE booltrie_plus_SRC "*.c++")

add_library (booltrie_plus STATIC ${booltrie_plus_SRC})

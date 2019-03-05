cmake_minimum_required (VERSION 3.10)

file (GLOB_RECURSE range_bsearch_SRC "*.c++")

add_library (range_bsearch STATIC ${range_bsearch_SRC})

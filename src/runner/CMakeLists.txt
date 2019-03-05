cmake_minimum_required (VERSION 3.10)

file (GLOB_RECURSE runner_SRC "*.c++")

add_executable (runner ${runner_SRC})
target_link_libraries (runner range_bsearch booltrie booltrie_plus booltrie_plus_avx)


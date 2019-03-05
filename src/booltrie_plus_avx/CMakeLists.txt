cmake_minimum_required (VERSION 3.10)

file (GLOB_RECURSE booltrie_plus_avx_SRC "*.c++")

add_library (booltrie_plus_avx STATIC ${booltrie_plus_avx_SRC})

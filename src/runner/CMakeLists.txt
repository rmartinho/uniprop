cmake_minimum_required (VERSION 3.10)

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

file (GLOB_RECURSE runner_SRC "*.c++")

set_source_files_properties(benches_avx.c++ PROPERTIES COMPILE_FLAGS -mavx2)
add_executable (runner ${runner_SRC})
target_link_libraries (runner range_bsearch booltrie booltrie_plus booltrie_plus_avx Threads::Threads)

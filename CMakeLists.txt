cmake_minimum_required (VERSION 3.10)
project (uniprop)

set (CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

set (CMAKE_CXX_STANDARD 17)
set (CMAKE_CXX_EXTENSIONS OFF)

include_directories (${PROJECT_SOURCE_DIR}/include)

add_subdirectory (src/runner)

add_subdirectory (src/range_bsearch)
add_subdirectory (src/booltrie)
add_subdirectory (src/booltrie_plus)
add_subdirectory (src/booltrie_plus_avx)

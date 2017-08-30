cmake_minimum_required(VERSION 2.8.7)
project (Embedding C CXX)

include(FindPackageHandleStandardArgs)

set(INTEL_ROOT "/opt/intel")
set(MKL_ROOT /home/marekstrelec/intel/compilers_and_libraries/linux/mkl)

# set(MKL_INCLUDE_DIR ${MKL_ROOT}/include)
set(MKL_LIBRARIES ${MKL_ROOT}/lib)

# Find include dir
find_path(MKL_INCLUDE_DIR mkl.h
    PATHS ${MKL_ROOT}/include)
MESSAGE( STATUS "MKL_INCLUDE_DIR: " ${MKL_INCLUDE_DIR} )

# Find libraries
# Handle suffix
set(_MKL_ORIG_CMAKE_FIND_LIBRARY_SUFFIXES ${CMAKE_FIND_LIBRARY_SUFFIXES})

if(MKL_STATAIC)
    set(CMAKE_FIND_LIBRARY_SUFFIXES .a)
else()
    set(CMAKE_FIND_LIBRARY_SUFFIXES .so)
endif()

# MKL is composed by four layers: Interface, Threading, Computational and RTL
find_library(MKL_LIBRARY mkl_rt
    PATHS ${MKL_ROOT}/lib/ia32/)

set(MKL_MINIMAL_LIBRARY ${MKL_LIBRARY})
set(CMAKE_FIND_LIBRARY_SUFFIXES ${_MKL_ORIG_CMAKE_FIND_LIBRARY_SUFFIXES})

find_package_handle_standard_args(MKL DEFAULT_MSG
    MKL_INCLUDE_DIR MKL_LIBRARY MKL_MINIMAL_LIBRARY)

MESSAGE( STATUS "MKL_SDL: " ${MKL_FOUND} )
if(MKL_FOUND)
    set(MKL_INCLUDE_DIRS ${MKL_INCLUDE_DIR})
    set(MKL_LIBRARIES ${MKL_LIBRARY})
    set(MKL_MINIMAL_LIBRARIES ${MKL_LIBRARY})
endif()

# FAISS
set(FAISS_ROOT faiss)
include_directories(${FAISS_ROOT})
link_directories(${FAISS_ROOT})
add_subdirectory(${FAISS_ROOT})

file(GLOB faiss_cpu_headers ${CMAKE_CURRENT_SOURCE_DIR}/faiss/*.h)
file(GLOB faiss_cpu_cpp ${CMAKE_CURRENT_SOURCE_DIR}/faiss/*.cpp)

set(faiss_lib Embedding)
add_library(${faiss_lib} STATIC ${faiss_cpu_headers} ${faiss_cpu_cpp})
target_link_libraries(${faiss_lib})

# flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -fPIC -m64 -Wall -g -O3  -msse4 -mpopcnt -fopenmp -Wno-sign-compare")
add_definitions(-DFINTEGER=int)

# executables
set(name faiss-cmd)
add_executable(${name} faiss-cmd.cpp)

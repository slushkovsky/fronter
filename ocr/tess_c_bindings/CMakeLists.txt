project(tesseract_test)
cmake_minimum_required(VERSION 2.8)

set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/modules)

find_package(Tesseract REQUIRED)
find_package(SWIG REQUIRED)
find_package(PythonLibs REQUIRED)

include(${SWIG_USE_FILE})

include_directories(${PYTHON_INCLUDE_PATH})
include_directories(${Tesseract_INCLUDE_DIR})

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_SWIG_FLAGS "")

SET_SOURCE_FILES_PROPERTIES(tess_c_api.i PROPERTIES CPLUSPLUS ON)
SET_SOURCE_FILES_PROPERTIES(tess_c_api.i PROPERTIES SWIG_FLAGS "-includeall")
SET_SOURCE_FILES_PROPERTIES(tess_c_api.i PROPERTIES SWIG_FLAGS "-cpperraswarn")

SWIG_ADD_MODULE(tess_c_api python tess_c_api.i tess_c_api.h tess_c_api.cpp)
SWIG_LINK_LIBRARIES(tess_c_api ${PYTHON_LIBRARIES} ${Tesseract_LIBRARY})

configure_file(tess_api.py tess_api.py COPYONLY)

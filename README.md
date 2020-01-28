[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?maxAge=3600)](https://raw.githubusercontent.com/mpusz/new-project-template/master/LICENSE)
[![Travis CI](https://img.shields.io/travis/com/mpusz/new-project-template/master.svg?label=Travis%20CI)](https://travis-ci.com/mpusz/new-project-template)
[![AppVeyor](https://img.shields.io/appveyor/ci/mpusz/new-project-template/master.svg?label=AppVeyor)](https://ci.appveyor.com/project/mpusz/new-project-template)

# `new_project` template

A template to start up a new C++ project with the support for:
- CMake
- Conan
- Travis CI
- AppVeyor


## Repository structure

This repository contains the following independent `cmake`-based projects:
 - `./src` - header-only project for `units`
 - `.` - project used for development needs that wraps `./src` project together with
   usage examples and unit tests
 - `./test_package` - library installation and Conan package verification
 
Please note that the projects depend on `cmake` git submodule in the `./cmake/common`
subdirectory.


## Building, testing, and installation

For a detailed information on project compilation, testing and reuse please refer to
[doc/INSTALL.md](doc/INSTALL.md).


## Steps to start a new project

1. Replace `mp` with the project namespace name in
  - `CMakeLists.txt` files
  - directory of project interface header files and source files including those
  - `INSTALL.md`
2. Replace `new_project` with new project name in all `CMakeLists.txt` files and quickly start
   a development of something really exciting :-)
3. Update `build.py` with proper packaging data


## Available Conan Options

| Option | Default | Values        | Description                         |
|--------|---------|---------------|-------------------------------------|
| shared | False   | [True, False] | Generates shared library            |
| fPIC   | True    | [True, False] | Generates position-independent code |


## Environment variables

| Option          | Default | Values        | Travis CI | AppVeyor | Description                                                             |
|-----------------|---------|---------------|-----------|----------|-------------------------------------------------------------------------|
| CONAN_RUN_TESTS | False   | [True, False] | True      | True     | Compiles all the tests and examples and runs unit tests during CI build |

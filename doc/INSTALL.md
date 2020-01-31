# Installation Guide

## Installation and Reuse

This library uses CMake to build a project and a Conan package manager to handle
dependencies and packaging. Although, Conan usage is still optional here, please note
that most probably CMake-only usage for more complicated projects will not be able to
scale enough to your needs. Typical sources of issues here are:
- not-CMake-based dependencies
- header-only libraries depending on non-header-only libraries
- problems with `find_package()` transitivity for projects with many levels of dependencies
- problems with handling/building/testing several configurations during project development
  (any mix of Debug/Release, x68/x68_64, gcc/clang/VS, etc)


### CMake only

To use this library as a CMake imported target via CMake configuration files the following
steps may be done:
- build and install only the library sources

  ```shell
  mkdir build && cd build
  cmake ../src -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=~/.local
  cmake --build . --target install
  ```

- link your CMake target with the library

  ```text
  find_package(new-project CONFIG REQUIRED)
  target_link_libraries(${PROJECT_NAME} PRIVATE mp::new-project)
  ```

### CMake + Conan

To use this library as a Conan imported target the following steps may be done:
- add the library as a dependency to your Conan configuration file
  - `conanfile.txt`
  
    ```text
    [requires]
    new-project/0.0.1@mpusz/stable
    ```

  - `conanfile.py`

    ```python
    requires = "new-project/0.0.1@mpusz/stable"
    ```

- link your CMake target with the library

  ```text
  target_link_libraries(<your_target> PUBLIC|PRIVATE|INTERFACE CONAN_PKG::new-project)
  ```

- install Conan dependencies before configuring CMake for the first time

  ```shell
  cd build
  conan install .. -pr <your_conan_profile> -b=outdated
  ```


## Full build and unit testing

In case you would like to build all the code in this repository (with unit tests and examples)
you should use the `CMakeLists.txt` from the parent directory and run Conan with
`CONAN_RUN_TESTS=True`.

```shell
mkdir build && cd build
conan install .. -pr <your_conan_profile> -e CONAN_RUN_TESTS=True -b outdated
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
ctest -VV
```


## Packaging

### Conan package creation and the verification of Conan and CMake packages

To create a Conan package the following step may be done:

```shell
conan create . <username>/<channel> -pr <your_conan_profile> -b outdated
```

### Above + Building unit tests and examples + Running unit tests

The following command will create a Conan package, verify the compilation of all the executable
files, and run the unit tests. Moreover, it will perform aforementioned compilation with a really
restrictive compilation warnings flags set.

```shell
conan create . <username>/<channel> -pr <your_conan_profile> -e CONAN_RUN_TESTS=True -b outdated
```


## Upload package to Conan server

To upload the package to a Conan server the following step may be done:

```shell
$ conan upload -r <remote-name> --all new-project/0.0.1@<user>/<channel>
```

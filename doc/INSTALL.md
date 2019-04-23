# Installation and Reuse

This library uses CMake to build a project and a Conan package manager to handle
dependencies and packaging. Although, Conan usage is still optional here, please note
that most probably CMake-only usage for more complicated projects will not be able to
scale enough for your needs. Typical sources of issues here are:
- not-CMake-based dependencies
- header-only libraries depending on non-header-only libraries
- problems with `find_package()` transitivity for projects with many levels of dependencies
- problems with handling/building/testing several configuration at once (any setup of
  Debug/Release, x68/x68_64, gcc/clang/VS, etc)


## CMake only

To use this library as a CMake imported target via CMake configuration files the following
steps may be done:
- download the repository
- build and install the project

  ```bash
  $ cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=~/.local
  $ cmake --build . --target install
  ```

- link your CMake target with the library

  ```text
  find_package(new_project CONFIG REQUIRED)
  target_link_libraries(${PROJECT_NAME} PRIVATE mp::new_project)
  ```

## CMake + Conan

To use this library as a Conan imported target the following steps may be done:
- add the library as a dependency to your Conan configuration file 
  - `conanfile.txt`
  
    ```text
    [requires]
    new_project/0.0.1@mpusz/stable
    ```
    
  - `conanfile.py`

    ```python
    requires = "new_project/0.0.1@mpusz/stable"
    ```

- link your CMake target with the library

  ```text
  target_link_libraries(<your_target> PUBLIC|PRIVATE|INTERFACE CONAN_PKG::new_project)
  ```

- install Conan dependencies before configuring CMake for the first time

  ```bash
  $ cd build
  $ conan install .. -pr <your_conan_profile> -b=outdated
  ```


# Full build and unit testing

In case you would like to build all the code in that repository (with unit tests and examples)
you should use `CMakeLists.txt` from the parent directory. 

```bash
mkdir build && cd build
conan install .. <your_profile_and_settings> -b outdated
cmake .. <your_cmake_configuration>
cmake --build .
ctest -VV
```


# Packaging

## Conan package creation and the verification of Conan and CMake packages

To create a Conan package the following step may be done:

```bash
$ conan create . <username>/<channel> -b=outdated <your_profile_and_settings>
```

## Above + Building unit tests and examples + Running unit tests

The following command will create a Conan package, verify the compilation of all the executable
files, and run the unit tests. Moreover, it will perform aforementioned compilation with a really
restrictive compilation warnings flags set.

```bash
$ conan create . <username>/<channel> -b=outdated <your_profile_and_settings> -e CONAN_RUN_TESTS=True
```


# Upload package to Conan server

To upload the package to a Conan server the following step may be done:

```bash
$ conan upload -r <remote-name> --all new_project/0.0.1@<user>/<channel>
```

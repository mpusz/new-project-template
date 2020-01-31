# The MIT License (MIT)
#
# Copyright (c) 2016 Mateusz Pusz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from conans import ConanFile, CMake, tools
import re


def get_version():
    try:
        content = tools.load("src/CMakeLists.txt")
        version = re.search(r"project\([^\)]+VERSION (\d+\.\d+\.\d+)[^\)]*\)", content).group(1)
        return version.strip()
    except Exception:
        return None


class NewProjectConan(ConanFile):
    name = "new-project"
    version = get_version()
    author = "Mateusz Pusz"
    license = "https://github.com/mpusz/new-project-template/blob/master/LICENSE"
    url = "https://github.com/mpusz/new-project-template"
    description = "A template to quickly start a new project"
    exports = ["LICENSE.md"]
    settings = "os", "compiler", "build_type", "arch"
    requires = ()
    options = {   # remove for a header-only library
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,    # remove for a header-only library
        "fPIC": True,       # remove for a header-only library
        "gtest:shared": False
    }
    scm = {
        "type": "git",
        "url": "auto",
        "revision": "auto",
        "submodule": "recursive"
    }
    generators = "cmake"

    @property
    def _run_tests(self):
        return tools.get_env("CONAN_RUN_TESTS", False)

    def _configure_cmake(self, folder="src"):
        cmake = CMake(self)
        if self.settings.compiler == "Visual Studio" and self.options.shared:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = True
        if self._run_tests:
            # developer's mode (unit tests, examples, restrictive compilation warnings, ...)
            cmake.configure()
        else:
            # consumer's mode (library sources only)
            cmake.configure(source_folder=folder, build_folder=folder)
        return cmake

    # def configure(self):
    #     tools.check_min_cppstd(self, "17")

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC   # remove for a header-only library

    def build_requirements(self):
        if self._run_tests:
            self.build_requires("gtest/1.10.0")

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        if self._run_tests:
            self.run("ctest -VV -C %s" % cmake.build_type, run_environment=True)

    def package(self):
        self.copy(pattern="*license*", dst="licenses", excludes="cmake/common/*", ignore_case=True, keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ['new_project']

    # uncomment for a header-only library
    # def package_id(self):
    #     self.info.header_only()

from conans import ConanFile, CMake, tools
from conans.tools import load
# from conans.errors import ConanInvalidConfiguration
import re


def get_version():
    try:
        content = load("src/CMakeLists.txt")
        version = re.search(r"project\([^\)]+VERSION (\d+\.\d+\.\d+)[^\)]*\)", content).group(1)
        return version.strip()
    except Exception:
        return None


class NewProjectConan(ConanFile):
    name = "new_project"
    version = get_version()
    author = "Mateusz Pusz"
    license = "https://github.com/mpusz/new_project_template/blob/master/LICENSE"
    url = "https://github.com/mpusz/new_project_template"
    description = "A template to quickly start a new project"
    exports = ["LICENSE.md"]
    settings = "cppstd", "os", "compiler", "build_type", "arch"
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

    # def configure(self):
    #     if self.settings.cppstd not in ["17", "gnu17", "20", "gnu20"]:
    #         raise ConanInvalidConfiguration("Library requires at least C++17 support")

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def build_requirements(self):
        if tools.get_env("CONAN_RUN_TESTS", False):
            self.build_requires("gtest/1.8.1@bincrafters/stable")

    def _configure_cmake(self):
        cmake = CMake(self)
        if self.settings.compiler == "Visual Studio" and self.options.shared:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = True
        if tools.get_env("CONAN_RUN_TESTS", False):
            cmake.configure()
        else:
            cmake.configure(source_dir="%s/src" % self.source_folder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        if tools.get_env("CONAN_RUN_TESTS", False):
            cmake.test()

    def package(self):
        self.copy(pattern="*license*", dst="licenses", excludes="cmake/common/*", ignore_case=True, keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ['new_project']
        self.cpp_info.includedirs = ['include']

    # uncomment for a header-only library
    # def package_id(self):
    #     self.info.header_only()

from conans import ConanFile, CMake

class NewProjectConan(ConanFile):
    name = "new_project"
    version = "0.0.1"
    author = "Mateusz Pusz"
    license = "https://github.com/mpusz/new_project_template/blob/master/LICENSE"
    url = "https://github.com/mpusz/new_project_template"
    description = "A template to quickly start a new project"
    settings = "os", "compiler", "build_type", "arch"
    build_requires = (
        "gtest/1.8.0@bincrafters/stable"
    )
    default_options = "gtest:shared=False"
    generators = "cmake_paths"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir="%s/src" % self.source_folder)
        cmake.build()
        # cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["new_project"]

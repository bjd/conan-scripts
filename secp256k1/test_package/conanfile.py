from conans import ConanFile, CMake
import os

# This easily allows to copy the package in other user or channel
channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "bjd")

class TestLibbitcoinSecp256k1Conan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "secp256k1/2016.12.28@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def test(self):
        # equal to ./bin/greet, but portable win: .\bin\greet
        self.run(os.sep.join([".","bin", "testlib"]))

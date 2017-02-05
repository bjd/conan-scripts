from conans import ConanFile

class LibSecp256k1Conan(ConanFile):
    name = "secp256k1"
    description = "Optimized C library for EC operations on curve secp256k1"
    version = "2016.12.28"
    url = "https://github.com/bitcoin-core/secp256k1"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("git clone https://github.com/bitcoin-core/secp256k1.git")
        self.run("cd secp256k1 && git checkout --detach 9d560f992db26612ce2630b194aef5f44d63a530")

    def build(self):
        self.run("mkdir _build")
        self.run("cd secp256k1 && ./autogen.sh -ivf && ./configure --prefix=$PWD/../_build --enable-module-recovery")
        self.run("cd secp256k1 && make -j8 && make install")

    def package(self):
        self.copy("*.h", dst="include", src="_build/include", links=True)
        self.copy("*.so*", dst="lib", src="_build/lib", links=True)
        self.copy("*.a", dst="lib", src="_build/lib", links=True)

    def package_info(self):
        self.cpp_info.libs = ["secp256k1"]

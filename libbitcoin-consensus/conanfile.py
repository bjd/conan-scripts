from conans import ConanFile

class LibbitcoinConsenusConan(ConanFile):
    name = "libbitcoin-consensus"
    description = "Bitcoin Consensus Library"
    version = "2.0.0"
    url = "https://github.com/bjd/conan-scripts.git"
    license = "AGPL-3.0"
    settings = "os", "compiler", "build_type", "arch"

    def configure(self):
        self.requires.add("secp256k1/2016.12.28@bjd/testing")
        self.requires.add("Boost/1.60.0@lasote/stable")

    def source(self):
        self.run("git clone https://github.com/libbitcoin/libbitcoin-consensus.git")
        self.run("cd libbitcoin-consensus && git checkout --detach v2.0.0")

    def build(self):
        configure_options  = " --with-boost=" + self.deps_cpp_info["Boost"].lib_paths[0] + "/.."
        configure_env  = " secp256k1_LIBS=-L" + self.deps_cpp_info["secp256k1"].lib_paths[0]
        configure_env += " secp256k1_CFLAGS=-I" + self.deps_cpp_info["secp256k1"].include_paths[0]
        self.run("mkdir _build")
        self.run("cd libbitcoin-consensus && ./autogen.sh -ivf && " + configure_env + " ./configure --prefix=$PWD/../_build " + configure_options)
        self.run("cd libbitcoin-consensus && make -j8 && make install")

    def package(self):
        self.copy("*", dst="include", src="_build/include", links=True)
        self.copy("*.so*", dst="lib", src="_build/lib", links=True)
        self.copy("*.a", dst="lib", src="_build/lib", links=True)

    def package_info(self):
        self.cpp_info.libs = ["bitcoin-consensus"]

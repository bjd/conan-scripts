from conans import ConanFile

class LibbitcoinConan(ConanFile):
    name = "libbitcoin"
    description = "Bitcoin Cross-Platform C++ Development Toolkit"
    version = "2.11.0"
    url = "https://github.com/bjd/conan-scripts.git"
    license = "AGPL-3.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "with_icu" : [True, False],
        "with_png" : [True, False],
        "with_qrencode" : [True, False]
    }
    default_options = "with_icu=False", \
                      "with_png=False", \
                      "with_qrencode=False"

    def configure(self):
        self.requires.add("secp256k1/2016.12.28@bjd/testing")
        self.requires.add("Boost/1.60.0@lasote/stable")
        if self.options.with_png:
            self.requires.add("libpng/1.6.23@lasote/stable")
        if self.options.with_icu:
            self.requires.add("icu/57.1@shinichy/stable")

    def source(self):
        self.run("git clone https://github.com/libbitcoin/libbitcoin.git")
        self.run("cd libbitcoin && git checkout --detach v2.11.0")

    def build(self):
        print(str(self.deps_cpp_info.lib_paths))
        configure_options  = " --enable-shared=no --with-examples=no"
        configure_options += " --with-boost=" + self.deps_cpp_info["Boost"].lib_paths[0] + "/.."
        configure_env  = " secp256k1_LIBS=-L" + self.deps_cpp_info["secp256k1"].lib_paths[0]
        configure_env += " secp256k1_CFLAGS=-I" + self.deps_cpp_info["secp256k1"].include_paths[0]
        if self.options.with_png:
            configure_options  += " --with-libpng"
            configure_env      += " -L" + self.deps_cpp_info["libpng"].lib_paths[0]
            configure_env      += " -I" + self.deps_cpp_info["libpng"].include_paths[0]
        if self.options.with_icu:
            configure_options  += " --with-icu"
            configure_env      += " icu_LIBS=-L" + self.deps_cpp_info["icu"].lib_paths[0]
            configure_env      += " icu_CFLAGS=-I" + self.deps_cpp_info["icu"].include_paths[0]
        self.run("mkdir _build")
        self.run("cd libbitcoin && ./autogen.sh -ivf && " + configure_env + " ./configure --prefix=$PWD/../_build " + configure_options)
        self.run("cd libbitcoin && make -j8 && make install")

    def package(self):
        self.copy("*", dst="include", src="_build/include", links=True)
        self.copy("*.so*", dst="lib", src="_build/lib", links=True)
        self.copy("*.a", dst="lib", src="_build/lib", links=True)

    def package_info(self):
        self.cpp_info.libs = ["bitcoin"]

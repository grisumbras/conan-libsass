import contextlib
from conans import (
    AutoToolsBuildEnvironment,
    ConanFile,
    tools,
)


class LibSassConan(ConanFile):
    name = "libsass"
    description = "A C/C++ implementation of a Sass compiler"
    author = "Dmitry Arkhipov <grisumbras@gmail.com>"
    license = "MIT"
    homepage = "https://sass-lang.com/libsass"
    url = "https://github.com/grisumbras/conan-libsass"
    default_user = "grisumbras"
    default_channel = "testing"

    settings = "arch", "os", "compiler", "build_type"
    options = {"shared": [False, True]}
    default_options = {"shared": False}
    exports = "LICENSE"

    def configure(self):
        del self.settings.compiler.cxxstd

    def source(self):
        url = "https://github.com/sass/libsass/archive/{version}.{ext}".format(
            version=self.version,
            ext=self._os_ext,
        )
        tools.get(url)

    def build(self):
        with self._build_context():
            autotools = AutoToolsBuildEnvironment(self)
            autotools.make(vars=self._fixed_vars(autotools))

    def package(self):
        with self._build_context():
            autotools = AutoToolsBuildEnvironment(self)
            vars = self._fixed_vars(autotools)
            autotools.install(vars=vars)
            autotools.make(target="install-headers", vars=vars)
        self.copy("LICENSE", src=self._src_subdir, dst="share/libsass")

    def package_id(self):
        del self.settings.compiler.libcxx

    def package_info(self):
        self.cpp_info.libs = ["sass"]
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["dl"]

    @property
    def _os_ext(self):
        return "zip" if tools.os_info.is_windows else "tar.gz"

    @property
    def _src_subdir(self):
        return "libsass-{}".format(self.version)

    def _fixed_vars(self, autotools):
        vars = autotools.vars
        for var in ["CXXFLAGS", "CFLAGS"]:
            vars[var] += " " + vars["CPPFLAGS"]
        return vars

    @contextlib.contextmanager
    def _build_context(self):
        env = { "PREFIX": self.package_folder }
        if self.options.shared:
            env["BUILD"] = "shared"
        with tools.environment_append(env):
            with tools.chdir(self._src_subdir):
                yield

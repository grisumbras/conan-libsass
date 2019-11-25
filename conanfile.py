import contextlib
from conans import (
    AutoToolsBuildEnvironment,
    ConanFile,
    tools,
)


class LibSassConan(ConanFile):
    name = 'libsass'
    description = "A C/C++ implementation of a Sass compiler"
    author = "Dmitry Arkhipov <grisumbras@gmail.com>"
    license = "MIT"
    homepage = "https://sass-lang.com/libsass"
    url = "https://github.com/grisumbras/conan-libsass"

    settings = "arch", "os", "compiler", "build_type"
    options = {"shared": [False, True]}
    default_options = {"shared": False}

    def source(self):
        url = "https://github.com/sass/libsass/archive/{version}.{ext}".format(
            version=self.version,
            ext=self._os_ext,
        )
        tools.get(url)

    def build(self):
        with self._build_context():
            autotools = AutoToolsBuildEnvironment(self)
            autotools.make()

    def package(self):
        with self._build_context():
            with tools.environment_append({"PREFIX": self.package_folder}):
                autotools = AutoToolsBuildEnvironment(self)
                autotools.install()
        self.copy("LICENSE", src=self._src_subdir,  dst="share/libsass")

    @property
    def _os_ext(self):
        return "zip" if self.settings.os == "Windows" else "tar.gz"

    @property
    def _src_subdir(self):
        return "libsass-{}".format(self.version)

    @contextlib.contextmanager
    def _build_context(self):
        if self.options.shared:
            env = tools.environment_append({"BUILD": "shared"})
        else:
            env = tools.no_op()
        with env:
            with tools.chdir(self._src_subdir):
                yield

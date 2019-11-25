from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(pure_c=True)
    builder.update_build_if(
        lambda build: build.settings["compiler"] == "clang",
        new_env_vars={"CC": "clang", "CXX": "clang++"},
    )
    builder.run()

from setuptools import setup, find_packages

with open("README.md", "rt") as f:
    setup(
        name="luarine",
        version='0.1',
        description="Lunar Client local api wrapper for Python",
        long_description=f.read(),
        long_description_content_type="text/markdown",
        url="https://github.com/voids-top/lunarine",
        author="NaeCqde",
        license="MIT",
        keywords="python lunarclient api",
        packages=find_packages()
    )

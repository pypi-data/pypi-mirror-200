import setuptools
import version

print("Building version: {}".format(version.__version__))

version = {}
with open("version.py") as fp:
    exec(fp.read(), version)

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
name="sayneng",
version=version['__version__'],
author="wangsayneng",
author_email="sayneng69@gmail.com",
description="This is a personal library.",
long_description="",
long_description_content_type="text/markdown",
url="",
packages=setuptools.find_packages(),
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
],
python_requires='>=3.7',
)

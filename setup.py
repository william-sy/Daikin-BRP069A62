import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dohpc",
    version = "1.2",
    author = "William",
    author_email = "None",
    description = ("Connect to the daikin lan adapter and control / read it"),
    license = "GPL-3.0-only",
    keywords = "daikin altherma heat pump ",
    url = "",
    packages=['dohpc'],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    install_requires=['websocket-client', 'dpath', 'ipaddress'],
    classifiers=[
        "Topic :: Utilities",
        "License :: GPL-3.0-only",
    ],
)

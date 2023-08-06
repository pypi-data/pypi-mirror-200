#coding:utf8
__author__ = 'dk'
import setuptools
long_desp = \
'''
A python lib to parse traffic flow information from pcaps.\n
Homepage : https://github.com/jmhIcoding/flowcontainer.\n
Fix bugs:\n
\t set the default filter string to be `tcp or udp or gre`.\n
\t update help information for errors. \n
\t supports ipv6 parse. \n
\t fix separator bugs, replace separator from '+' to '`'  \n
\t fix separator bugs, for http payload, the separator char would separate the payload wrongly.  \n
\t support extract the extended protocol name, e.g. TLSv1, TLSv2, IPSEC etc. \n
\t fix http payload bugs. \n
\t 2023-03-30: check the version of wireshark, ensure the version is not greater than 4.0.0. \n
'''

setuptools.setup(
    name="flowcontainer",
    version="6.4",
    author="Minghao Jiang",
    author_email="jiangminghao@iie.ac.cn",
    description="A python lib to parse traffic flow information from pcaps",
    url="https://github.com/jmhIcoding/flowcontainer",
    long_description=long_desp,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

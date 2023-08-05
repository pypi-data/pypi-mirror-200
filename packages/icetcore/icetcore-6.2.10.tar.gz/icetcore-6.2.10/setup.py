# -*- coding: utf-8 -*-
__author__ = 'ICE Technology'

import setuptools

setuptools.setup(
    name='icetcore',
    version="6.2.10",
    description='icetcore python api',
    author='zxlee',
    author_email='service@algostars.com',
    url='https://www.algostars.com.cn/',
    packages=setuptools.find_packages(exclude=["icetcore.sample.*"]),
    install_requires=["pywin32","psutil"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)
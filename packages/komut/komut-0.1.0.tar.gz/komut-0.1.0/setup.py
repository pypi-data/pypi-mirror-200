#! /usr/bin/env python3

import pathlib
import setuptools

root = pathlib.Path(__file__).resolve().parent
readme = (root / 'README.rst').read_text()

setuptools.setup(
    name='komut',
    version='0.1.0',
    description='A High-Magic CLI Framework',
    long_description=readme,
    long_description_content_type="text/x-rst",
    url='https://github.com/alpernebbi/komut',
    author='Alper Nebi Yasak',
    author_email='alpernebiyasak@gmail.com',
    license='GPL2+',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='cli command line interface',
    packages=setuptools.find_packages(),
    install_requires=[
        'setuptools',
    ],
)

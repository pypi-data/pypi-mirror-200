#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function
from glob import glob
import os
from os.path import join as pjoin
from setuptools import setup, find_packages


from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
    skip_if_exists
)

HERE = os.path.dirname(os.path.abspath(__file__))




# The name of the project
name = 'speechwidgets'

# Get the version
version = get_version(pjoin(name, '_version.py'))


# Representative files that should exist after a successful build
jstargets = [
    pjoin(HERE, name, 'nbextension', 'index.js'),
    pjoin(HERE, name, 'labextension', 'package.json'),
]


package_data_spec = {
    name: [
        'nbextension/**js*',
        'labextension/**'
    ]
}


data_files_spec = [
    ('share/jupyter/nbextensions/speechwidgets', 'speechwidgets/nbextension', '**'),
    ('share/jupyter/labextensions/speechwidgets', 'speechwidgets/labextension', '**'),
    ('share/jupyter/labextensions/speechwidgets', '.', 'install.json'),
    ('etc/jupyter/nbconfig/notebook.d', '.', 'speechwidgets.json'),
]


cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
    data_files_spec=data_files_spec)
npm_install = combine_commands(
    install_npm(HERE, build_cmd='build:prod'),
    ensure_targets(jstargets),
)
cmdclass['jsdeps'] = skip_if_exists(jstargets, npm_install)


setup_args = dict(
    name            = name,
    description     = 'A library with Jupyter widgets for speech processing',
    version         = version,
    scripts         = glob(pjoin('scripts', '*')),
    cmdclass        = cmdclass,
    packages        = find_packages(),
    author          = 'nicolvisser',
    author_email    = 'nicolvisser@yahoo.com',
    url             = 'https://github.com/nicolvisser/speechwidgets',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Jupyter', 'Widgets', 'IPython'],
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Jupyter',
    ],
    include_package_data = True,
    python_requires=">=3.6",
    install_requires = [
        'ipywidgets>=7.0.0',
        'ipykernel>=6.22.0',
        'jupyter_packaging>=0.12.3',
        'librosa>=0.8.0',
        'numpy>=1.0.0',
        'pytest>=7.2.2',
        'setuptools>=67.6.0',
        'Sphinx>=6.1.3',
        'sphinx_rtd_theme>=1.2.0',
        'traitlets>=5.9.0',
        'traittypes>=0.2.1'
    ],
    extras_require = {
        'test': [
            'pytest>=4.6',
            'pytest-cov',
            'nbval',
        ],
        'examples': [
            # Any requirements for the examples to run
        ],
        'docs': [
            'jupyter_sphinx',
            'nbsphinx',
            'nbsphinx-link',
            'pytest_check_links',
            'pypandoc',
            'recommonmark',
            'sphinx>=1.5',
            'sphinx_rtd_theme',
        ],
    },
    entry_points = {
    },
)

if __name__ == '__main__':
    setup(**setup_args)

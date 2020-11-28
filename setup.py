#!/usr/bin/env python
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from viewwork/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version('viewwork', '__init__.py')
readme = open('README.md').read()
requirements = open('requirements/base.txt').readlines()
require_select2 = open('requirements/select2.txt').readlines()
require_all = requirements + require_select2

setup(
    name='django-viewwork',
    version=version,
    description='Collect views, generate urls and create menu',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Sergei Pikhovkin',
    author_email='s@pikhovkin.ru',
    url='https://github.com/pikhovkin/django-viewwork',
    packages=[
        'viewwork',
    ],
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'all': require_all,
        'select2': require_select2,
    },
    python_requires='>=3.8.*, <4.0.*',
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

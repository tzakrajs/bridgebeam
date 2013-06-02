#!/usr/bin/env python

import bridgebeam

from setuptools import setup, find_packages

setup(
        name='bridgebeam',
        version=bridgebeam.__version__,

        description='a simple conference bridge solution using Twiio',
        long_description=open('README.rst').read(),

        author='Thomas Zakrajsek',
        author_email='tzakrajs@gmail.com',

        url='https://github.com/tzakrajs/bridgebeam',

        scripts=['run_server.py', ],

        include_package_data=True,
        packages=['bridgebeam'],
        package_dir={'bridgebeam': 'bridgebeam'},
        package_data={'bridgebeam': ['views/*.tpl',
                                     'static/js/*.js',
                                     'static/css/*.css',
                                     'static/img/*.png',
                                     'static/img/*.gif']},

        license=open('LICENSE').read(),

        install_requires=[
                    'twilio == 3.5.1',
                ],

        keywords='twilio conference bridge',
        classifiers=[
                    'Development Status :: 3 - Alpha',
                    'Programming Language :: Python',
                    'Programming Language :: Python :: 2.7',
                    'Framework :: Bottle',
                    'Operating System :: OS Independent',
                    'Environment :: Console',
                    'Intended Audience :: Information Technology',
                    'Natural Language :: English',
                    'Topic :: Communications :: Telephony',
                    'License :: OSI Approved :: Apache Software License',
                ],
)

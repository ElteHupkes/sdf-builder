#!/usr/bin/env python
from distutils.core import setup

setup(name='sdfbuilder',
      version=0.2,
      description='Pragmatic utility library for building SDF files',
      author='Elte Hupkes',
      author_email='elte@hupkes.org',
      url='https://github.com/ElteHupkes/sdf-builder',
      packages=['sdfbuilder', 'sdfbuilder.joint', 'sdfbuilder.sensor', 'sdfbuilder.math',
                'sdfbuilder.physics', 'sdfbuilder.structure', 'sdfbuilder.util'],
      install_requires=['numpy'])

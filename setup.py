#!/usr/bin/env python
from distutils.core import setup

setup(name='sdfbuilder',
      version=0.1,
      description='Pragmatic utility library for building SDF files',
      author='Elte Hupkes',
      author_email='elte@hupkes.org',
      url='https://github.com/ElteHupkes/sdf-builder',
      packages=['sdfbuilder', 'sdfbuilder.base', 'sdfbuilder.joint', 'sdfbuilder.math',
                'sdfbuilder.physics', 'sdfbuilder.structure', 'sdfbuilder.util'],
      requires=['numpy'])

#!/usr/bin/env python

from distutils.core import setup

setup(name='wxslack',
      version='1.0',
      description='slack and wechat bidirectional sync',
      author='Zhongke Chen',
      author_email='ch3n2k@gmail.com',
      url='https://ch3n2k.com',
      packages=['wxslack'],
      scripts=['script/wxslack'
     )

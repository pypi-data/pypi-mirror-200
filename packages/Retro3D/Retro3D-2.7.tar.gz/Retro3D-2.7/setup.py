from setuptools import setup, find_packages
import os 

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Retro3D',
  version='2.7',
  description='3D Game Engine with software rendering written in Python',
  long_description_content_type='text/markdown',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
  url='',  
  author='Deepak Deo',
  author_email='deepakbr14@yahoo.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='3d game engine software rendering python', 
  packages=find_packages(),
  package_data={'': ['*.png', '*.ttf'],},
  include_package_data=True,
  install_requires=['numpy', 'pygame', 'numba'],
)



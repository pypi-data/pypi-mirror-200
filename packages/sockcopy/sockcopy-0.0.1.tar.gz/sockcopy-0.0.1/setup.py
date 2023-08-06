from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='sockcopy',
  version='0.0.1',
  description='Package for sending and receiving files over socket connections',
  url='',  
  author='Erasmus A. Junior',
  author_email='eirasmx@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='socketcopy',
  packages=find_packages(),
  install_requires=[''] 
)
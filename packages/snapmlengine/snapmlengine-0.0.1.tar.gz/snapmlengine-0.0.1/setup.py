from setuptools import setup, find_packages
 
setup(
  name='snapmlengine',
  version='0.0.1',
  description='ML Dashboard',
  long_description='Code generating code',
  url='https://github.com/midnightbot/snapmlengine',  
  author='Anish Adnani',
  author_email='anishadnani00@gmail.com',
  license='MIT', 
  keywords=['python', 'coding', 'ml', 'algorithms'],
  packages=find_packages(),
  install_requires=['snapalgo'] ,
  classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
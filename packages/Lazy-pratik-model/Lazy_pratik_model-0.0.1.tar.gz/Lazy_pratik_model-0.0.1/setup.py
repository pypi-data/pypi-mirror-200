from setuptools import find_packages,setup
from typing import List

classifiers = [  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
  ]


setup(
    name='Lazy_pratik_model',
    version='0.0.1',
    description='This package directly gives you output performance on different models',
    url='',
    license='MIT',
    long_description= open('ChangeLog.txt').read(),
    author='pratik',
    classifiers=classifiers,
    author_email='pratikvdatey@gmail.com',
    keywords='Lazy_pratik_model',
    packages=find_packages(),
    install_requires=['sklearn','lightgbm','catboost','xgboost'],
    Source = "https://github.com/pratikdatey/Lazy_pratik_model"
   
)

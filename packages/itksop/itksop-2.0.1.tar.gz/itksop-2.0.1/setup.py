# -*- encoding: utf-8 -*-
'''
Description:  PyPI     
@created   : 2022/09/28 20:25
'''

from setuptools import setup 

setup(
    name="itksop",
    version="2.0.1",
    author="Shudong Wang",
    author_email="wangsd@ihep.ac.cn",
    description="ATLAS ITk SOP",
    packages=['itksop'],
    install_requires=[
      'streamlit',
      'itkdb',
      'st-annotated-text',
      'matplotlib',
      'scikit-spatial',
      'maskpass',
      'plotly',
      'plotly-express'
      ], 
    license='MIT',
    classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
    ]
	)

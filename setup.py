from setuptools import setup

setup(name='WhatInstalled',
	version='0.1',
	description='A simple tool to retrieve what you installed using CLI',
	url='http://github.com/AlexMili/whatinstalled',
	author='AlexMili',
	license='MIT',
	zip_safe=True,
	entry_points={
		'console_scripts': [
			'whatinstalled = whatinstalled:whatinstalled',
		]
	}
)

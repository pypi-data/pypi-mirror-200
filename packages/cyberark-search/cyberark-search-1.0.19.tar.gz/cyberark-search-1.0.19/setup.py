from setuptools import setup

requirements_list = [
	'certifi',
	'charset-normalizer',
	'click',
	'colorama',
	'enum34',
	'idna',
	'pexpect',
	'ptyprocess',
	'urllib3',
	'pypass',
	'requests',
]

setup(
	name='cyberark-search',
    	version='1.0.19',    
    	description='CyberArk Search: Search for accounts and retrieve their passwords in the CyberArk elevated access management application. You can only retrieve accounts that you are able to view.',
    	url='https://github.com/mjackstewart1/cyberark-search',
    	author='Jack Stewart',
    	author_email='mjstew@umich.edu',
    	license='Unilicense',
    	packages=['cyberark-search'],
	setup_requires=requirements_list,
    	install_requires=requirements_list,

	classifiers=[
		'Development Status :: 1 - Planning',
		'Intended Audience :: Information Technology',
		'License :: Free for non-commercial use',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 3',
	],

	scripts=[
		'scripts/cyberark-search.py',
	],
)


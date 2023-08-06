#!/usr/bin/env python3

import argparse
import os
import platform
import subprocess
import sys
import sysconfig

COMMAND_LINUX = 'python'
COMMAND_SKYNET = '/usr/local/mcomm/cs_venv/bin/python'
COMMAND_WINDOWS = 'python.exe'
HOSTNAME = platform.node().split('.', 1)[0].lower()
OS_NAME = platform.system()
PYTHON_SITE_PACKAGES = sysconfig.get_path('purelib')
SCRIPT_LINWIN = 'cyberark-search/cyberark-search-script.py'
SCRIPT_SKYNET =  '/usr/local/mcomm/cs_venv/lib/python3.7/site-packages/cyberark-search/cyberark-search-script.py'

def get_arguments():
	command_params_list = []
	
	if len(sys.argv) > 1:
		parser = argparse.ArgumentParser(description='CyberArk Search: Search for accounts and retrieve their passwords in the CyberArk elevated access management application. You can only retrieve accounts that you are able to view.')
		
		parser.add_argument('--uniqname', '-u', type=str, required=True, help='Your uniqname')
		parser.add_argument('--password', '-p', type=str, required=True, help='Your UMICH Level 1 password')
		
		args = parser.parse_args()
		
		username = args.uniqname
		password = args.password
		
		command_params_list.append('--uniqname')
		command_params_list.append(f'{username}')
		command_params_list.append('--password')
		command_params_list.append(f'{password}')
	
	return command_params_list

def main():
	if HOSTNAME == 'skynet':
		command = COMMAND_SKYNET
		script = SCRIPT_SKYNET
	else:	
		if OS_NAME == 'Linux':
			command = COMMAND_LINUX	
			script = PYTHON_SITE_PACKAGES + '/' + SCRIPT_LINWIN
		elif OS_NAME.startswith('Windows'):
			command = COMMAND_WINDOWS
			script = PYTHON_SITE_PACKAGES.replace('\\', '/') + '/' + SCRIPT_LINWIN
		else:
			print(f'{OS_NAME} is not a valid OS')
			print('Exiting ...')
			exit(1)

		if not(os.path.isfile(script)):
			print()
			print('Cannot find the script:') 
			print(f'{script}')
			print('This is the path to site-packages:')
			print(f'{PYTHON_SITE_PACKAGES}')
			print('Exiting ...')
			print()
			exit(1)

	command_list = [command, script]
	command_params_list = get_arguments()
	subprocess.run(command_list + command_params_list)
		
if __name__ == "__main__":
	main()
	

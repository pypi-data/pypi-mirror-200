# -----------------------------------------------------------------------------
import os
from nettoolkit import Validation, STR, Multi_Execution, addressing, IPv4

from .conection import Execute_Device

# -----------------------------------------------------------------------------

class Execute_By_Login(Multi_Execution):
	"""Execute the device capture by logging in to device.

	"""    	

	def __init__(self, 
		ip_list, 
		auth, 
		cmds, 
		path, 
		cumulative=False, 
		forced_login=False, 
		parsed_output=False,
		concurrent_connections=100,
		):
		"""Initiatlize the connections for the provided iplist, authenticate with provided auth parameters, and execute given commands.

		Args:
			ip_list (set, list, tuple): set of ip addresses to be logging for capture
			auth (dict): authentication parameters ( un, pw, en)
			cmds (set, list, tuple): set of commands to be captured
			path (str): path where output should be stored.
			cumulative (bool, optional): True: will store all commands output in a single file, 
				False will store each command output in differet file. Defaults to False.
				and 'both' will do both.
			forced_login (bool, optional): True: will try to ssh/login to devices even if ping respince fails.
				False will try to ssh/login only if ping responce was success. (default: False)
			parsed_output (bool, optional): True: will check the captures and generate the general parsed excel file.
				False will omit this step. No excel will be generated in the case. (default: False)
			concurrent_connections (int, optional): 100: manipulate how many max number of concurrent connections to be establish.
				default is 100.

		Raises:
			Exception: raise exception if any issue with authentication or connections.
		"""    		
		self.devices = STR.to_set(ip_list) if isinstance(ip_list, str) else set(ip_list)
		self.auth = auth
		if not isinstance(cmds, dict):
			raise Exception("commands to be executed are to be in proper dict format")
		self.cmds = cmds
		self.path = path
		self.cumulative = cumulative
		self.forced_login = forced_login
		self.parsed_output = parsed_output
		if parsed_output and not cumulative :
			self.cumulative='both'
		super().__init__(self.devices)
		try:
			self.max_connections = concurrent_connections
		except:
			print(f"Invalid number of `concurrent_connections` defined {concurrent_connections}, default 100 taken.")
		self.start()
		# self.end()

	def is_valid(self, ip):
		"""Validation function to check if provided ip is valid IPv4 or IPv6 address

		Args:
			ip (str): ipv4 or ipv6 address

		Returns:
			bool: True/False based on validation success/fail
		"""    		
		try:
			return ip and Validation(ip).version in (4, 6)
		except:
			print(f'Device Connection: {ip} :: Skipped due to bad Input')
			return False
		return True

	def execute(self, hn):
		"""execution function for a single device. hn == ip address in this case.

		Args:
			hn (str): ip address of a reachable device
		"""    		
		Execute_Device(hn, 
			auth=self.auth, 
			cmds=self.cmds, 
			path=self.path, 
			cumulative=self.cumulative,
			forced_login=self.forced_login, 
			parsed_output=self.parsed_output,
			)



class Execute_By_Individual_Commands(Multi_Execution):
	"""Execute the device capture by logging in to device and running individual commands on to it.

	"""    	

	def __init__(self, 
		auth, 
		dev_cmd_dict,
		op_path='.', 
		cumulative=False, 
		forced_login=False, 
		parsed_output=False,
		concurrent_connections=100,
		):
		"""Initiatlize the connections for the provided iplist, authenticate with provided auth parameters, and execute given commands.

		Args:
			auth (dict): authentication parameters ( un, pw, en)
			op_path (str): path where output should be stored.
			dev_cmd_dict: dictionary of list {device_ip:[commands list,]}
			cumulative (bool, optional): True: will store all commands output in a single file, 
				False will store each command output in differet file. Defaults to False.
				and 'both' will do both.
			forced_login (bool, optional): True: will try to ssh/login to devices even if ping respince fails.
				False will try to ssh/login only if ping responce was success. (default: False)
			parsed_output (bool, optional): True: will check the captures and generate the general parsed excel file.
				False will omit this step. No excel will be generated in the case. (default: False)
			concurrent_connections (int, optional): 100: manipulate how many max number of concurrent connections to be establish.
				default is 100.

		Raises:
			Exception: raise exception if any issue with authentication or connections.
		"""
		#
		self.add_auth_para(auth)
		self.verify_dev_cmd_dict(dev_cmd_dict)
		self.add_devices(dev_cmd_dict)
		self.individual_device_cmds_dict(dev_cmd_dict)
		#
		self.path = op_path
		self.cumulative = cumulative
		self.forced_login = forced_login
		self.parsed_output = parsed_output
		if parsed_output and not cumulative :
			self.cumulative='both'
		super().__init__(self.devices)
		try:
			self.max_connections = concurrent_connections
		except:
			print(f"Invalid number of `concurrent_connections` defined {concurrent_connections}, default 100 taken.")
		self.start()
		# self.end()

	def add_auth_para(self, auth):
		if not isinstance(auth, dict):
			raise Exception(f"authentication parameters needs to be passed as dictionary")
		if not auth.get('un') or auth['un'] == '':
			raise Exception(f"authentication parameters missing with username `un`")
		if not auth.get('pw') or auth['pw'] == '':
			raise Exception(f"authentication parameters missing with password `pw`")
		if not auth.get('en') or auth['en'] == '':
			auth['en'] = auth['pw']
		self.auth = auth

	def verify_dev_cmd_dict(self, dev_cmd_dict):
		if not isinstance(dev_cmd_dict, dict):
			raise Exception(f"`capture_individual` requires `dev_cmd_dict` parameter in dictionary format")
		for ip, cmds in dev_cmd_dict.items():
			if isinstance(ip, (tuple, set)):
				for x in ip:
					if not isinstance(addressing(x), IPv4):
						raise Exception(f"`dev_cmd_dict` key expecting IPv4 address, received {ip}")
			elif isinstance(ip, str) and not isinstance(addressing(ip), IPv4):
				raise Exception(f"`dev_cmd_dict` key expecting IPv4 address, received {ip}")
			if not isinstance(cmds, (list, set, tuple, dict)):
				raise Exception(f"`dev_cmd_dict` values expecting iterable, received {cmds}")

	def add_devices(self, dev_cmd_dict):
		devs = set()
		for ip, cmds in dev_cmd_dict.items():
			if isinstance(ip, (tuple, set)):
				for x in ip:
					devs.add(x)
			elif isinstance(ip, str):
				devs.add(ip)
		self.devices = devs

	def is_valid(self, ip):
		"""Validation function to check if provided ip is valid IPv4 or IPv6 address

		Args:
			ip (str): ipv4 or ipv6 address

		Returns:
			bool: True/False based on validation success/fail
		"""    		
		try:
			return ip and Validation(ip).version in (4, 6)
		except:
			print(f'Device Connection: {ip} :: Skipped due to bad Input')
			return False
		return True

	def execute(self, ip):
		"""execution function for a single device. hn == ip address in this case.

		Args:
			ip (str): ip address of a reachable device
		"""
		Execute_Device(ip, 
			auth=self.auth, 
			cmds=sorted(self.dev_cmd_dict[ip]), 
			path=self.path, 
			cumulative=self.cumulative,
			forced_login=self.forced_login, 
			parsed_output=self.parsed_output,
			)

	def individual_device_cmds_dict(self, dev_cmd_dict):
		self.dev_cmd_dict = {}
		for device in self.devices:
			if not self.dev_cmd_dict.get(device):
				self.dev_cmd_dict[device] = set()
			for ips, cmds in dev_cmd_dict.items():
				if isinstance(ips, (tuple, set, list)):
					for ip in ips:
						if device == ip:
							self.add_to(ip, cmds)
				if isinstance(ips, str):
					if device == ips:
						self.add_to(ips, cmds)


	def add_to(self, ip, cmds):
		cmds = set(cmds)
		self.dev_cmd_dict[ip] = self.dev_cmd_dict[ip].union(cmds)


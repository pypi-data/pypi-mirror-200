"""pyVig Excel Preparation -  A Single Device Cabling Details.
"""

import pandas as pd
from .general import drop_empty
# --------------------------------------------- 

DEFAULT_CONNECTOR_TYPE = 'straight'  ## other options = 'curved', 'angled'
DEFAULT_LINE_COLOR = 'blue'
DEFAULT_LINE_WT = 3
DEFAULT_LINE_PATTERN = 1
# --------------------------------------------- 
class ADevCablings():
	"""A single Device Cabling details
	"""	

	def __init__(self, self_device, **kwargs):
		"""Object Initializer for A single device cabling details.

		Args:
			self_device (str): device hostname (self)
		"""		
		self.self_device = self_device
		self.cablings = {}
		self.cablings['a_device'] = []
		self.cablings['a_device_port'] = []
		self.cablings['b_device'] = []
		self.cablings['dev_b_port'] = []
		self.cabling_mandatory_columns = set(self.cablings.keys())
		self.cabling_optional_columns = {'connector_type', 'color', 'weight', 'pattern'}
		self.connector_type, self.color, self.weight, self.pattern = DEFAULT_CONNECTOR_TYPE, DEFAULT_LINE_COLOR, DEFAULT_LINE_WT, DEFAULT_LINE_PATTERN 
		self.update_attrib(**kwargs)

	def update_attrib(self, **kwargs):
		"""update object attributes
		"""
		for k, v in kwargs.items():
			if v is not None:
				self.__dict__[k] = v

	def add_to_cablings(self, **kwargs):
		"""add provided keyword arguments to cablings (dictionary)
		"""
		mandatory_col_maps = {
			'b_device': 'nbr_hostname' ,
			'a_device_port': 'interface',
			'dev_b_port': 'nbr_interface',
		}
		#
		for k in self.cablings:
			if k == 'a_device':
				self.cablings[k].append(self.self_device)
			elif k in self.cabling_mandatory_columns:
				try:
					self.cablings[k].append(kwargs[mandatory_col_maps[k]])
				except:
					self.cablings[k].append("")
					if k != 'b_device':
						print(f"Mandatory requirement missing, df gen may fails {k}")

		for k in self.cabling_optional_columns:
			try:
				if k in kwargs:
					if k not in self.cablings:
						self.cablings[k] = []
					self.cablings[k].append(kwargs[k])
				# else set detaults ------
				elif k == 'connector_type':
					self.cablings[k].append(self.connector_type)
				elif k == 'color':
					self.cablings[k].append(self.color)
				elif k == 'weight':
					self.cablings[k].append(self.weight)
				elif k == 'pattern':
					self.cablings[k].append(self.pattern)
			except:
				if k not in self.cablings:
					self.cablings[k] = []
				self.cablings[k].append("")

	def cabling_dataframe(self):
		"""generate the dataframe for the cablings details captured in cablings dictionary of self.

		Returns:
			DataFrame: Pandas DataFrame object
		"""
		df =  pd.DataFrame(self.cablings)
		df = drop_empty(df, column='b_device')
		return df

# --------------------------------------------- 


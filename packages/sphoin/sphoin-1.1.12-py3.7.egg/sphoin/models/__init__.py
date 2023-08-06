"""Models module."""

__author__ = "pom11"
__copyright__ = "Copyright 2022, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "1.1.12"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

class Ohlcv:
	"""
Ohlcv class

Attributes
----------
date : list
	List of dates
open : list
	List of open values
high : list
	List of high values
low : list
	List of low values	
close : list
	List of close values
volume : list
	List of volume values
	"""
	def __init__(self,**kwargs) -> None:
		self.date : list = kwargs['date']
		self.open : list = kwargs['open']
		self.high : list = kwargs['high']
		self.low : list = kwargs['low']
		self.close : list = kwargs['close']
		self.volume : list = kwargs['volume']

class Study:
	"""
Study class

Attributes
----------
crt : str
	Study index number
name : str
	Study custom name
study : str
	Study name
	['U|D','M|M','X','---','[ ]']
description : str
	Study description
code : str
	Study code
	['#1','#2','#3','#4','#5']
normalize : bool
	True if values are normalized and False if not
inverse : bool
	True if resulting signals are inversed and False is not
config : dict
	StudyConfig
result : list
	List of resulted signals
	"""
	def __init__(self,**kwargs) -> None:
		self.crt : str = kwargs['crt']
		self.name : str = kwargs['name']
		self.study : str = kwargs['study']
		self.code : str = kwargs['code']
		self.description : str = kwargs['description']
		self.normalize : bool = kwargs['normalize']
		self.inverse : bool = kwargs['inverse']
		self.config : dict = StudyConfig(**kwargs['config'])
		self.result : list = list(kwargs['result'].values())

class StudyConfig:
	"""
StudyConfig class

Attributes
----------
indicator_1: Indicator
indicator_2: Indicator
	None: If the Study uses only 1 technical indicator or pattern
	"""
	def __init__(self,**kwargs) -> None:
		self.indicator_1 : Indicator = None
		self.indicator_2 : Indicator = None
		for x in kwargs.keys():
			if x not in ['raw','PASSS']:
				if self.indicator_1 == None:
					data = kwargs[x]
					data['name'] = x
					data['raw'] = kwargs['raw'][x]
					self.indicator_1 : Indicator = Indicator(**data)
				elif self.indicator_2 == None:
					data = kwargs[x]
					data['name'] = x
					data['raw'] = kwargs['raw'][x]
					self.indicator_2 : Indicator = Indicator(**data)
			elif x == 'PASSS':
				self.indicator_2 : Indicator = None

class Indicator:
	"""
Indicator class
	Technical indicator or pattern

Attributes
----------
name : str
	name
info : IndicatorInfo
min_threshold : MinMaxThreshold
max_threshold : MinMaxThreshold
parameters : list
	List of IndicatorParameters
raw : list
	List of raw values of technical indicator or pattern
	"""
	def __init__(self,**kwargs) -> None:
		self.name : str = kwargs['name']
		self.info : IndicatorInfo = IndicatorInfo(**kwargs['info'])
		self.min_threshold : MinMaxThreshold = MinMaxThreshold(**kwargs['min_threshold'])
		self.max_threshold : MinMaxThreshold = MinMaxThreshold(**kwargs['max_threshold'])
		self.parameters : list = [IndicatorParameter(**kwargs[x]) for x in kwargs.keys() if x not in ['min_threshold','max_threshold','raw','name','info']]
		self.raw : list = list(kwargs['raw'].values())

class IndicatorInfo:
	"""
IndicatorInfo
	Detailed info of technical indicator or pattern

Attributes
----------
display_name : str
name : str
group : str
function_flags : list
input_names : dict
output_flags : dict
	"""
	def __init__(self,**kwargs) -> None:
		self.display_name : str = kwargs['display_name']
		self.name : str = kwargs['name']
		self.group : str = kwargs['group']
		self.function_flags : list = kwargs['function_flags']
		self.input_names : dict = kwargs['input_names']
		self.output_flags : dict = kwargs['output_flags']
		# self.parameters : dict = kwargs['parameters']

class MinMaxThreshold:
	"""
MinMaxThreshold class
	Used for study code #2

Attributes
----------
display_name : str
value : int
	Custom value to filter indicator raw values
default_value : int
	Values used if custom value is not set
help : str
	"""
	def __init__(self,**kwargs) -> None:
		self.display_name : str = kwargs['display_name']
		self.default_value : int = int(kwargs['default_value'])
		self.help : str = kwargs['help']
		self.value : int = kwargs['value']

class IndicatorParameter:
	"""
IndicatorParameter class

Attributes
----------
name : str
display_name : str
help : str
type : int
	Type value of technical indicator or pattern
	values : 
		0 - float value
		2 - int value
		3 - int value
value : float or int
default_value : float or int
	"""
	def __init__(self,**kwargs) -> None:
		self.name : str = kwargs['name']
		self.display_name : str = kwargs['display_name']
		self.help : str = kwargs['help']
		self.type : int = int(kwargs['type'])
		if self.type == 0:
			self.default_value : float = kwargs['default_value']
			self.value : float = kwargs['value']
		elif self.type == 2 or self.type == 3:
			self.default_value : int = kwargs['default_value']
			self.value : int = kwargs['value']



"""Plot module."""

__author__ = "pom11"
__copyright__ = "Copyright 2023, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "1.2.0"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

def isNumber(n):
	return not n == None

plot_lines = {
	"light":{
		"curved":{
			"horizontal": u'\u2500',
			"vertical": u'\u2502',
			"up_right": u'\u2570',
			"down_right": u'\u256D',
			"left_down": u'\u256E',
			"left_up": u'\u256F',
		},
		"angular":{
			"horizontal": u'\u2500',
			"vertical": u'\u2502',
			"up_right": u'\u2514',
			"down_right": u'\u250C',
			"left_down": u'\u2510',
			"left_up": u'\u2518'
		},
	},
	"heavy":{
		"angular":{
			"horizontal": u'\u2501',
			"vertical": u'\u2503',
			"up_right": u'\u2517',
			"down_right": u'\u250F',
			"left_down": u'\u2513',
			"left_up": u'\u251B'
		},
		"cross":{
			"full":{
				"light_horizontal": u'\u2542',
				"light_vertical": u'\u253F',
				"light_up_right": u'\u2545',
				"light_left_down": u'\u2544',
				"light_left_up": u'\u2546',
				"light_down_right": u'\u2543'
			},
			"vertical":{
				"light_rigth": u'\u2520',
				"ligth_left": u'\u2528',
				"left_down": u'\u252A',
				"left_up": u'\u2529',
				"up_right": u'\u2521',
				"down_right": u'\u2522'
			},
			"horizontal":{
				"light_up": u'\u2537',
				"light_down": u'\u252F',
				"left_down": u'\u2531',
				"left_up": u'\u2539',
				"up_right": u'\u253A',
				"down_right": u'\u2532'
			}
		}
	}
}

import datetime
from dateutil import tz
from sphoin.models import Ohlcv, Study
from sphoin.app import Slot
from math import floor, ceil

class Plot:
	"""
Plot module for sphoin.app Slots

Methods
-------
line
    Generate an ascii chart for a series of numbers
study_bar
    Generate an ascii bar chart for a series of numbers
time_bar
    Generate an ascii time bar for a series of numbers
	"""

	def line(
		series: list,
		signals: list,
		min_flag: int,
		max_flag: int,
		color1: str = '45', 
		color2: str = '46',
		sizeY: int = 200, 
		sizeX: int = 50,
		signal_as_line: bool = False,
		dark_theme: bool = True) -> str:

		"""
Generate an ascii chart for a series

Parameters
----------
series : list
    List of values to chart
signals : list
    List of signals corresponding to each series element
min_flag : int
    Filter signals lower or equal with min_flag
max_flag : int
	Filter signals bigger or equal with max_flag
color1 : str
	Ansi color code for min_flag signals 
	Default = '45'
	[40,41,42,43,44,45,46,47,49]
color2 : str
	Ansi color code for max_flag signals
	Default = '46'
	[40,41,42,43,44,45,46,47,49]
sizeY : int
	Height of chart plot
	Default = 200
	Constraints
		min = 4
		max = 200
sizeX : int
	Width of chart plot
	Default = 50
	Contraints
		min = 50
		max = 500
signal_as_line : bool
	Plots signal as vertical line (True) or dot (False)
	Default = False
dark_theme : bool
	Theme of chart plot
	Default = True

Returns
------
str
	Ansi chart
		"""

		if len(series) == 0:
			return ''
		
		if sizeY < 4:
			sizeY = 4
		elif sizeY > 200:
			sizeY = 200
		if sizeX < 50:
			sizeX = 50
		elif sizeX > 500:
			sizeX = 500

		sizeY -= 1
		line_type = "curved"
		line_color = "37" if dark_theme else "30"
		background_color = "40" if dark_theme else "47"

		offset = 1
		if not isinstance(series[0],list):
			if all(not isNumber(n) for n in series):
				return ''
			else:
				series = [series[-sizeX+11:]]
		else:
			line_type = "angular"
			series = [x[-sizeX+11:] for x in series]

		signals = signals[-sizeX+11:]
		minimum = min(filter(isNumber, [y for x in series for y in x]))
		maximum = max(filter(isNumber, [y for x in series for y in x]))
		interval = abs(float(maximum) - float(minimum))
		interval = 0.1 if interval == 0 else interval
		ratio = (sizeY) / interval
		intmin2 = int(round(float(minimum) * ratio))
		intmax2 = int(round(float(maximum) * ratio))

		rows = abs(intmax2 - intmin2)

		width = 0
		for i in range(0,len(series)):
			width = max(width, len(series[i]))
		width += offset

		result = [[f'\x1b[{background_color};{line_color}m'+u'\u0020'+'\x1b[0m'] * (width-offset) for i in range(rows+1)]

		for y in range(intmin2, intmax2 + 1):
			try:
				label = '{:8.9f}'.format(float(maximum) - ((y - intmin2) * interval / rows))[:11]
			except Exception as e:
				label = '{:8.9f}'.format(0)
			result[y - intmin2][max(offset - len(label), 0)] = f'\x1b[{background_color};{line_color}m'+label+u'\u2524'

		
		for i in range(0, len(series)):
			font_weight =["light","heavy"][i]
			for x in range(0, len(series[i])-1):
				y0 = int(round(series[i][x + 0] * ratio) - intmin2)
				y1 = int(round(series[i][x + 1] * ratio) - intmin2)
				if y0 == y1:
					horizontal = plot_lines[font_weight][line_type]["horizontal"]
					if i == 1:
						if plot_lines["light"][line_type]["up_right"] in result[rows - y0][x + offset]:
							horizontal = plot_lines["heavy"]["cross"]["horizontal"]["light_up"]
						elif plot_lines["light"][line_type]["left_up"] in result[rows - y0][x + offset]:
							horizontal = plot_lines["heavy"]["cross"]["horizontal"]["light_up"]
						elif plot_lines["light"][line_type]["vertical"] in result[rows - y0][x + offset]:
							horizontal = plot_lines["heavy"]["cross"]["full"]["light_vertical"]
						elif plot_lines["light"][line_type]["down_right"] in result[rows - y0][x + offset]:
							horizontal = plot_lines["heavy"]["cross"]["horizontal"]["light_down"]
						elif plot_lines["light"][line_type]["left_down"] in result[rows - y0][x + offset]:
							horizontal = plot_lines["heavy"]["cross"]["horizontal"]["light_down"]
					paint0 = f'\x1b[{background_color};{line_color}m'+ horizontal +'\x1b[0m' 
					try:#background from signal
						if signals[x]>=max_flag:
							paint0 = '\x1b[30;'+color2+';5m'+ horizontal +'\x1b[0m'
						elif signals[x]<=min_flag:
							paint0 = '\x1b[30;'+color1+';5m'+ horizontal +'\x1b[0m'
					except:
						pass
					result[rows - y0][x + offset] = paint0
				else:
					if y0 > y1:
						going_lower1 = plot_lines[font_weight][line_type]["up_right"]
						if i == 1:
							if plot_lines["light"][line_type]["horizontal"] in result[rows - y1][x + offset]:
								going_lower1 = plot_lines["heavy"]["cross"]["horizontal"]["up_right"]
							elif plot_lines["light"][line_type]["left_up"] in result[rows - y1][x + offset]:
								going_lower1 = plot_lines["heavy"]["cross"]["horizontal"]["up_right"]
							elif plot_lines["light"][line_type]["vertical"] in result[rows - y1][x + offset]:
								going_lower1 = plot_lines["heavy"]["cross"]["vertical"]["up_right"]
							elif plot_lines["light"][line_type]["down_right"] in result[rows - y1][x + offset]:
								going_lower1 = plot_lines["heavy"]["cross"]["vertical"]["up_right"]
							elif plot_lines["light"][line_type]["left_down"] in result[rows - y1][x + offset]:
								going_lower1 = plot_lines["heavy"]["cross"]["full"]["light_left_down"]
						paint1 = f'\x1b[{background_color};{line_color}m' + going_lower1 + '\x1b[0m'
						try:
							if signals[x]>=max_flag:
								paint1 = '\x1b[30;'+color2 + ';5m'+ going_lower1 + '\x1b[0m'
							elif signals[x]<=min_flag:
								paint1 = '\x1b[30;'+color1 + ';5m'+ going_lower1 + '\x1b[0m'
						except:
							pass
						result[rows - y1][x + offset] = paint1
						
						going_lower2 = plot_lines[font_weight][line_type]["left_down"]
						if i == 1:
							if plot_lines["light"][line_type]["horizontal"] in result[rows - y0][x + offset]:
								going_lower2 = plot_lines["heavy"]["cross"]["horizontal"]["left_down"]
							elif plot_lines["light"][line_type]["left_up"] in result[rows - y0][x + offset]:
								going_lower2 = plot_lines["heavy"]["cross"]["vertical"]["left_down"]
							elif plot_lines["light"][line_type]["vertical"] in result[rows - y0][x + offset]:
								going_lower2 = plot_lines["heavy"]["cross"]["vertical"]["left_down"]
							elif plot_lines["light"][line_type]["down_right"] in result[rows - y0][x + offset]:
								going_lower2 = plot_lines["heavy"]["cross"]["horizontal"]["left_down"]
							elif plot_lines["light"][line_type]["up_right"] in result[rows - y0][x + offset]:
								going_lower2 = plot_lines["heavy"]["cross"]["full"]["light_up_right"]
						paint2 = f'\x1b[{background_color};{line_color}m'+going_lower2+'\x1b[0m'
						try:
							if signals[x]>=max_flag:
								paint2 = '\x1b[30;'+color2+';5m'+going_lower2+'\x1b[0m'
							elif signals[x]<=min_flag:
								paint2 = '\x1b[30;'+color1+';5m'+going_lower2+'\x1b[0m'
						except:
							pass
						result[rows - y0][x + offset] = paint2
					
					elif y0 < y1:
						going_up1 = plot_lines[font_weight][line_type]["down_right"]
						if i == 1:
							if plot_lines["light"][line_type]["horizontal"] in result[rows - y1][x + offset]:
								going_up1 = plot_lines["heavy"]["cross"]["horizontal"]["down_right"]
							elif plot_lines["light"][line_type]["left_up"] in result[rows - y1][x + offset]:
								going_up1 = plot_lines["heavy"]["cross"]["full"]["light_left_up"]
							elif plot_lines["light"][line_type]["vertical"] in result[rows - y1][x + offset]:
								going_up1 = plot_lines["heavy"]["cross"]["vertical"]["down_right"]
							elif plot_lines["light"][line_type]["up_right"] in result[rows - y1][x + offset]:
								going_up1 = plot_lines["heavy"]["cross"]["vertical"]["down_right"]
							elif plot_lines["light"][line_type]["left_down"] in result[rows - y1][x + offset]:
								going_up1 = plot_lines["heavy"]["cross"]["horizontal"]["down_right"]
						paint1 = f'\x1b[{background_color};{line_color}m'+going_up1+'\x1b[0m'
						try:
							if signals[x]>=max_flag:
								paint1 = '\x1b[30;'+color2+';5m'+going_up1+'\x1b[0m'
							elif signals[x]<=min_flag:
								paint1 = '\x1b[30;'+color1+';5m'+going_up1+'\x1b[0m'
						except:
							pass
						result[rows - y1][x + offset] = paint1
						
						going_up2 = plot_lines[font_weight][line_type]["left_up"]
						if i == 1:
							if plot_lines["light"][line_type]["horizontal"] in result[rows - y0][x + offset]:
								going_up2 = plot_lines["heavy"]["cross"]["horizontal"]["left_up"]
							elif plot_lines["light"][line_type]["down_right"] in result[rows - y0][x + offset]:
								going_up2 = plot_lines["heavy"]["cross"]["full"]["light_down_right"]
							elif plot_lines["light"][line_type]["vertical"] in result[rows - y0][x + offset]:
								going_up2 = plot_lines["heavy"]["cross"]["vertical"]["left_up"]
							elif plot_lines["light"][line_type]["up_right"] in result[rows - y0][x + offset]:
								going_up2 = plot_lines["heavy"]["cross"]["horizontal"]["left_up"]
							elif plot_lines["light"][line_type]["left_down"] in result[rows - y0][x + offset]:
								going_up2 = plot_lines["heavy"]["cross"]["vertical"]["left_up"]
						paint2 = f'\x1b[{background_color};{line_color}m'+going_up2+'\x1b[0m'
						try:
							if signals[x]>=max_flag:
								paint2 = '\x1b[30;'+color2+';5m'+going_up2+'\x1b[0m'
							elif signals[x]<=min_flag:
								paint2 = '\x1b[30;'+color1+';5m'+going_up2+'\x1b[0m'
						except:
							pass
						result[rows - y0][x + offset] = paint2

					start = min(y0, y1) + 1
					end = max(y0, y1)
					for y in range(start, end):
						vertical = plot_lines[font_weight][line_type]["vertical"]
						if i == 1:
							if plot_lines["light"][line_type]["up_right"] in result[rows - y][x + offset]:
								vertical = plot_lines["heavy"]["cross"]["vertical"]["light_right"]
							elif plot_lines["light"][line_type]["left_up"] in result[rows - y][x + offset]:
								vertical = plot_lines["heavy"]["cross"]["vertical"]["light_left"]
							elif plot_lines["light"][line_type]["horizontal"] in result[rows - y][x + offset]:
								vertical = plot_lines["heavy"]["cross"]["full"]["light_horizontal"]
							elif plot_lines["light"][line_type]["down_right"] in result[rows - y][x + offset]:
								vertical = plot_lines["heavy"]["cross"]["vertical"]["light_right"]
							elif plot_lines["light"][line_type]["left_down"] in result[rows - y][x + offset]:
								vertical = plot_lines["heavy"]["cross"]["vertical"]["light_left"]
						paint3 = f'\x1b[{background_color};{line_color}m'+vertical+'\x1b[0m'
						try:
							if signals[x]>=max_flag:
								paint3 = '\x1b[30;'+color2+';5m'+vertical+'\x1b[0m'
							elif signals[x]<=min_flag:
								paint3 = '\x1b[30;'+color1+';5m'+vertical+'\x1b[0m'
						except:
							pass
						result[rows - y][x + offset] = paint3
		if signal_as_line:
			for i in range(len(result[0])):
				ll = [row[i] for row in result]
				for jj,j in enumerate(ll):
					if '\x1b[30;'+color2 in j:
						for k in range(len(result)):
							if k!=jj:
								result[k][i]=result[k][i].replace(f'\x1b[{background_color};{line_color}m',f'\x1b[{background_color};{line_color};{color2}m')
					elif '\x1b[30;'+color1 in j:
						for k in range(len(result)):
							if k!=jj:
								result[k][i]=result[k][i].replace(f'\x1b[{background_color};{line_color}m',f'\x1b[{background_color};{line_color};{color1}m')
		ret = '\n'.join([''.join(row) for row in result])
		return(ret)

	def study_bar(
		study: Study,
		color1: str, 
		color2: str, 
		sizeX: int = 50,
		dark_theme: bool = True) -> str:
		"""
Generate an ascii bar chart for Sphoin Slot Study

Parameters
----------
study : Study
    Sphoin Slot Study
    Example:
    	study = slot.studies[0]
color1 : str
	Ansi color code for min_flag signals 
	Default = '45'
	[40,41,42,43,44,45,46,47,49]
color2 : str
	Ansi color code for max_flag signals
	Default = '46'
	[40,41,42,43,44,45,46,47,49]
sizeX : int
	Width of chart plot
	Default = 50
	Contraints
		min = 50
		max = 500
dark_theme : bool
	Theme of chart plot
	Default = True

Returns
------
str
	Ansi chart
		"""

		line_color = "37" if dark_theme else "30"
		background_color = "40" if dark_theme else "47"
		inter = [f'\x1b[30;4{int(study.code.split("#")[1])};5m' + (study.study.center(11," ") + '|'+'\x1b[0m').rjust(12)]
		series = study.result[-sizeX+11:]
		for i in range(0,len(series)-1):
			if series[i] == None or int(series[i])==0:
				inter.append(f'\x1b[{background_color};{line_color};2m'+'\u0020'+'\x1b[0m')
			elif int(series[i]) == 1:
				inter.append('\x1b[30;'+color2+';5m'+'\u0020'+'\x1b[0m')
			elif int(series[i]) == -1:
				inter.append('\x1b[30;'+color1+';5m'+'\u0020'+'\x1b[0m')
		return(''.join(inter))

	def time_bar(
		slot: Slot, 
		sizeX: int = 50,
		dark_theme: bool = True) -> str:
		"""
Generate an ascii time bar for a Sphoin Slot

Parameters
----------
slot : Slot
    Sphoin Slot 
    slot = Slot(config='example')
sizeX : int
	Width of chart plot
	Default = 50
	Contraints
		min = 50
		max = 500
dark_theme : bool
	Theme of chart plot
	Default = True

Returns
------
str
	Ansi chart
		"""
		from_zone = tz.tzutc()
		to_zone = tz.tzlocal()
		line_color = "37" if dark_theme else "30"
		background_color = "40" if dark_theme else "47"
		series = slot.ohlcv.date[-sizeX+12:]
		result = []
		visible_length = divmod(len(series),6)
		visible_index = len(series)-1
		while visible_index >= 0:
			current_length = len(result)
			if current_length < visible_length[0]:        
				try:
					current_date = datetime.datetime.strptime(series[visible_index-2], "%Y-%m-%dT%H:%M:%S")
				except Exception as e:
					current_date = datetime.datetime.strptime(series[visible_index-2].split(".")[0], "%Y-%m-%d %H:%M:%S")
				current_date = current_date.replace(tzinfo=from_zone)
				current_date = current_date.astimezone(to_zone)
				if slot.interval[-1] in ["m","h"]:
					current_date = current_date.strftime("%H:%M")
				else:
					current_date = current_date.strftime("%d/%m")
				result.insert(0,f'\x1b[{background_color};{line_color}m'+current_date.rjust(6,' ')+'\x1b[0m')
				visible_index = visible_index-6
			else:
				result.insert(0,f'\x1b[{background_color};{line_color}m'+u'\u0020'+'\x1b[0m')
				visible_index -= 1
		
		result.insert(0,'time'.rjust(12,'·'))
		result.insert(0,'\x1b[30;43;22m')
		result.insert(2,f'\x1b[{background_color};{line_color};22m')
		result.insert(3,'\x1b[0m')
		return(''.join(result))


if __name__ == '__main__':

	slot = Slot(config='example')

	close = Plot.line(
		series=slot.ohlcv.close,
		signals=slot.signals_sum,
		min_flag=slot.min_flag,
		max_flag=slot.max_flag, 
		color1=slot.colors['1'], 
		color2=slot.colors['-1'],
		sizeX=100,
		sizeY=10,
		signal_as_line=True,
		dark_theme=False)
	print(close)

	time = Plot.time_bar(slot=slot,sizeX=100,dark_theme=False)
	print(time)

	signals = Plot.line(
		series=slot.signals_sum,
		signals=slot.signals_sum,
		min_flag=slot.min_flag,
		max_flag=slot.max_flag, 
		color1=slot.colors['1'], 
		color2=slot.colors['-1'],
		sizeX=100,
		sizeY=7,
		signal_as_line=True)
	print(signals)

	for study in slot.studies:
		series = study.config.indicator_1.raw
		if study.config.indicator_2 != None:
			series = [series]
			series.append(study.config.indicator_2.raw)
		s = Plot.line(
			series=series,
			signals=study.result,
			min_flag=0,
			max_flag=0,
			color1=slot.colors['1'], 
			color2=slot.colors['-1'],
			sizeX=100,
			sizeY=4,
			signal_as_line=True)
		print(s)
		s_bar = Plot.study_bar(
			study=study,
			color1=slot.colors['1'],
			color2=slot.colors['-1'],
			sizeX=100,
			dark_theme=False
			)
		print(s_bar)



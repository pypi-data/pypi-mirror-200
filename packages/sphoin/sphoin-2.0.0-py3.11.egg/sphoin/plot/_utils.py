from rich.text import Text
from rich.style import Style


uni_chars = {
	"space": u'\u0020',
	"vertical_bar":u'\u2524',
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
				"light_right": u'\u2520',
				"light_left": u'\u2528',
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

def intersperse(_list: list, item):
	result = [item] * (len(_list) * 2 -1)
	result[0::2] = _list
	return result

def text_with_style(
	string: str,
	fg: str,
	bg: str) -> tuple:
	return [string,f"{fg} on {bg}"]

def isNumber(n) -> bool:
	return not n == None
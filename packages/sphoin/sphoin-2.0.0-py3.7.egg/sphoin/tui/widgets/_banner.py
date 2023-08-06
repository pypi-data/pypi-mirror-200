from textual.reactive import reactive
from textual.widgets import Static
from rich.text import Text
from rich.style import Style
from rich.color import Color
from ...app import Slot
from ...plot import Plot
import datetime

display = {
	"left":{
		"s":"\x1b[30;47;5m{market}{interval}\x1b[30;46;5m|{max_flag}\x1b[30;45;5m|{min_flag}\x1b[0m",
		"m":"\x1b[30;47;5m{market} | {interval} \x1b[30;46;5m| {max_flag} \x1b[30;45;5m| {min_flag} \x1b[0m",
		"l":"\x1b[30;43;5m{exchange}\x1b[30;47;5m|{market}|{interval}\x1b[30;46;5m|{max_flag}\x1b[30;45;5m|{min_flag}\x1b[0m",
		"xl":"\x1b[30;43;5m{exchange} \x1b[30;47;5m| {market} | {interval} \x1b[30;43;5m| Flags \x1b[30;46;5m| {max_flag} \x1b[30;45;5m| {min_flag} \x1b[0m"
		},
	"mid":{
		"s":"\x1b[30;43;5m|h|q|r|t|s\x1b[0m",
		"m":"\x1b[30;43;5m| h | q | r | t | s \x1b[0m",
		"l":"\x1b[30;43;5m|h Help|q Quit|r Refresh|t Theme|s Signal\x1b[0m",
		"xl":"\x1b[30;43;5m| h Help | q Quit | r Refresh | t Theme | s Signal \x1b[0m"
		},
	"right":{
		"s":"\x1b[30;47;5m|{eta}\x1b[0m",
		"m":"\x1b[30;47;5m| {eta} \x1b[0m",
		"l":"\x1b[30;47;5m|ETA {eta}\x1b[0m",
		"xl":"\x1b[30;47;5m| ETA {eta} \x1b[0m"
		},
	"pad":"\x1b[43;5m \x1b[0m"
}

actions = {
	"help":[" h Help ","h Help"," h ","h"],
	"quit":[" q Quit ","q Quit"," q ","q"],
	"refresh":[" r Refresh ","r Refresh"," r ","r"],
	"theme":[" t Theme ","t Theme"," t ","t"],
	"signal":[" s Signal ","s Signal"," s ","s"]
}


class Banner(Static):

	slot : [Slot, None] = reactive(None)
	banner : list = reactive([Text("Painting.."),Text()])
	multiline : bool = reactive(False)

	def __init__(self, slot: Slot) -> None:
		self._slot = slot
		super().__init__()

	def paint_banner(self, slot: Slot) -> list:
		if self.size.width <50:
			return [Text()]
		if slot!=None:
			eta = datetime.timedelta(seconds=int(slot.ETA))
			sizes = {
				"left":{
					"s":Text.from_ansi(display["left"]["s"].format(exchange=slot.exchange, market=slot.market, interval=slot.interval, max_flag=slot.max_flag, min_flag=slot.min_flag)),
					"m":Text.from_ansi(display["left"]["m"].format(exchange=slot.exchange, market=slot.market, interval=slot.interval, max_flag=slot.max_flag, min_flag=slot.min_flag)),
					"l":Text.from_ansi(display["left"]["l"].format(exchange=slot.exchange, market=slot.market, interval=slot.interval, max_flag=slot.max_flag, min_flag=slot.min_flag)),
					"xl":Text.from_ansi(display["left"]["xl"].format(exchange=slot.exchange, market=slot.market, interval=slot.interval, max_flag=slot.max_flag, min_flag=slot.min_flag))
				},
				"mid":{
					"s":Text.from_ansi(display["mid"]["s"]),
					"m":Text.from_ansi(display["mid"]["m"]),
					"l":Text.from_ansi(display["mid"]["l"]),
					"xl":Text.from_ansi(display["mid"]["xl"]),
				},
				"right":{
					"s":Text.from_ansi(display["right"]["s"].format(eta=eta)),
					"m":Text.from_ansi(display["right"]["m"].format(eta=eta)),
					"l":Text.from_ansi(display["right"]["l"].format(eta=eta)),
					"xl":Text.from_ansi(display["right"]["xl"].format(eta=eta))
				}
			}
			size = ["xl","l","m","s"]
			for r in size:
				tright = sizes["right"][r]
				right = len(tright)
				for l in size:
					tleft = sizes["left"][l]
					left = len(tleft)					
					for m in size:
						tmid = sizes["mid"][m]
						for action in actions.keys():
							for key in actions[action]:
								if key in tmid:
									tmid.stylize(Style.on(click=action),start=str(tmid).index(key),end=str(tmid).index(key)+len(key))
									break
						mid = len(tmid)
						spare = self.size.width - right - left - mid
						if spare >= 0:
							return [tleft,Text.from_ansi(display["pad"]*spare),tmid,tright]
		else:
			return [Text()]

	def on_mount(self) -> None:
		self.slot = self._slot
		# self.styles.link_color = "black"
		self.styles.link_background = "yellow"
		self.styles.link_style = "bold"
		self.styles.link_hover_style = "italic"

		self.set_interval(1, self.refresh_banner)

	def refresh_banner(self) -> None:
		self.banner = self.paint_banner(slot=self.slot)

	def watch_banner(self, banner: list) -> None:
		string = Text()
		for text in banner:
			string += text
		self.update(string)

	def watch_slot(self, slot: Slot) -> None:
		self.banner = self.paint_banner(slot=slot)
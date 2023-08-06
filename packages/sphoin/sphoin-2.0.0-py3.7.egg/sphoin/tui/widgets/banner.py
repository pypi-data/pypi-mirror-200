__author__ = "pom11"
__copyright__ = "Copyright 2023, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

from textual.reactive import reactive
from textual.widgets import Static
from rich.text import Text
from sphoin.app import Slot
from sphoin.plot import Plot
import datetime

class Banner(Static):

	slot : [Slot, None] = reactive(None)
	banner : list = reactive([Text("Painting.."),Text()])
	multiline : bool = reactive(False)

	def __init__(self, slot: Slot) -> None:
		self._slot = slot
		self.rotate = 0
		super().__init__()

	def paint_banner(self, slot: Slot) -> list:
		if self.size.width <50:
			return [Text()]
		if slot!=None:
			eta = datetime.timedelta(seconds=int(slot.ETA))
			disp0 = f"\x1b[30;43;5m{slot.exchange} \x1b[30;47;5m| {slot.market} | {slot.interval} \x1b[30;43;5m" \
			+ f"| Flags \x1b[30;46;5m| {slot.max_flag} \x1b[30;45;5m| {slot.min_flag} \x1b[0m"
			disp1 = f"\x1b[30;43;5mh help | q Quit | r Refresh | t Theme | s Signal | ETA \x1b[30;47;5m| {eta} \x1b[0m"
			result = [Text.from_ansi(disp0),Text.from_ansi(disp1)]
			pad = self.size.width-len(result[0])-len(result[1])
			if pad<=0:
				disp1 = f"\x1b[30;43;5mh|q|r|t|s \x1b[30;47;5m| {eta} \x1b[0m"
				result = [Text.from_ansi(disp0),Text.from_ansi(disp1)]
				pad = self.size.width-len(result[0])-len(result[1])
				if pad<=0:
					disp0 = disp0.replace("| Flags ",'')
					result = [Text.from_ansi(disp0),Text.from_ansi(disp1)]
					pad = self.size.width-len(result[0])-len(result[1])
					if pad <=0:
						disp0 = disp0.replace(" ","")
						disp1 = disp1.replace(f"h|q|r|t|s",'')
						result = [Text.from_ansi(disp0),Text.from_ansi(disp1)]
						pad = self.size.width-len(result[0])-len(result[1])
			result.insert(1,Text.from_ansi("\x1b[43;5m \x1b[0m"*pad))
			return result
		else:
			return [Text()]

	def on_mount(self) -> None:
		self.slot = self._slot
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
	
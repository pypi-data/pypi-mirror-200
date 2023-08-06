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

class Time(Static):

	slot : [Slot, None] = reactive(None)
	banner : [str, None] = reactive(None)
	dark: bool = reactive(True)

	def __init__(self, slot: Slot) -> None:
		self._slot = slot
		super().__init__()

	def paint_time(self, slot: Slot, dark: bool) -> str:
		if self.size.width<50:
			return ''
		return Plot.time_bar(slot=slot,sizeX=self.size.width,dark_theme=dark)

	def on_mount(self) -> None:
		self.slot = self._slot
		self.set_interval(1, self.refresh_banner)

	def refresh_banner(self) -> None:
		self.banner = self.paint_time(slot=self.slot, dark=self.dark)

	def watch_banner(self, banner: str) -> None:
		self.update(Text.from_ansi(f"{banner}"))

	def watch_slot(self, slot: Slot) -> None:
		if slot!=None:
			self.banner = self.paint_time(slot=slot,dark=self.dark)

	def watch_dark(self, dark: bool) -> None:
		self.banner = self.paint_time(slot=self.slot,dark=dark)
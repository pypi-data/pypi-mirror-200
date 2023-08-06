from textual.reactive import reactive
from textual.widgets import Static
from rich.text import Text
from sphoin.app import Slot
from sphoin.plot import Plot

class Time(Static):

	slot : [Slot, None] = reactive(None)
	banner : [str, None] = reactive(None)

	def __init__(self, slot: Slot) -> None:
		self._slot = slot
		super().__init__()

	def on_mount(self) -> None:
		self.slot = self._slot
		self.set_interval(1, self.refresh_banner)

	def refresh_banner(self) -> None:
		self.banner = Plot.time_bar(slot=self.slot,sizeX=self.size.width,dark_theme=True)

	def watch_banner(self, banner: str) -> None:
		self.update(Text.from_ansi(f"{banner}"))

	def watch_slot(self, slot: Slot) -> None:
		if slot!=None:
			self.banner = Plot.time_bar(slot=slot,sizeX=self.size.width,dark_theme=True)
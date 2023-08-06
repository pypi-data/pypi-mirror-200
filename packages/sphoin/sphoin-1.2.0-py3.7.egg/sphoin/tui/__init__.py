__author__ = "pom11"
__copyright__ = "Copyright 2023, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "1.2.0"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"


from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static
from math import floor
from sphoin.app import Slot
from sphoin.plot import Plot
from widgets.graph import Graph
from widgets.banner import Banner
from widgets.time import Time

class TUI(App[None]):

	CSS_PATH = "__init__.css"

	BINDINGS = [
		("r","refresh","Refresh"),
		("q","quit","Quit"),
		("t", "toggle_dark", "Theme"),
		("s", "signal_as_line","Signal")
	]

	def __init__(self, **kwargs) -> None:
		if 'slot' in kwargs.keys():
			self.slot = kwargs['slot']
		else:
			self.slot = Slot(config='example')
		super().__init__()			

	def compose(self) -> ComposeResult:
		plots = []
		for layout in self.slot.layout:
			if layout in ['line','signals','studies']:
				widget = Graph(slot_init=self.slot, plot_type=layout)
			elif layout == 'time':
				widget = Time(slot=self.slot)
			elif layout == 'banner':
				widget = Banner(slot=self.slot)
			plots.append(
				Container(
					widget,
					id=layout
				)
			)
		yield Vertical(
			*tuple(plots),
			id="contents"
			)

	def on_mount(self) -> None:
		self.set_interval(1,self.refresh_graphs)
		self.compute_height()

	def on_resize(self) -> None:
		self.compute_height()

	def refresh_graphs(self) -> None:
		self.slot.ETA = self.slot.ETA-1
		if self.slot.ETA == 0:
			self.slot.refresh()
		
	def action_refresh(self) -> None:
		self.slot.refresh()

	def action_toggle_dark(self) -> None:
		self.dark = not self.dark
		for widget in [Graph,Time]:
			graphs = self.query(widget)
			if len(graphs)>0:
				for graph in graphs:
					graph.dark = self.dark

	def action_signal_as_line(self) -> None:
		graphs = self.query(Graph)
		for graph in graphs:
			graph.signal_as_line = not graph.signal_as_line
		
	def compute_height(self) -> None:
		_studies = self.slot.nr_studies if "studies" in self.slot.layout else 0
		_signals = self.slot.nr_studies if "signals" in self.slot.layout else 0
		_time = 1 if "time" in self.slot.layout else 0
		_banner = 1 if "banner" in self.slot.layout else 0

		height = {
			"line": self.size.height-_studies-_signals-_time-_banner,
			"studies": self.slot.nr_studies,
			"signals": self.slot.nr_studies,
			"time": _time,
			"banner": _banner
		}

		for layout in self.slot.layout:
			graphs = self.query(f"#{layout}")
			if len(graphs)>0:
				graphs.first().styles.height = height[layout]


if __name__ == "__main__":
	slot = Slot(config="example")
	app = TUI(slot=slot)
	app.run()


"""Console script for sphoin."""

__author__ = "pom11"
__copyright__ = "Copyright 2022, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "1.1.12"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

import argparse
import sys
from sphoin.app import Slot
from sphoin.tui import TUI
from rich.table import Table
from rich import print

app_title = f' [bold cyan]sphoin[/bold cyan][bold magenta].app[/bold magenta] [bold yellow]TUI[/bold yellow]'
table = Table(title=None,box=None)
table.add_column('Argument',justify='left', style='green', no_wrap=False)
table.add_column('',justify='left', style='yellow', no_wrap=False)
table.add_column('Help',justify='left', style='bold cyan', no_wrap=False)
data = [
		['--help','-h', 'Print help'],
		['--example','-e','View example'],
		['--file','-f','Load .yaml config file']
	]
for d in data:
	table.add_row(*d)

def main():
"""Console script for sphoin."""
	print(app_title)
	import argparse
	parser = argparse.ArgumentParser(description="Connect via apiv1 to sphoin.app slots",add_help=False)
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-h","--help",help="Print help",action="store_true")
	group.add_argument("-e","--example",help="View example",action="store_true")
	group.add_argument("-f","--file",help="Load .yaml config file")
	args = parser.parse_args()

	if len(sys.argv)==1:
		print(table)
		sys.exit(1)

	if args.help:
		print(table)
		sys.exit(1)
	elif args.file:
		slot = Slot(config=args.file)
		if slot == "slot_error":
			sys.exit(1)
	elif args.example:
		print("[bold cyan]Loading...[/bold cyan]")
		slot = Slot(config="example")
		app = TUI(slot=slot)
		app.run()
		
	

if __name__ == "__main__":
	sys.exit(main())

display = {
	"left":{
		"s":"{market}{interval}\x1b[30;46;5m|{max_flag}\x1b[30;45;5m|{min_flag}",
		"m":"{market} | {interval} \x1b[30;46;5m| {max_flag} \x1b[30;45;5m| {min_flag} ",
		"l":"\x1b[30;43;5m{exchange}|{market}|{interval}\x1b[30;46;5m|{max_flag}\x1b[30;45;5m|{min_flag}",
		"xl":"\x1b[30;43;5m{exchange} | {market} | {interval} \x1b[30;43;5m| Flags \x1b[30;46;5m| {max_flag} \x1b[30;45;5m| {min_flag} "
		},
	"mid":{
		"s":"\x1b[30;43;5m|h|q|r|t|s",
		"m":"\x1b[30;43;5m| h | q | r | t | s ",
		"l":"\x1b[30;43;5m|h Help|q Quit|r Refresh|t Theme|s Signal",
		"xl":"\x1b[30;43;5m| h Help | q Quit | r Refresh | t Theme | s Signal "
		},
	"right":{
		"s":"|{eta}",
		"m":"| {eta} ",
		"l":"|ETA {eta}",
		"xl":"| ETA {eta} "
		}
}

actions = {
	"help":[" h Help ","h Help"," h ","h"],
	"quit":[" q Quit ","q Quit"," q ","q"],
	"refresh":[" r Refresh ","r Refresh"," r ","r"],
	"theme":[" t Theme ","t Theme"," t ","t"],
	"signal":[" s Signal ","s Signal"," s ","s"]
}
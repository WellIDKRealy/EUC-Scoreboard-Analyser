# EUC Scoreboard Analyser

Analyser that tries to extract data from EU Commadner scoreboard screenshoots

## Deployment
```bash
   guix shell --pure -m manifest.scm  -C -N --no-cwd
```
For now it requires GNU/Guix

## Usage
```bash
   python3 main.py <path_to_file>
```

## Example
```bash
   python3 main.py EXAMPLE_SCREEN.png
```
```json
{
  "team1": {
	"score": 0,
	"name": "i\\XKonisreich PreufBen",
	"alive": 64,
	"players_no": 7,
	"players": [
	  {
		"name": "witehhunt Ip",
		"alive": "25 Alive",
		"kills": "20D",
		"deaths": "10",
		"ping": "oOSo7"
	  },
	  {
		"name": "Polskise#mtoc",
		"alive": "1DAhcde",
		"kills": "14",
		"deaths": "25",
		"ping": "Sa"
	  },
	  {
		"name": "Sandwich",
		"alive": "1 Alive",
		"kills": "10",
		"deaths": "12",
		"ping": "a0"
	  },
	  {
		"name": "C(HUR_MoO]c",
		"alive": "ObAdinek",
		"kills": "10",
		"deaths": "20",
		"ping": "40"
	  },
	  {
		"name": "BlackBruceLe",
		"alive": "28 Alive",
		"kills": "6",
		"deaths": "?",
		"ping": "B87"
	  },
	  {
		"name": "Avron",
		"alive": "ODAd ek",
		"kills": "O",
		"deaths": "O",
		"ping": "23"
	  },
	  {
		"name": "Draven_Mac",
		"alive": "ODAdack",
		"kills": "O",
		"deaths": "O",
		"ping": "100"
	  }
	]
  },
  "team2": {
	"score": 0,
	"name": "| Rheinbund",
	"alive": 7,
	"players_no": 6,
	"players": [
	  {
		"name": "New Plavert",
		"alive": "28 Alive",
		"kills": "34",
		"deaths": "26",
		"ping": "lavert"
	  },
	  {
		"name": "HM_Charles.",
		"alive": "S Alive",
		"kills": "17",
		"deaths": "GS",
		"ping": "yarles"
	  },
	  {
		"name": "Milena_Velb:",
		"alive": "18 Alive",
		"kills": "13",
		"deaths": "12",
		"ping": "_Velb:"
	  },
	  {
		"name": "BloodyCamt",
		"alive": "15 Alive",
		"kills": "10",
		"deaths": "2",
		"ping": "amt"
	  },
	  {
		"name": "Rafal_PL",
		"alive": "ODAd ek",
		"kills": "O",
		"deaths": "O",
		"ping": "Le"
	  },
	  {
		"name": "(TSS]-SharSh",
		"alive": "TD Adarck",
		"kills": "O",
		"deaths": "15",
		"ping": "bharSh"
	  }
	]
  }
}
```

Sadly for now it does have lot of errors especialy on player names
mostly due to tesseract being awfull

## TODO
- Decouple guix
- Make deploying through pip possible
- Replace tesseract with something good

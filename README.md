# EUC Scoreboard Analyser

Analyser that tries to extract data from EU Commadner scoreboard screenshoots

## Deployment
### GNU/GUIX
```bash
   guix shell --pure -m manifest.scm  -C -N --no-cwd
```
#### Windows
Download and install python(3.10)

```bat
   pip install -r requirements.txt
```

## Usage
```bash
   python3 cli.py <path_to_file>
```

For more information use
```bash
   python3 cli.py --help
```

## Example
```bash
   python3 cli.py EXAMPLE_SCREEN.png
```

```json
[
  {
	"path": "<PATH>/EXAMPLE_SCREEN.png",
	"team1": {
	  "score": [
		0,
		0.9578052555011173
	  ],
	  "name": [
		"Preulen",
		0.8403375127338236
	  ],
	  "alive": [
		64,
		0.9995292521618042
	  ],
	  "players_no": [
		7,
		0.8355429938133971
	  ],
	  "players": [
		{
		  "name": [
			"Ja",
			0.9900739880242595
		  ],
		  "alive": [
			25,
			0.6634882982550647
		  ],
		  "kills": [
			20,
			0.9999274238982652
		  ],
		  "deaths": [
			10,
			0.9995619537627194
		  ],
		  "ping": [
			257,
			0.9556120592322573
		  ]
		},
		{
		  "name": [
			"Polskiseimtoc",
			0.914322837271461
		  ],
		  "alive": [
			108,
			0.32999014471943217
		  ],
		  "kills": [
			14,
			0.6307932636203527
		  ],
		  "deaths": [
			25,
			0.8351181543812688
		  ],
		  "ping": [
			54,
			0.6213257198317109
		  ]
		},
		{
		  "name": [
			"Sandwich",
			0.9870416023506801
		  ],
		  "alive": [
			1,
			0.9973649478901656
		  ],
		  "kills": [
			10,
			0.9943145836470499
		  ],
		  "deaths": [
			12,
			0.6582661223399465
		  ],
		  "ping": [
			410,
			0.9208906888961792
		  ]
		},
		{
		  "name": [
			"IHUR Molc",
			0.49684034969444446
		  ],
		  "alive": [
			6,
			0.36127620533168037
		  ],
		  "kills": [
			10,
			0.525073998111937
		  ],
		  "deaths": [
			20,
			0.9996695071926264
		  ],
		  "ping": [
			40,
			0.9389479756355286
		  ]
		},
		{
		  "name": [
			"BlackBrucela",
			0.6704585189412067
		  ],
		  "alive": [
			28,
			0.999999915706304
		  ],
		  "kills": [
			6,
			0.9999531512979196
		  ],
		  "deaths": [
			7,
			0.861212255510292
		  ],
		  "ping": [
			87,
			0.5109152406256455
		  ]
		},
		{
		  "name": [
			"Auron",
			0.9915887760541654
		  ],
		  "alive": [
			1,
			0.3340105793579355
		  ],
		  "kills": [
			0,
			0.8891401169902997
		  ],
		  "deaths": [
			0,
			0.9962490274867299
		  ],
		  "ping": [
			23,
			0.9999647654164576
		  ]
		},
		{
		  "name": [
			"Draven Mac",
			0.9918185732400095
		  ],
		  "alive": [
			6,
			0.2237014862722925
		  ],
		  "kills": [
			0,
			0.9978593589031908
		  ],
		  "deaths": [
			0,
			0.9994433700985752
		  ],
		  "ping": [
			100,
			0.9785931081655308
		  ]
		}
	  ]
	},
	"team2": {
	  "score": [
		0,
		0.9997894874747004
	  ],
	  "name": [
		"Rheinbund",
		0.919090141657784
	  ],
	  "alive": [
		7,
		0.3004763978318046
	  ],
	  "players_no": [
		6,
		0.726334191776671
	  ],
	  "players": [
		{
		  "name": [
			"New",
			0.9999347536965667
		  ],
		  "alive": [
			28,
			0.8554829364835952
		  ],
		  "kills": [
			34,
			0.9999938465656626
		  ],
		  "deaths": [
			26,
			0.9999635010242852
		  ],
		  "ping": [
			41,
			0.4759822139251648
		  ]
		},
		{
		  "name": [
			"HM Charles",
			0.8486385765929211
		  ],
		  "alive": [
			5,
			0.9999963045154381
		  ],
		  "kills": [
			17,
			0.9196221637408135
		  ],
		  "deaths": [
			6,
			0.9998890192307819
		  ],
		  "ping": [
			46,
			0.5861245012018236
		  ]
		},
		{
		  "name": [
			"Milena Velb:",
			0.48466844342757565
		  ],
		  "alive": [
			18,
			0.8367264100917727
		  ],
		  "kills": [
			13,
			0.9992550935929279
		  ],
		  "deaths": [
			12,
			0.9999735318817311
		  ],
		  "ping": [
			263,
			0.31254928622337497
		  ]
		},
		{
		  "name": [
			"BloodvCam1",
			0.6156992164777665
		  ],
		  "alive": [
			15,
			0.9999989884757856
		  ],
		  "kills": [
			10,
			0.9960060601992062
		  ],
		  "deaths": [
			2,
			0.9871686142135325
		  ],
		  "ping": [
			301,
			0.16206199762788578
		  ]
		},
		{
		  "name": [
			"PL",
			0.9951882046354003
		  ],
		  "alive": [
			1,
			0.28692522802232107
		  ],
		  "kills": [
			0,
			0.9991574870639717
		  ],
		  "deaths": [
			0,
			0.9890105332055477
		  ],
		  "ping": [
			1,
			0.6352161113136958
		  ]
		},
		{
		  "name": [
			"TTSS]-Sharsh",
			0.4126252896976977
		  ],
		  "alive": [
			1,
			0.4612487506094567
		  ],
		  "kills": [
			0,
			0.9993274151097218
		  ],
		  "deaths": [
			15,
			0.9253097480501261
		  ],
		  "ping": [
			66,
			0.7042792294971787
		  ]
		}
	  ]
	}
  }
]
```

JSON output format:
```json
[
 {
  "path": "<PATH_TO_FILE>",
  "team1": {
	"score": [
		<VALUE>,
		<VALUE_CONFIDENCE>
	],
	"name": [
		<VALUE>,
		<VALUE_CONFIDENCE>
	],
	"alive": [
		<VALUE>,
		<VALUE_CONFIDENCE>
	],
	"player_no": [
		<VALUE>,
		<VALUE_CONFIDENCE>
	],
	"players": [
		{
		 "name": [
			 "<VALUE>",
			 <VALUE_CONFIDENCE>
		 ],
		 "alive": [
			 <VALUE>,
			 <VALUE_CONFIDENCE>
		 ],
		 "kills": [
			 <VALUE>,
			 <VALUE_CONFIDENCE>
		 ],
		 "deaths": [
			 <VALUE>,
			 <VALUE_CONFIDENCE>
		 ]
		 "ping": [
			 <VALUE>,
			 <VALUE_CONFIDENCE>
		 ]
		},
		...<OTHER PLAYERS>
	]
  }
  "team2": <IDENTICAL_TO_TEAM_ONE>
  }
]
```


## TODO
- Decouple guix
- Make deploying through pip possible

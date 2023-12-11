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
```
Team One:
PlayerName:Pharis. 1 Abad
Kills:65S
Deaths:31
Ping:Bd
PlayerName:Northern 19 Alive
Kills:a2
Deaths:an}
Ping:15
PlayerName:Pal 27 Alive
Kills:40
Deaths:30
Ping:57
PlayerName:BavarianBarbarian 27 Alive
Kills:29
Deaths:30
Ping:33
PlayerName:Geralt_The_Whistleds Alive
Kills:24
Deaths:42
Ping:22
PlayerName:Ivatur 22 Alive
Kills:18
Deaths:26
Ping:22
PlayerName:POLSKAGUROM 26 Alive
Kills:9
Deaths:1
Ping:36
PlayerName:MeNusset 21 Alive
Kills:S
Deaths:1
Ping:20
PlayerName:<Ve_lerFusGre_(lort_ Abiemont
Kills:. G
Deaths:18
Ping:36
PlayerName:New _PlayerPixel 20 Alive
Kills:GS
Deaths:26
Ping:23
PlayerName:JohnWickWThBisliicR7 Alive
Kills:4
Deaths:oO
Ping:72
PlayerName:SabirSlayer OMd ack
Kills:O
Deaths:oO
Ping:261
```

Sadly for now it does have lot of errors especialy on player names
mostly due to tesseract being awfull

## TODO
- Decouple guix
- Make deploying through pip possible
- Replace tesseract with something good
- Refactor code so it is't shit
- Add sensible CLI interface


# EUC Scoreboard Analyser

Analyser that tries to extract data from EU Commadner scoreboard screenshoots

## Deployment
```bash
   guix shell --pure -m manifest.scm  -C -N --no-cwd
```
For now it requires GNU/Guix
### TODO:
Decouple Guix/Make deployment through pip possible

## Usage
```bash
   python3 main.py <path_to_file>
```

### TODO:
Add any sensible CLI interface
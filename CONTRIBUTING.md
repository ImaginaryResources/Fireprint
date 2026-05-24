# Dev setup

Clone and cd into project

```
git clone https://github.com/ImaginaryResources/Fireprint
```

```
cd Fireprint
```

## Windows

Create a virtual python environment

```
py -m venv env-fireprint
```

Activate the virtual python environment

```
.\env-fireprint\Scripts\activate
```

Install required python packages

```
pip install -r requirements.txt
```

### Testing fireprint.py

```
.\env-fireprint\Scripts\python.exe fireprint.py --printer "Fireprint" `
    --image https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/castle_.png `
    --username "Castle_" `
    --subMessage "You da besh" `
    --subMonths 13 `
    --subCurrentStreak 3 `
    --eventMsg "Thanks for the tier 1 sub!"
```

### Creating the fireprint.exe

Run pyinstaller to initalize the exe

```
pyinstaller.exe --onefile .\fireprint.py
```

Add the following to `fireprint.spec`

```
datas=[('env-fireprint\\Lib\\site-packages\\escpos\\capabilities.json', 'escpos')],
```

Run pyinstaller with the spec file

```
pyinstaller.exe .\fireprint.spec 
```

### Test the exe

```
.\dist\fireprint.exe --printer "Fireprint" `
    --image https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/castle_.png `
    --username "Castle_" `
    --subMessage "You da besh" `
    --subMonths 13 `
    --subCurrentStreak 3 `
    --eventMsg "Thanks for the tier 1 sub!"
```

## Linux (Ubuntu)

Install packages

```
sudo apt install libcups2-dev build-essential python3-dev gcc python3.14-venv
``` 

Create a virtual python environment

```
python3 -m venv env-fireprint
```

Activate the virtual python environment

```
source env-fireprint/bin/activate
```

Install required python packages

```
pip install -r requirements.txt
```

### Testing fireprint.py

```
python fireprint.py --server 127.0.0.1 \
    --image https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/castle_.png \
    --username "Castle_" \
    --subMessage "You da besh" \
    --subMonths 13 \
    --subCurrentStreak 3 \
    --eventMsg "Thanks for the\ntier 1 sub!"
```

### Creating the fireprint binary

Run pyinstaller to initalize the binary

```
pyinstaller --onefile ./<fireprint|print-server>.py
```

1. Add the following to `fireprint.spec`

```
datas=[('env-fireprint/lib/python3.14/site-packages/escpos/capabilities.json', 'escpos')],
```

2. Add the following for `print-server.spec`

```
datas=[('env-fireprint/lib/python3.14/site-packages/py_star_tsp/fonts', 'py_star_tsp/fonts')],
```

Run pyinstaller with the spec file

```
pyinstaller ./<fireprint|print-server>.spec 
```

### Testing the fireprint binary

```
./dist/fireprint --server 127.0.0.1 \
    --image https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/castle_.png \
    --username "Castle_" \
    --subMessage "You da besh" \
    --subMonths 13 \
    --subCurrentStreak 3 \
    --eventMsg "Thanks for the\ntier 1 sub!"
```

## Notes

If you're looking to use a TSP100 or TSP143 with escpos you need to do the following as described in [this guide](https://starmicronics.com/help-center/knowledge-base/how-to-change-the-emulation-on-star-tsp100-series-printers/).

Set the printer to use [Win32Raw](https://python-escpos.readthedocs.io/en/latest/user/printers.html#win32raw).
This works since the printer is visible to Windows. Here my printer is named "Fireprint" in Windows.

```
p = Win32Raw("Fireprint")
```

Its a bit odd that this is not mentioned in the docs, instead it states, ["you will not be able to directly print with this library to the printer."](https://python-escpos.readthedocs.io/en/latest/user/usage.html#print-with-star-tsp100-family).

# Dev setup

Clone and cd into project

```
git clone
```

```
cd Fireprint
```

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

## Creating the fireprint.exe

Run pyinstaller to initalize the exe

```
pyinstaller.exe --onefile .\fireprint.py
```

Add the following to `fireprint.spec `

```
...
datas=[('env-fireprint\\Lib\\site-packages\\escpos\\capabilities.json', 'escpos')],
...
```

Run pyinstaller with the spec file

```
pyinstaller.exe .\fireprint.spec 
```

### Test the exe

```
.\fireprint.exe "Fireprint" `
    https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/castle_.png `
    "Castle_" `
    --subMessage "You da besh" `
    --subMonths 13 `
    --subCurrentStreak 3 `
    --eventMsg "Thanks for the tier 1 sub!"
```

## Notes

If you're looking to use a TSP100 or TSP143 with escpos you need to do the following as described in [this guide](https://starmicronics.com/help-center/knowledge-base/how-to-change-the-emulation-on-star-tsp100-series-printers/).

Set the printer to use [Win32Raw](https://python-escpos.readthedocs.io/en/latest/user/printers.html#win32raw).
This works since the printer is visible to Windows. Here my printer is named "Fireprint" in Windows.

```
p = Win32Raw("Fireprint")
```

Its a bit odd that this is not mentioned in the docs, instead it states, ["you will not be able to directly print with this library to the printer."](https://python-escpos.readthedocs.io/en/latest/user/usage.html#print-with-star-tsp100-family).

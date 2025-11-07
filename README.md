# Fireprint 🔥🖨️

A thermal printer companion for [Firebot](https://github.com/crowbartools/Firebot), an open source Twitch bot.  
For the best compatability make sure the printer in use is listed [here](https://python-escpos.readthedocs.io/en/latest/printer_profiles/available-profiles.html).

## Running a command in CLI

It is important to first test `fireprint.exe` to ensure it works as expected.

```
usage: fireprint.py [-h] [--eventMsg EVENTMSG] [--subMonths SUBMONTHS] [--subCurrentStreak SUBCURRENTSTREAK] [--subMsg SUBMSG]
                    [--cheerTotalBits CHEERTOTALBITS]
                    printer url username

A thermal printer companion for Firebot

positional arguments:
  printer               name of the printer
  url                   URL of the user image
  username              username for the receipt

options:
  -h, --help            show this help message and exit
  --eventMsg EVENTMSG   message to display
  --subMonths SUBMONTHS
                        number of months subbed
  --subCurrentStreak SUBCURRENTSTREAK
                        current sub streak in months
  --subMsg SUBMSG       sub message
  --cheerTotalBits CHEERTOTALBITS
                        number of bits cheered
```

> [!NOTE]  
> New lines via CLI will not appear, they do appear when sent from Firebot.

### Example command

```
.\fireprint.exe "Fireprint" `
    https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/castle_.png `
    "Castle_" `
    --subMessage "You da besh" `
    --subMonths 13 `
    --subCurrentStreak 3 `
    --eventMsg "Thanks for the tier 1 sub!"
```

The output should look like the following, and may not reflect the result when printed from Firebot.  
This is because newlines are sent from Firebot, but is not possible through CLI.

<img src="https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/CLI_test.png" alt="Alt Text" width="300">

Once its confirmed to be working continue to the steps below.

## In Firebot

Download the setupfile and import it to Firebot.

### Import Questions

#### Enter full path to fireprint.exe. Example: C:\Fireprint\dist\fireprint.exe

Default: `blank`

#### Enter the name of the printer

Default: `blank`

### Result

After importing test the "Fireprint Sub" event. It should look like the following.

<img src="https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/Firebot_test.png" alt="Alt Text" width="300">

### Default messages for events

Follow

```
$%fireprinterName $userAvatarUrl[$username] $username --eventMsg "Thank you for\n the follow!"
```

Sub

```
$%fireprinterName $userAvatarUrl[$username] $username --eventMsg "Thank you for\n the $subType sub!" --subMonths $subMonths --subCurrentStreak $subCurrentStreak --subMessage "$subMessage"
```

Sub Gifted

```
$%fireprinterName $userAvatarUrl[$giftGiverUsername] $giftGiverUsername --eventMsg "Thank you for\n the gift to\n $giftReceiverUsername!"
```

Community Subs Gifted

```
$%fireprinterName $userAvatarUrl[$giftGiverUsername] $giftGiverUsername --eventMsg "Thank you for\n the gifts to\n the community!"
```

Gift Sub Upgraded

```
$%fireprinterName $userAvatarUrl[$username] $username --eventMsg "Thank you for\n the upgraded\n gifted sub!"
```

Prime Sub Upgraded

```
$%fireprinterName $userAvatarUrl[$username] $username --eventMsg "Thank you for\n the upgraded\n prime sub!"
```

Cheer/Bits

```
$%fireprinterName $userAvatarUrl[$username] $username --eventMsg "Thank you for\n the $cheerBitsAmount bits!" --cheerTotalBits $cheerTotalBits --cheerMessage "$cheerMessage"
```

Follower Goal

```
$%fireprinterName $userAvatarUrl[$streamer] $streamer --eventMsg "Follower goal of\n $channelGoalTargetAmount[follow]\n is completed!"
```

Sub Goal

```
$%fireprinterName $userAvatarUrl[$streamer] $streamer --eventMsg "Sub goal of\n $channelGoalTargetAmount[sub]\n is completed!"
```

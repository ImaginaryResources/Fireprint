# Fireprint 🔥🖨️

A thermal printer companion for [Firebot](https://github.com/crowbartools/Firebot), an open source Twitch bot, 
to print Twitch events on receipt paper.
For the best compatability make sure the printer in use is listed [here](https://python-escpos.readthedocs.io/en/latest/printer_profiles/available-profiles.html).

Supported events out of the box:

- Follow
- Sub
- Sub Gifted
- Community Subs Gifted
- Gift Sub Upgraded
- Prime Sub Upgraded
- Cheer/Bits: Default is set to 25+ bits
  - Gigantify Emote
  - Message Effect
  - On-Screen Celebration
- Follower Goal
- Sub Goal
- Raids: Default is set to 10+ viewers

> [!TIP]  
> Before trying this project make sure you can print a test page to your thermal printer and the appropriate drivers are installed.

To start download the `Fireprint.firebotsetup` and executable from the [releases page](https://github.com/ImaginaryResources/Fireprint/releases).

## Running a command in CLI

It is important to first test `fireprint.exe` or `fireprint` binary to ensure it works as expected.

```
usage: fireprint.exe [-h] -p PRINTER -i [IMAGESOURCE] -u USERNAME [-e EVENTMSG] [-M SUBMONTHS] [-S SUBCURRENTSTREAK] [-m SUBMESSAGE] [-c CHEERMESSAGE] [-t CHEERTOTALBITS]

A thermal printer companion for Firebot

options:
  -h, --help            show this help message and exit
  -p, --printer PRINTER
                        name of the printer
  -i, --imageSource [IMAGESOURCE]
                        full path to png image or URL of the user image (optional)
  -u, --username USERNAME
                        username for the receipt
  -e, --eventMsg EVENTMSG
                        message to display
  -M, --subMonths SUBMONTHS
                        number of months subbed
  -S, --subCurrentStreak SUBCURRENTSTREAK
                        current sub streak in months
  -m, --subMessage SUBMESSAGE
                        sub message
  -c, --cheerMessage CHEERMESSAGE
                        message from cheer
  -t, --cheerTotalBits CHEERTOTALBITS
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

<img src="https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/CLI_test.png" alt="Alt Text" width="300">

Once its confirmed to be working continue to the steps below.

## Firebot

[Download](https://github.com/ImaginaryResources/Fireprint/releases) the setupfile and import it to Firebot, (Settings -> Setups -> Import Setup).

### Import Questions

#### Enter full path to fireprint.exe. Example: C:\Fireprint\dist\fireprint.exe

Default: `blank`

#### Enter the name of the printer

Default: `blank`

### Result

After importing, test the "Fireprint Sub" event. It should look like the following.

<img src="https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/Firebot_test.png" alt="Alt Text" width="300">

### Default messages for events

Follow

```
-p $%fireprinterName -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the follow!"
```

Sub

```
-p $%fireprinterName -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the $subType sub!" --subMonths $subMonths --subCurrentStreak $subCurrentStreak --subMessage "$subMessage"
```

Sub Gifted

```
-p $%fireprinterName -i $userAvatarUrl[$giftGiverUsername] -u $giftGiverUsername --eventMsg "Thank you for\n the gift to\n $giftReceiverUsername!"
```

Community Subs Gifted

```
-p $%fireprinterName -i $userAvatarUrl[$giftGiverUsername] -u $giftGiverUsername --eventMsg "Thank you for\n $giftCount gifts to\n the community!"
```

Gift Sub Upgraded

```
-p $%fireprinterName -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the upgraded\n gifted sub!"
```

Prime Sub Upgraded

```
-p $%fireprinterName -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the upgraded\n prime sub!"
```

Cheer/Bits

```
-p $%fireprinterName -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the $cheerBitsAmount bits!" --cheerTotalBits $cheerTotalBits --cheerMessage "$cheerMessage"
```

Gigantify Emote (Cheer/Bits)

```
-p $%fireprinterName -i $gigantifiedEmoteUrl -u $userDisplayName --eventMsg "Giant emote\n for $cheerBitsAmount bits!" --cheerTotalBits $cheerTotalBits --cheerMessage "$cheerMessage"
```

Message Effect (Cheer/Bits)

```
-p $%fireprinterName -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Msg effect\n for $cheerBitsAmount bits!" --cheerTotalBits $cheerTotalBits --cheerMessage "$cheerMessage"
```

On-Screen Celebration (Cheer/Bits)

```
-p $%fireprinterName -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Emote party\n for $cheerBitsAmount bits!" --cheerTotalBits $cheerTotalBits
```

Tips/Donations

```
-p $%fireprinterName -i $userAvatarUrl[$donationFrom] -u $donationFrom --eventMsg "Thank you for\n the $donationAmountFormatted dono!" --cheerMessage "$donationMessage"
```

Follower Goal

```
-p $%fireprinterName -i $userAvatarUrl[$userDisplayName[$streamer]] -u $userDisplayName[$streamer] --eventMsg "Follower goal of\n $channelGoalTargetAmount[follow]\n is completed!"
```

Sub Goal

```
-p $%fireprinterName -i $userAvatarUrl[$userDisplayName[$streamer]] -u $userDisplayName[$streamer] --eventMsg "Sub goal of\n $channelGoalTargetAmount[sub]\n is completed!"
```

Incoming Raid

```
-p $%fireprinterName -i -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the $raidViewerCount\n viewer raid!"
```

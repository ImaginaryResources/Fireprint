# Fireprint 🔥🖨️

> [!IMPORTANT]
> This branch only works with TSP printer which uses the [`py-star-tsp` Python SDK](https://github.com/printer-stream/py-star-tsp).
> Uses a client-server architecture — `fireprint.py` sends ESC/POS data to a `print_server.py` which renders it on a Star TSP100 thermal printer over USB.
> Follow the required steps before [proceeding](https://github.com/printer-stream/py-star-tsp#linux-usb-access-udev-rule).

A thermal printer companion for [Firebot](https://github.com/crowbartools/Firebot), an open source Twitch bot, 
to print Twitch events on receipt paper.

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

First start the print server in one terminal:

```
python print_server.py
```

Then in another terminal, send receipts with `fireprint.py`:

```
usage: fireprint.exe [-h] [-s SERVER] [-P PORT] -i [IMAGESOURCE] -u USERNAME [-e EVENTMSG] [-d] [-M SUBMONTHS] [-S SUBCURRENTSTREAK] [-m SUBMESSAGE] [-c CHEERMESSAGE] [-t CHEERTOTALBITS]

A thermal printer companion for Firebot

options:
  -h, --help            show this help message and exit
  -s, --server SERVER   print server host (default: 127.0.0.1)
  -P, --port PORT       print server port (default: 9100)
  -i, --imageSource [IMAGESOURCE]
                        full path to png image or URL of the user image (optional)
  -u, --username USERNAME
                        username for the receipt
  -e, --eventMsg EVENTMSG
                        message to display (use \n for line breaks)
  -d, --debug           save preview image instead of printing
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
> Use `\n` in string arguments to add line breaks (e.g. `--eventMsg "Thank you\nfor the sub!"`).
>
> Use `-d` to render a `preview.bmp` without wasting paper or needing the print server.

### Example command

```
python fireprint.py --server 127.0.0.1 \
    --image https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/castle_.png \
    --username "Castle_" \
    --subMessage "You da besh" \
    --subMonths 13 \
    --subCurrentStreak 3 \
    --eventMsg "Thanks for the\ntier 1 sub!"
```

The output should look like the following, and may not reflect the result when printed from Firebot.

<img src="https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/CLI_test.png" alt="Alt Text" width="300">

Once its confirmed to be working continue to the steps below.

## Firebot

[Download](https://github.com/ImaginaryResources/Fireprint/releases) the setupfile and import it to Firebot, (Settings -> Setups -> Import Setup).

### Import Questions

#### Enter full path to fireprint.exe. Example: C:\Fireprint\dist\fireprint.exe

Default: `blank`

#### Enter the print server host (default: 127.0.0.1)

Default: `blank`

> [!IMPORTANT]  
> Make sure `print_server.py` is running on the target machine before sending receipts.

### Result

After importing, test the "Fireprint Sub" event. It should look like the following.

<img src="https://raw.githubusercontent.com/ImaginaryResources/Fireprint/main/media/Firebot_test.png" alt="Alt Text" width="300">

### Default messages for events

Follow

```
-s $%fireprinterServer -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the follow!"
```

Sub

```
-s $%fireprinterServer -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the $subType sub!" --subMonths $subMonths --subCurrentStreak $subCurrentStreak --subMessage "$subMessage"
```

Sub Gifted

```
-s $%fireprinterServer -i $userAvatarUrl[$giftGiverUsername] -u $giftGiverUsername --eventMsg "Thank you for\n the gift to\n $giftReceiverUsername!"
```

Community Subs Gifted

```
-s $%fireprinterServer -i $userAvatarUrl[$giftGiverUsername] -u $giftGiverUsername --eventMsg "Thank you for\n $giftCount gifts to\n the community!"
```

Gift Sub Upgraded

```
-s $%fireprinterServer -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the upgraded\n gifted sub!"
```

Prime Sub Upgraded

```
-s $%fireprinterServer -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the upgraded\n prime sub!"
```

Cheer/Bits

```
-s $%fireprinterServer -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the $cheerBitsAmount bits!" --cheerTotalBits $cheerTotalBits --cheerMessage "$cheerMessage"
```

Gigantify Emote (Cheer/Bits)

```
-s $%fireprinterServer -i $gigantifiedEmoteUrl -u $userDisplayName --eventMsg "Giant emote\n for $cheerBitsAmount bits!" --cheerTotalBits $cheerTotalBits --cheerMessage "$cheerMessage"
```

Message Effect (Cheer/Bits)

```
-s $%fireprinterServer -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Msg effect\n for $cheerBitsAmount bits!" --cheerTotalBits $cheerTotalBits --cheerMessage "$cheerMessage"
```

On-Screen Celebration (Cheer/Bits)

```
-s $%fireprinterServer -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Emote party\n for $cheerBitsAmount bits!" --cheerTotalBits $cheerTotalBits
```

Tips/Donations

```
-s $%fireprinterServer -i $userAvatarUrl[$donationFrom] -u $donationFrom --eventMsg "Thank you for\n the $donationAmountFormatted dono!" --cheerMessage "$donationMessage"
```

Follower Goal

```
-s $%fireprinterServer -i $userAvatarUrl[$userDisplayName[$streamer]] -u $userDisplayName[$streamer] --eventMsg "Follower goal of\n $channelGoalTargetAmount[follow]\n is completed!"
```

Sub Goal

```
-s $%fireprinterServer -i $userAvatarUrl[$userDisplayName[$streamer]] -u $userDisplayName[$streamer] --eventMsg "Sub goal of\n $channelGoalTargetAmount[sub]\n is completed!"
```

Incoming Raid

```
-s $%fireprinterServer -i $userAvatarUrl[$userDisplayName] -u $userDisplayName --eventMsg "Thank you for\n the $raidViewerCount\n viewer raid!"
```

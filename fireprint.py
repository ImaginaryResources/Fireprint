from escpos.printer import Network, Dummy
import requests
import argparse
import arrow
import shutil
import codecs
import os

from py_star_tsp.escpos import EscposEmulator, PRESET_EPSON_TM_T88
from py_star_tsp import StarTSP


def get_current_date():
    now = arrow.now()
    return now.format("MMMM Do, YYYY HH:mm A")
 
def months_to_years_months(total_months):
    years = total_months // 12
    months = total_months % 12
    return years, months
    
def format_years_months(total_months):
    years, months = months_to_years_months(total_months)
    output = []
    if years > 0:
        output.append(f"{years} Year{'s' if years > 1 else ''}")
    if months > 0:
        output.append(f"{months} Month{'s' if months > 1 else ''}")
    return " ".join(output)
    
def download_png(source, imageName):
    png_path = f"{imageName.lower()}.png"

    if source.startswith("http://") or source.startswith("https://"):
        try:
            response = requests.get(source)
            response.raise_for_status()
            with open(png_path, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded successfully from URL to {png_path}")
            return png_path
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while downloading from URL: {e}")
            return None
    
    else:
        try:
            if not os.path.isfile(source):
                print(f"Local file {source} not found.")
                return None

            shutil.copy(source, png_path)
            print(f"Copied local PNG to {png_path}")
            return png_path

        except (OSError, shutil.Error) as e:
            print(f"Error copying local file: {e}")
            return None

def build_receipt(p, imageSource, username, eventMsg="", subMonths=0, subCurrentStreak=0, subMessage="", cheerMessage="", cheerTotalBits=0):
    if len(username) > 16:
        p.set(align='center', bold=False, width=1, height=1, custom_size=True)
    else:
        p.set(align='center', bold=False, width=2, height=2, custom_size=True)

    p.text(f"@{username}")
    p.ln(2)
    
    if eventMsg:
        p.set(align='center', bold=False, width=2, height=2, custom_size=True)
        p.text(eventMsg)
        p.ln(2)

    png_path = download_png(imageSource, username)

    if not png_path or not os.path.isfile(png_path):
        print(f"Error: Could not get the image for username '{username}'.")
        p.cut()
        return png_path  # caller handles the partial output

    try:
        p.image(png_path)
        p.ln(2)
    except Exception as e:
        print(f"Error loading image: {e}")
        p.text("Error loading image.\n")
    finally:
        if os.path.isfile(png_path):
            os.remove(png_path)

    p.set(align='center', bold=False, width=2, height=2, custom_size=True)

    if cheerTotalBits:
        p.text(f"{cheerTotalBits}\n Total cheered!")
        p.ln(2)
    if cheerMessage:
        p.set(align='center', bold=False, normal_textsize=True)
        p.text(cheerMessage)
        p.ln(2)
    
    if subMonths:
        p.text(format_years_months(subMonths))
        p.ln(2)
    if subCurrentStreak > 1:
        p.text(f"{format_years_months(subCurrentStreak)} Streak\n\n")
    if subMessage:
        p.set(align='center', bold=False, normal_textsize=True)
        p.text(subMessage)
        p.ln(2)
    
    p.set(align='center', bold=False, width=1, height=1, custom_size=True)
    p.text(get_current_date())
    p.cut(feed=False)


def print_receipt(serverHost, imageSource, username, eventMsg="", subMonths=0, subCurrentStreak=0, subMessage="", cheerMessage="", cheerTotalBits=0, debug=False, port=9100):
    d = Dummy()
    d.set_with_default()
    build_receipt(d, imageSource, username, eventMsg, subMonths, subCurrentStreak, subMessage, cheerMessage, cheerTotalBits)

    if debug:
        captured = []
        emulator = EscposEmulator(
            preset=PRESET_EPSON_TM_T88,
            on_print=lambda rs: captured.append(rs),
        )
        emulator.feed(d.output)
        raster_set = captured[0] if captured else emulator.flush()

        p = StarTSP()
        p.raster_width = PRESET_EPSON_TM_T88.print_width_dots
        for block in raster_set.blocks:
            p.add_raster(block)
        p.save_rendered("preview.bmp")
        print("Preview saved to preview.bmp")
    else:
        p = Network(serverHost, port=port)
        p._raw(d.output)
        p.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A thermal printer companion for Firebot")
    parser.add_argument("-s", "--server", default="127.0.0.1", help="print server host (default: 127.0.0.1)")
    parser.add_argument("-P", "--port", type=int, default=9100, help="print server port (default: 9100)")
    parser.add_argument("-i", "--imageSource", required=True, nargs="?", default=None, help="full path to png image or URL of the user image (optional)")
    parser.add_argument("-u", "--username", required=True, help="username for the receipt")
    parser.add_argument("-e", "--eventMsg", default="", help="message to display")
    parser.add_argument("-d", "--debug", action="store_true", help="save preview image instead of printing")
    parser.add_argument("-M", "--subMonths", type=int, default=0, help="number of months subbed")
    parser.add_argument("-S", "--subCurrentStreak", type=int, default=0, help="current sub streak in months")
    parser.add_argument("-m", "--subMessage", default="", help="sub message")
    parser.add_argument("-c", "--cheerMessage", default="", help="message from cheer")
    parser.add_argument("-t", "--cheerTotalBits", default="", help="number of bits cheered")

    args = parser.parse_args()

    for attr in ('eventMsg', 'subMessage', 'cheerMessage', 'username'):
        val = getattr(args, attr, None)
        if val:
            setattr(args, attr, codecs.decode(val, 'unicode_escape'))

    print_receipt(
        serverHost=args.server,
        imageSource=args.imageSource,
        username=args.username,
        eventMsg=args.eventMsg,
        subMonths=args.subMonths,
        subCurrentStreak=args.subCurrentStreak,
        subMessage=args.subMessage,
        cheerMessage=args.cheerMessage,
        cheerTotalBits=args.cheerTotalBits,
        debug=args.debug,
        port=args.port
    )

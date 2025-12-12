from escpos.printer import CupsPrinter, Win32Raw
from datetime import datetime
import platform
import requests
import argparse
import arrow
import shutil
import sys
import os

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
            response.raise_for_status()  # Raise an exception for HTTP errors
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

def print_receipt(printer, imageSource, username, eventMsg="", printImage=True, subMonths=0, subCurrentStreak=0, subMessage="", cheerMessage="", cheerTotalBits=0):
    # Configure thermal printer here https://python-escpos.readthedocs.io/en/latest/user/usage.html
    if platform.system() == "Windows":
        p = Win32Raw(printer)
    elif platform.system() == "Linux":  # requires pycups https://python-escpos.readthedocs.io/en/latest/user/printers.html#cups
        p = CupsPrinter(printer)
    else:
        raise OSError("Unsupported operating system")
    p.open()

    if len(username) > 16:
        p.set(align='center', bold=True, width=1, height=1, custom_size=True)
    else:
        p.set(align='center', bold=True, width=2, height=2, custom_size=True)

    p.text(f"@{username}")
    p.ln(2)
    
    if eventMsg:
        p.set(align='center', bold=True, width=2, height=2, custom_size=True)
        p.text(eventMsg)
        p.ln(2)

    png_path = download_png(imageSource, username)

    if not png_path or not os.path.isfile(png_path):
        print(f"Error: Could not get the image for username '{username}'.")
        p.cut()
        return  # Exit if the download failed

    try:
        p.image(png_path)
        p.ln(2)
    except Exception as e:
        print(f"Error loading image: {e}")
        p.text("Error loading image.\n")
    finally:
        if os.path.isfile(png_path):
            os.remove(png_path)  # Clean up after printing

    p.set(align='center', bold=True, width=2, height=2, custom_size=True)

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
    
    # Print current date and time to the end
    p.set(align='center', bold=True, width=1, height=1, custom_size=True)
    p.text(get_current_date())
    p.cut()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A thermal printer companion for Firebot")
    parser.add_argument("printer", help="name of the printer")
    parser.add_argument("imageSource", nargs="?", default=None, help="full path to png image or URL of the user image (optional)")
    parser.add_argument("username", help="username for the receipt")
    parser.add_argument("--eventMsg", default="", help="message to display")
    parser.add_argument("--subMonths", type=int, default=0, help="number of months subbed")
    parser.add_argument("--subCurrentStreak", type=int, default=0, help="current sub streak in months")
    parser.add_argument("--subMessage", default="", help="sub message")
    parser.add_argument("--cheerMessage", default="", help="message from cheer")
    parser.add_argument("--cheerTotalBits", default="", help="number of bits cheered")

    args = parser.parse_args()

    print_receipt(
        printer=args.printer,
        imageSource=args.imageSource,
        username=args.username,
        eventMsg=args.eventMsg,
        subMonths=args.subMonths,
        subCurrentStreak=args.subCurrentStreak,
        subMessage=args.subMessage,
        cheerMessage=args.cheerMessage,
        cheerTotalBits=args.cheerTotalBits
    )

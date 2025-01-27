#!/usr/bin/env python3

import qrcode
import random
from PIL import Image
import os
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--wordlist", help="List of payloads to generate", required=True)
parser.add_argument("-d", "--delay", type=int, help="Time in seconds between each qr code generation", required=False)
args= parser.parse_args()

class bcolors:
    OK = '\033[92m'
    FAIL = '\033[91m'
    RESET = '\033[0m'

def banner():
    print("""
[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m
[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m
[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m
[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m
[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m
[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m
[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m
[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m
[47m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[40m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[40m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m[47m  [0m[40m  [0m[47m  [0m
[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m[47m  [0m

    """)

def generate_qr_code(text, filename):
    qr = qrcode.QRCode()
    qr.add_data(text)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

def display_qr_code(wordlist):
    i=0
    with open(args.wordlist,'r') as wordlist:
        for payload in wordlist:
            filename = f"qr_code_{i+1}.png"
            generate_qr_code(payload, filename)
            img = Image.open(filename)
            print(f'\n{bcolors.OK}[*]{bcolors.RESET} Opening QR code for {bcolors.OK}{payload}{bcolors.RESET}')
            img.show()
            if args.delay:
                time.sleep(args.delay)
            else:
                time.sleep(1)
            os.remove(filename)

def main():
    display_qr_code(args.wordlist)

try:
    banner()
    main()
except KeyboardInterrupt:
    print(f'{bcolors.FAIL}[!]{bcolors.RESET} Script canceled')
except Exception as e:
    print(e)


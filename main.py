#!/usr/bin/env python

from signal import pause
from gpiozero import Button


def say_yeah():
    print('yeah')


def main():
    button = Button(5, bounce_time=0.3)
    while True:
        print('hey')
        button.wait_for_press()
        say_yeah()


if __name__ == "__main__":
    main()

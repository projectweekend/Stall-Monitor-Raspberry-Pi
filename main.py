#!/usr/bin/env python

from signal import pause
from gpiozero import Button


def say_yeah():
    print('yeah')


def main():
    button = Button(5, bounce_time=0.3)
    button.when_pressed = say_yeah
    pause()


if __name__ == "__main__":
    main()

#!/usr/bin/env python

from signal import pause
from gpiozero import Button


def say_hello():
    print('hello')


def say_bye():
    print('bye')


def main():
    button = Button(5, bounce_time=0.3)
    button.when_pressed = say_hello
    button.when_released = say_bye
    pause()


if __name__ == "__main__":
    main()

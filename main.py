#!/usr/bin/env python

from gpiozero import Button


def main():
    button = Button(5, bounce_time=0.3)
    while True:
        button.wait_for_press()
        print('yeah')


if __name__ == "__main__":
    main()

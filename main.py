#!/usr/bin/env python

import sys
from time import sleep
import RPi.GPIO as GPIO
from picloud_client import PiCloud


class StallMonitor(object):

    def __init__(self, pin_num, gpio, picloud):
        self._pin_num = pin_num
        self._gpio = gpio
        self._picloud = picloud

        self._gpio.setmode(self._gpio.BCM)
        self._gpio.setwarnings(False)
        self._gpio.setup(
            self._pin_num,
            self._gpio.IN,
            initial=self._gpio.HIGH,
            pull_up_down=self._gpio.PUD_UP)

    def run(self):
        while True:
            current_reading = self._gpio.input(self._pin_num)
            status = 'open' if current_reading else 'closed'
            self._picloud.publish(event='stall', data=status)
            sleep(1)

    def stop(self):
        self._gpio.cleanup()


def main():
    stall_monitor = StallMonitor(pin_num=18, gpio=GPIO, picloud=PiCloud())
    try:
        stall_monitor.run()
    except:
        sys.exit(1)
    finally:
        stall_monitor.stop()


if __name__ == "__main__":
    main()

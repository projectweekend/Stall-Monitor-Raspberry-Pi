#!/usr/bin/env python

import os
import sys
import time
import RPi.GPIO as GPIO

from pika_pack import Broadcaster


RABBIT_URL = os.getenv('RABBIT_URL', None)
assert RABBIT_URL

EXCHANGE = 'gpio_broadcast'

DEVICE_KEY = 'stall_monitor'

PIN = 18


class StallMonitor(object):

    def __init__(self):
        self._gpio = GPIO
        self._pin = PIN
        self._broadcaster = Broadcaster(
            rabbit_url=RABBIT_URL,
            exchange=EXCHANGE)
        self._last_pin_reading = None
        self.setup_gpio()

    def setup_gpio(self):
        self._gpio.setmode(self._gpio.BCM)
        self._gpio.setwarnings(False)
        self._gpio.setup(
            self._pin,
            self._gpio.IN,
            initial=self._gpio.HIGH,
            pull_up_down=self._gpio.PUD_UP)

    @staticmethod
    def _door_message(is_open):
        return {
            'timestamp': int(time.time()),
            'door_open': bool(is_open)
        }

    def send_stall_activity(self):
        pin_reading = self._gpio.input(self._pin)

        if self._last_pin_reading is None or self._last_pin_reading != pin_reading:
            self._last_pin_reading = pin_reading
            self._broadcaster.send(DEVICE_KEY, self._door_message(pin_reading))

    def start(self):
        while True:
            self._gpio.wait_for_edge(self._pin, self._gpio.BOTH)
            print("Door changed!")
            self.send_stall_activity()

    def stop(self):
        self._gpio.cleanup()


def main():

    stall_monitor = StallMonitor()

    try:
        stall_monitor.start()
    except:
        sys.exit(1)
    finally:
        stall_monitor.stop()


if __name__ == '__main__':
    main()

#!/usr/bin/env python

import os
import sys
import time
from pi_pin_manager import PinManager
from pika_pack import Broadcaster


RABBIT_URL = os.getenv('RABBIT_URL', None)
assert RABBIT_URL

EXCHANGE = 'gpio_broadcast'

DEVICE_KEY = 'stall_monitor'

PIN_CONFIG_FILE = './pins.yml'


class PinEventHandler(object):

    def __init__(self, gpio):
        self._gpio = gpio
        self._broadcaster = Broadcaster(
            rabbit_url=RABBIT_URL,
            exchange=EXCHANGE)
        self._last_pin_reading = None

    @staticmethod
    def _door_message(is_open):
        return {
            'timestamp': int(time.time()),
            'door_open': bool(is_open)
        }

    def send_stall_activity(self, pin_number):
        pin_reading = self._gpio.input(pin_number)

        if self._last_pin_reading is None or self._last_pin_reading != pin_reading:
            self._last_pin_reading = pin_reading
            self._broadcaster.send(DEVICE_KEY, self._door_message(pin_reading))


def main():
    pins = PinManager(
        config_file=PIN_CONFIG_FILE,
        event_handlers=PinEventHandler)

    try:
        # This has to stay running for the GPIO threaded event callbacks
        while True:
            time.sleep(0.500)
    except:
        sys.exit(1)
    finally:
        pins.cleanup()


if __name__ == '__main__':
    main()

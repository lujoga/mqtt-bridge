# MQTT bridge
# Copyright (C) 2019  Luca Schmid

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from sys import exit
from argparse import ArgumentParser
from signal import SIGINT, pause, signal
from bridge import Bridge

bridge = None

def signal_handler(sig, frame):
    print('Exiting...')
    if bridge:
        bridge.disconnect()
    exit(0)

def main():
    global bridge

    parser = ArgumentParser()
    parser.add_argument('sub', help='MQTT broker to subscribe to')
    parser.add_argument('pub', help='MQTT broker to publish to')
    parser.add_argument('-t', '--topics', help='Only relay given topics', nargs='*')
    args = parser.parse_args()

    signal(SIGINT, signal_handler)

    bridge = Bridge(args.sub, args.pub, args.topics or ['#'])
    bridge.connect()
    bridge.loop()

    pause()

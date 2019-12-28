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

from paho.mqtt.client import Client

def parse_addr(addr):
    i = addr.rfind(':')
    if i < 0:
        return (addr, 1883)

    return addr[:i], int(addr[i+1:])

def on_connect(client, userdata, flags, rc):
    for t in userdata.topics:
        client.subscribe(t)

def on_message(client, userdata, msg):
    userdata.publisher.publish(msg.topic, msg.payload, msg.qos, msg.retain)

class Bridge:
    def __init__(self, sub_addr, pub_addr, topics):
        self.sub_host, self.sub_port = parse_addr(sub_addr)
        self.pub_host, self.pub_port = parse_addr(pub_addr)
        self.topics = topics

        self.subscriber = Client()
        self.subscriber.user_data_set(self)
        self.subscriber.on_connect = on_connect
        self.subscriber.on_message = on_message

        self.publisher = Client()

    def connect(self):
        self.subscriber.connect_async(self.sub_host, self.sub_port)
        self.publisher.connect_async(self.pub_host, self.pub_port)

    def disconnect(self):
        self.subscriber.loop_stop()
        self.subscriber.disconnect()
        self.publisher.loop_stop()
        self.publisher.disconnect()

    def loop(self):
        self.subscriber.loop_start()
        self.publisher.loop_start()

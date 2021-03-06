from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import threading
import json
from EventEmitter import EventEmitter


class SingleClientHandler(WebSocket):
    def sendValue(self, key, value):
        message = json.dumps({ key: value })
        self.sendMessage(message)

    # @override
    def handleMessage(self):
        json_data = json.loads(self.data)
        if json_data['action'] == 'wifiSetting':
            EventEmitter.get().on_wifi_setting(json_data)


    # @override
    def handleConnected(self):
        print('New client connected:', self.address)

        EventEmitter.get().on_temperature += lambda x: self.sendValue('temperature', x)
        EventEmitter.get().on_pressure += lambda x: self.sendValue('pressure', x)
        EventEmitter.get().on_location += lambda x: self.sendValue('location', x)
        EventEmitter.get().on_combined_event_count += lambda x: self.sendValue('combined_event_count', x)
        EventEmitter.get().on_serial += lambda x: self.sendValue('serial', x)
        EventEmitter.get().set_ADC_readings += lambda x: self.sendValue('set_ADC_readings', x)


    # @override
    def handleClose(self):
        print('Client disconnected:', self.address)


class WebSocketHandler(object):
    def __init__(self, port):
        self._port = port

    def run(self):
        server = SimpleWebSocketServer('', self._port, SingleClientHandler)
        server.serveforever()


class WebSocket(object):
    def async_start(port=9000):
        web_socket_handler = WebSocketHandler(port=port)
        thread = threading.Thread(target=web_socket_handler.run)
        thread.start()


# This is how to get values
EventEmitter.get().on_wifi_setting += lambda x: print('SSID:', x['ssid'], '; Password: ', x['password'])

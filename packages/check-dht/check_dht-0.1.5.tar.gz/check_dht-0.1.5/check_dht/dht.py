import serial
import json
import nagiosplugin
import errno


class DeviceReportsError(Exception):
    """Error class used to report issues coming from the Pico itself when communication works"""

    def __init__(self, errno):
        self.code = errno

    def __str__(self) -> str:
        message = errno.errorcode[self.code]
        return f"Connection to Raspberry Pi successful, but device reports error {self.code} ({message})\nPlease ensure all header pins are securely connected!"


class DHT(nagiosplugin.Resource):
    """Domain model: digital humidity and temperature."""

    def __init__(self, port, baud):
        self.serial = serial.Serial(port, baud)

    def read_data(self):
        """Reads one line of data via serial and parses it as JSON"""
        line = self.serial.readline()
        data = json.loads(line)

        # Check for errors: if there is an error, the data may be unreliable!
        if data["error"] != 0:
            raise DeviceReportsError(data["error"])

        return data

    def probe(self):
        data = self.read_data()

        return [
            nagiosplugin.Metric("temperature", data["temperature"]),
            nagiosplugin.Metric("onboard", data["onboard"], context="temperature"),
            nagiosplugin.Metric("humidity", data["humidity"], uom="%"),
        ]

# check-dht
![PyPI](https://img.shields.io/pypi/v/check_dht)
![PyPI - Downloads](https://img.shields.io/pypi/dm/check-dht)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/check_dht)

Nagios plugin to monitor humidity and temperature data from a Raspberry Pi Pico

```console
$ check_dht
DHT OK - temperature is 23°C | humidity=48%;60;65;0;100 onboard=23°C;30;40 temperature=23°C;30;40
```

## Format
**Notice:** This plugin works in conjuction with the [pico-dht](https://github.com/j0hax/pico-dht) project! It expects a device to be available which periodically prints JSON data to a serial port:

```json
{
   "humidity":48,
   "temperature":23,
   "onboard":23,
   "error":0
}
```

- `humidity` and `temperature` are measurements taken directly from a DHT22/DHT11 sensor
- The RP2040s built-in temperature sensor is reported in the `onboard` field.
- In case of an Issue (e.g. I/O), a POSIX errno is set in the `error` field.

## Install
The recommended installation is via `pip install check-dht`.

### Manually
Alternatively, the source module can be executed after installing needed dependencies:

1. [pySerial](https://pyserial.readthedocs.io/en/stable/)
2. [nagiosplugin](https://nagiosplugin.readthedocs.io/en/stable/)

## Usage
```console
$ poetry run check_dht --help
usage: check_dht [-h] [-p PORT] [-b BAUD] [-w TEMP] [-c TEMP]
                 [--humidity-warning PERCENT] [--humidity-critical PERCENT]

Nagios plugin to monitor humidity and temperature data

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  the serial file to read from
  -b BAUD, --baud BAUD  baudrate of the serial port
  -w TEMP, --warning TEMP
                        return warning if air temperature is beyond TEMP
  -c TEMP, --critical TEMP
                        return critical if air temperature is beyond TEMP
  --humidity-warning PERCENT
                        return warning if humidity is beyond PERCENT
  --humidity-critical PERCENT
                        return critical if humidity is beyond PERCENT

(c) Johannes Arnold 2023. This software is published under the terms of the
GNU GPLv3. For the companion project to this plugin, see
https://github.com/j0hax/pico-dht
```

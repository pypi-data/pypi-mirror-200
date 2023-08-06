#!/usr/bin/env python3
import argparse
import sys
import nagiosplugin
import logging
from .dht import DHT


def main():
    parser = argparse.ArgumentParser(
        description="Nagios plugin to monitor humidity and temperature data",
        epilog="(c) Johannes Arnold 2023. This software is published under the terms of the GNU GPLv3. For the companion project to this plugin, see https://github.com/j0hax/pico-dht",
    )

    parser.add_argument(
        "-p",
        "--port",
        default="/dev/ttyACM0",
        help="the serial file to read from",
    )

    parser.add_argument(
        "-b", "--baud", default=115200, help="baudrate of the serial port"
    )

    parser.add_argument(
        "-w",
        "--warning",
        metavar="TEMP",
        default=30,
        help="return warning if air temperature is beyond TEMP",
    )

    parser.add_argument(
        "-c",
        "--critical",
        metavar="TEMP",
        default=40,
        help="return critical if air temperature is beyond TEMP",
    )

    parser.add_argument(
        "--humidity-warning",
        metavar="PERCENT",
        default=60,
        help="return warning if humidity is beyond PERCENT",
    )

    parser.add_argument(
        "--humidity-critical",
        metavar="PERCENT",
        default=65,
        help="return critical if humidity is beyond PERCENT",
    )

    args = parser.parse_args()

    check = nagiosplugin.Check(
        DHT(args.port, args.baud),
        nagiosplugin.ScalarContext(
            name="temperature",
            fmt_metric="{valueunit}°C",
            warning=args.warning,
            critical=args.critical,
        ),
        nagiosplugin.ScalarContext(
            name="humidity",
            warning=args.humidity_warning,
            critical=args.humidity_critical,
        ),
    )

    try:
        check.main()
    except Exception as e:
        logging.exception(e)
        sys.exit(1)


if __name__ == "__main__":
    main()

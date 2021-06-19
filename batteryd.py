#!/usr/bin/env python
import argparse
import collections
import logging
import os
import re
import subprocess
import time

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-a', '--apps',
                    help='only run battery checks when any of these are opened, '
                         'separate each app with "|". e.g. Steam|LeagueClient')
parser.add_argument('-s', '--seconds-between-checks',
                    help='seconds between battery checks',
                    type=int,
                    default=10)
args = parser.parse_args()
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)

def get_battery_status(
    RE_BATTERY_PERCENT=re.compile(r'(\d+)%'),
    RE_IS_CHARGING=re.compile(r'AC Power'),
    CMD_PMSET=('pmset', '-g', 'batt'),
):
    output = subprocess.check_output(CMD_PMSET)
    return (
        int(RE_BATTERY_PERCENT.search(output).group(1)),
        bool(RE_IS_CHARGING.search(output)),
    )

def any_listed_app_is_running(CMD_PGREP = ('pgrep', args.apps)):
    return subprocess.call(CMD_PGREP, stdout=subprocess.PIPE) == 0

MAX_DEQUE_LENGTH = 6
battery_history = collections.deque(maxlen=MAX_DEQUE_LENGTH)
while True:
    if args.apps and not any_listed_app_is_running():
        logging.info('skipping battery check, apps are all off: %s', args.apps)
        time.sleep(args.seconds_between_checks)
        continue

    current_battery, is_charging = get_battery_status()
    battery_history.append(current_battery)
    is_losing_battery = current_battery < battery_history[0]

    logging.info('%d, %s, %s', current_battery, is_charging, battery_history)

    if not is_charging:
        subprocess.check_call(['say', 'charger is not plugged in'])
    if is_losing_battery:
        subprocess.check_call(['say', 'battery is draining'])

    time.sleep(args.seconds_between_checks)

# Battery Checker

## Problem

My macbook is often in the "charging" state but is actually not charging,
and sometimes I just forget to plug in my charger 🤦
This causes my laptop to run out of battery while I'm playing video games
such as Steam or League of Legends 😭

## Solution

Laptop will say "battery is draining" if the battery is not increasing, and
will say "charger is not plugged in" if you didn't plug in your charger.

Done via a long-running script that can be run as a background process.

## How to use

Assumes you're familiar with opening and running commands in the terminal.

To run as a background process:

```sh
nohup ./batteryd.py >/dev/null 2>&1 &
```

Configs you can set:

```sh
❯ ./batteryd.py --help
usage: batteryd.py [-h] [-a APPS] [-s SECONDS_BETWEEN_CHECKS]

optional arguments:
  -h, --help            show this help message and exit
  -a APPS, --apps APPS  only run battery checks when any of these are opened,
                        separate each app with "|". e.g. Steam|LeagueClient
                        (default: None)
  -s SECONDS_BETWEEN_CHECKS, --seconds-between-checks SECONDS_BETWEEN_CHECKS
                        seconds between battery checks (default: 10)
```

e.g.

```sh
nohup ./batteryd.py --apps 'Steam|LeagueClient' --seconds-between-checks 30 >/dev/null 2>&1 &
```

To check if the background process is running:

```sh
ps -ax | grep 'batteryd.py'
```

To kill the background process:

```sh
kill <pid from the ps cmd>
```

## How it works

Read code at [`batteryd.py`](https://github.com/nickwu241/battery-checker/blob/master/batteryd.py) or can ask me.

## Limitations

- Only works for macOS
- Not friendly for people not familiar with the terminal
  - It's possible create this as a macOS app instead... 🤔

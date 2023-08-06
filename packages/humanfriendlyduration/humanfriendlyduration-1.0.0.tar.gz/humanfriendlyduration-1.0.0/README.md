uman-friendly-duration

Human-friendly-duration is a Python package that formats a duration, given as a number of seconds, in a human-friendly way. The package can be used to convert the duration of time into a combination of years, days, hours, minutes, and seconds.
Installation

human-friendly-duration can be installed using pip:

sh

pip install human-friendly-duration

Usage

python

from humanfriendly_duration import format_duration

print(format_duration(62)) # output: 1 minute and 2 seconds
print(format_duration(3662)) # output: 1 hour, 1 minute and 2 seconds

If the duration is zero, it will return "now".

python

print(format_duration(0)) # output: now


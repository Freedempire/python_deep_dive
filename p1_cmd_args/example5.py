import argparse
import datetime

parser = argparse.ArgumentParser(description='Return a person\' exact age')
parser.add_argument('-f', '--first-name', required=False, help='first name') # option
parser.add_argument('-l', '--last-name', required=True, help='last name')
parser.add_argument('-d', '--dob', required=True, help='date of birth in yyyy-mm-dd form', dest='dob_string')

args = parser.parse_args()
first_name = args.first_name
last_name = args.last_name
name = f'{first_name} {last_name}' if first_name else last_name

try:
    dob = datetime.datetime.strptime(args.dob_string, '%Y-%m-%d').date()
except ValueError: # catches format not matching error
    print('invalid dob format')
    raise

today = datetime.date.today()
today_month = today.month
today_year = today.year

if today < dob:
    print(f'{name} was born in future!')
else:
    days_delta = today.day - dob.day
    if days_delta < 0:
        today_month -= 1
        if today_month == 0:
            today_month = 12
            today_year -= 1
        today_one_month_ago = datetime.date(today_year, today_month, today.day)
        extra_days = (today - today_one_month_ago).days
        days_delta += extra_days # suppose each month has 30 days

    months_delta = today_month - dob.month
    if months_delta < 0:
        months_delta += 12
        today_year -= 1

    years_delta = today_year - dob.year

    print(f'{name}\'s exact age: {years_delta} years, {months_delta} months, {days_delta} days')

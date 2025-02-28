from nselib import capital_market
from nselib import trading_holiday_calendar

# print(trading_holiday_calendar())

# print(capital_market.bhav_copy_equities('01-03-2024'))

print(capital_market.short_selling_data(period='1M'))
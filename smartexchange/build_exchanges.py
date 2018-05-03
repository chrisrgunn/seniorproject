from app import app, Exchange, session, User, Prediction, TradeRate
import datetime
from forex_python.converter import CurrencyRates
app.app_context().push()
#
# currency_from='USD'
# # currency_from='AUD'
# currency_to='EUR'
# currency_to='AUD'


# new_exchange = Exchange(currency_from=currency_from, currency_to=currency_to)
# new_exchange.save()

# exchange = Exchange.query.filter(Exchange.currency_from == currency_from, Exchange.currency_to == currency_to).first()
#
# if exchange is None:
#     print('its none')
# else:
#     print('present')


# countries = ["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR",
# "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR",
# "NOK", "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "SGD", "THB", "TRY", "USD", "ZAR"]
#
#
# for i in range(0, len(countries)):
#     for j in range(0, len(countries)):
#         exchange = Exchange.query.filter(Exchange.currency_from == countries[i],
#                                          Exchange.currency_to == countries[j]).first()
#         if exchange is None:
#             new_exchange = Exchange(currency_from=countries[i], currency_to=countries[j])
#             new_exchange.save()

# print(len(countries))
# print(len(countries)*len(countries))
# print(len(Exchange.query.all()))


currency_rates = CurrencyRates()

data=[]
num_of_data_points=10
currency_from = "AUD"
currency_to = "BGN"

exchange = Exchange.query.filter(Exchange.currency_from == currency_from,
                                 Exchange.currency_to == currency_to).first()
# if exchange is None:
#     print("no exchange found!")
# else:
#     print("exchange found! removing...")
#     exchange.remove()

if exchange is None:
    new_exchange = Exchange(currency_from=currency_from, currency_to=currency_to)
    new_exchange.save()
    exchange=new_exchange



old_trade_rates = TradeRate.query.filter(TradeRate.exchange==exchange).all()
print(len(old_trade_rates))
old_trade_rates_dict = {}

for old_trade_rate in old_trade_rates:
    old_trade_rates_dict[old_trade_rate.date]=old_trade_rate.price

# print(old_trade_rates_dict)


for idx in range(0, num_of_data_points):
    curr_date = datetime.date.today() - datetime.timedelta(idx)
    curr_datetime = datetime.datetime.combine(curr_date, datetime.datetime.min.time())



    # If we have the current price point, use it. Otherwise save it to db
    if (curr_datetime in old_trade_rates_dict):
        print(old_trade_rates_dict[curr_datetime])
    else:
        print("does not exist. saving new price to db")
        curr_price = currency_rates.get_rate(currency_from, currency_to, curr_date)
        new_trade_rate = TradeRate(price=curr_price, date=curr_datetime, exchange=exchange)
        new_trade_rate.save()





# dates = '[datetime.date(2018, 4, 20), datetime.date(2018, 4, 21), datetime.date(2018, 4, 22), datetime.date(2018, 4, 23), datetime.date(2018, 4, 24), datetime.date(2018, 4, 25)]'
# dates=dates[1:-1]
# dates=dates.replace("datetime.date(","")
# dates=dates.replace(")","")
#
# dates=dates.split(',')
#
# new_dates=[]
#
# for idx in range(0,len(dates)/3):
#     year=int(dates[idx*3])
#     month=int(dates[idx*3+1])
#     day=int(dates[idx*3+2])
#     new_dates.append(datetime.datetime(year=year, month=month, day=day))
#
# for date in new_dates:
#     print(date)

# user = User.query.filter(User.username == 'chris').first()
# user.avatar_image_reference='asdf'
# user.save()

# user = User.query.filter(User.username == session['username']).first()
# print(user.username)
# print(exchange.currency_from)

#
# predictions = Prediction.query.filter(Prediction.user.username == 'chris').descending(Prediction.date)
# print(predictions)
# print(predictions[0].date)
# print(predictions[1].date)




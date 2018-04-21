from app import app, Exchange, session, User, Prediction
import datetime
app.app_context().push()

currency_from='USD'
# currency_from='AUD'
currency_to='EUR'
# currency_to='AUD'


# new_exchange = Exchange(currency_from=currency_from, currency_to=currency_to)
# new_exchange.save()

exchange = Exchange.query.filter(Exchange.currency_from == currency_from, Exchange.currency_to == currency_to).first()

if exchange is None:
    print('its none')
else:
    print('present')


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


predictions = Prediction.query.filter(Prediction.user.username == 'chris').descending(Prediction.date)
print(predictions)
print(predictions[0].date)
print(predictions[1].date)




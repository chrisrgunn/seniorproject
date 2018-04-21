from app import app, render_template, flash, session, redirect, \
    url_for, request, make_response, Prediction, Exchange, User, TradeRate

import os
import time
import warnings
import numpy as np
from numpy import newaxis
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential

from forex_python.converter import CurrencyRates
import datetime

import time
import matplotlib.pyplot as plt

import io
import base64

windows_first_data_point=[]

@app.route('/new_prediction', methods=['POST', 'GET'])
def new_prediction():
    if request.method == 'POST':
        if request.form['form-btn'] == "Generate Prediction":
            currency_to = request.form['currency_to']
            currency_from = request.form['currency_from']
            num_days_in_past = request.form['num_days_in_past']
            num_days_in_future = request.form['num_days_in_future']
            seq_len = request.form['seq_len']
            epochs = request.form['epochs']
            batch_size = request.form['batch_size']

            if num_days_in_past =='' or num_days_in_future=='' or seq_len=='' or \
                            epochs=='' or batch_size=='' or currency_to=='Select' or \
                            currency_from=='Select':
                flash('Fields cannot be empty!', "danger")
                return render_template("new_prediction.html")

            if currency_from == currency_to:
                flash('Cannot select the same From and To currency!', "danger")
                return render_template("new_prediction.html")

            num_days_in_past = int(num_days_in_past)
            num_days_in_future = int(num_days_in_future)
            seq_len = int(seq_len)
            epochs = int(epochs)
            batch_size = int(batch_size)

            data_layers = create_prediction(currency_to, currency_from, num_days_in_past,
                                            num_days_in_future, seq_len, epochs, batch_size)

            currency_rates = CurrencyRates()
            price_today = currency_rates.get_rate(currency_from, currency_to)
            date_today = datetime.date.today()
            dates = []
            for idx in range(0, len(data_layers[3])+1):
                dates.append(datetime.date.today()+datetime.timedelta(idx))

            return render_template("new_prediction.html", true_data=data_layers[0], true_data_denormalized=data_layers[1],
                                   predicted_data=data_layers[2], predicted_data_denormalized=data_layers[3],
                                   true_data_str=str(data_layers[0])[1:-1], predicted_data_str=str(data_layers[2])[1:-1],
                                   dates=dates, date_today=date_today, price_today=price_today, results=True,
                                   currency_from=currency_from, currency_to=currency_to, num_days_in_past=num_days_in_past,
                                   num_days_in_future=num_days_in_future, seq_len=seq_len, epochs=epochs, batch_size=batch_size)
        elif request.form['form-btn'] == "Save Prediction":
            currency_to = request.form['currency_to']
            currency_from = request.form['currency_from']
            num_days_in_past = int(request.form['num_days_in_past'])
            num_days_in_future = int(request.form['num_days_in_future'])
            seq_len = int(request.form['seq_len'])
            epochs = int(request.form['epochs'])
            batch_size = int(request.form['batch_size'])

            dates = request.form['dates']
            predictions = request.form['predictions']
            price_today = request.form['price_today']

            exchange = Exchange.query.filter(Exchange.currency_from == currency_from, Exchange.currency_to == currency_to).first()

            if exchange is None:
                exchange = Exchange(currency_from=currency_from, currency_to=currency_to)
                exchange.save()

            user = User.query.filter(User.username == session['username']).first()

            dates = dates[1:-1]
            dates = dates.replace("datetime.date(", "")
            dates = dates.replace(")", "")

            dates = dates.split(',')

            dates_formatted = []

            for idx in range(0, len(dates) / 3):
                year = int(dates[idx * 3])
                month = int(dates[idx * 3 + 1])
                day = int(dates[idx * 3 + 2])
                dates_formatted.append(datetime.datetime(year=year, month=month, day=day))

            print(dates_formatted)
            print(len(dates_formatted))

            predictions=predictions[1:-1]
            predictions = predictions.split(',')
            predictions = [price_today] + predictions
            print(predictions)
            print(len(predictions))

            trade_rates = []

            for idx in range(0,len(predictions)):
                curr_trade_rate = TradeRate(price=float(predictions[idx]), date=dates_formatted[idx], exchange=exchange)
                # curr_trade_rate.save()
                trade_rates.append(curr_trade_rate)

            new_prediction = Prediction(date=datetime.datetime.now(), user=user, exchange=exchange,
                                        num_days_in_past=num_days_in_past, num_days_in_future=num_days_in_future,
                                        seq_len=seq_len, epochs=epochs, batch_size=batch_size, trade_rates=trade_rates)

            new_prediction.save()

            flash("Prediction saved!", "success")

            return redirect(url_for("new_prediction"))

    return render_template("new_prediction.html")

def load_data(seq_len, num_of_data_points, currency_from, currency_to):
    currency_rates = CurrencyRates()

    data = []
    for idx in range(0, num_of_data_points):
        curr_date = datetime.date.today()-datetime.timedelta(idx)
        curr_price = currency_rates.get_rate(currency_from, currency_to, curr_date)
        data.append(curr_price)

    sequence_length = seq_len + 1 # add 1 to the sequence length
    results = []

    for index in range(len(data) - sequence_length):
        # append an array to each index of the results array where each inner array
        # is subset of the data for each of the sequences
        # each array within results is a "window"
        results.append(data[index: index + sequence_length])

    # the length of results is 1 + seq_len subracted to the lenght of data (i.e. if data=100 and seq=50 -> results=49)

    # save the first data point of every window before normalizing so we can denormalize back later
    for window in results:
        windows_first_data_point.append(window[0])

    # # save the first data point of the last window so that we can normalize the predictions
    # last_data_point = results[-1][0]

    # normalize the results
    results = normalize_windows_multiple(results)

    results = np.array(results) # organize results into multidimensional array

    row = round(0.9 * results.shape[0]) # get an integer 90% of the training data

    train = results[:int(row), :] # take 90% of results

    # np.random.shuffle(train) # shuffle training data windows

    '''
    each index of x_train array will contain the sequential number of seq_length
    of data points (e.g. first 5 data points). each index of y_train will contain
    the next data point so that the window of x_train can predict the next point
    '''
    x_train = train[:, :-1]
    y_train = train[:, -1]
    '''
    x_test and y_test are the same as x_train and y_train except that they are
    composed of the latter 10% of the data used for testing.
    '''
    x_test = results[int(row):, :-1]
    y_test = results[int(row):, -1]
    '''
    need to get x_train and x_test in the correct ordering for the neural net
    to use
    '''
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    return [x_train, y_train, x_test, y_test]

def normalize_windows_multiple(windows):
    normalized_windows = []
    for window in windows:
        normalized_window = [((float(data_point) / float(window[0])) - 1) for data_point in window]
        normalized_windows.append(normalized_window)
    return normalized_windows

def normalize_window(window):
    normalized_window = []

    for data_point in window:
        normalized_data_point = ((float(data_point) / float(window[0])) - 1)
        normalized_window.append(normalized_data_point)
    return normalized_window

def denormalize_window_multiple(windows, windows_first_data_point):
    denormalized_windows = []
    index = 0

    for window in windows:
        denormalized_window = [((float(data_point) + 1) * float(windows_first_data_point[index])) for data_point in
                               window]
        denormalized_windows.append(denormalized_window)
        index += 1
    return denormalized_windows

def denormalize_window(window, first_data_point):
    denormalized_window = []

    for data_point in window:
        denormalized_data_point = ((float(data_point) + 1) * float(first_data_point))
        denormalized_window.append(denormalized_data_point)
    return denormalized_window

def build_model(layers):
    model = Sequential()  # linear stack of layers

    # first layer - LSTM layer
    model.add(LSTM(
        input_shape=(layers[1], layers[0]),
        output_dim=layers[1],  # number of units in this layer
        return_sequences=True))  # True = the output of this layer ALWAYS fed into the next layer
    model.add(Dropout(0.2))  # add 20% dropout to this layer

    model.add(LSTM(
        layers[2],
        return_sequences=False))  # False = output is only fed to next layer at the END of the sequence. Instead of outputting
    # a prediction sequence, it INSTEAD outputs a prediction vector for the WHOLE input sequence
    model.add(Dropout(0.2))

    # use linear dense layer to aggregate data from this prediction vector into 1 value
    model.add(Dense(
        output_dim=layers[3]))
    model.add(Activation("linear"))

    start = time.time()
    # compile our model into popular loss function called mean squared error and use gradient descent as
    # our optimizer (labled rmsprop)
    model.compile(loss="mse", optimizer="rmsprop")
    print("> Compilation Time : ", time.time() - start)
    return model

# predict the graph based on the last window, up through the nubmer of days in the future
def predict_sequence_full(model, data, window_size, num_days_in_future):
    curr_frame = data[-1]

    predicted = []
    for i in range(num_days_in_future + window_size):
        predicted.append(model.predict(curr_frame[newaxis, :, :])[0, 0])
        curr_frame = curr_frame[1:]
        curr_frame = np.insert(curr_frame, [window_size - 1], predicted[-1], axis=0)
    return predicted

@app.route('/simple2/<true_data>/<predicted_data>')
def plot_results(predicted_data, true_data):

    print('\n')
    print(true_data)
    print('\n')

    if true_data is None or true_data == '':
        true_data = [1,2,3,4,5]
    else:
        true_data = true_data.split(' ')
        true_data = [float(i[:-1]) for i in true_data if i != '']

    if predicted_data is None or predicted_data == '':
        predicted_data = [6, 7, 8]
    else:
        predicted_data = predicted_data.split(' ')
        predicted_data = [float(i[:-1]) for i in predicted_data if i!= '']


    import StringIO
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')

    #Pad the list of predictions to shift it in the graph to it's correct start
    padding = [None for p in range(len(true_data))]
    plt.plot(padding + predicted_data, label='Prediction')
    plt.legend()

    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

def create_prediction(currency_to, currency_from, num_days_in_past, num_days_in_future,
                      seq_len, epochs, batch_size):

    global_start_time = time.time()
    # epochs = number of times that the LSTM network cycles through all of the sequence windows in the training set
    # if data has less structure, then a larger number of epochs required

    print('> Loading data... ')
    # load data
    x_train, y_train, x_test, y_test = load_data(seq_len, num_days_in_past, currency_from, currency_to)

    print('Data Loaded. Compiling...')

    first_lstm_layer_input_dimension = 1
    second_lstm_layer_input_dimension = 1

    first_lstm_layer_num_units = seq_len
    second_lstm_layer_num_units = 100

    model = build_model([first_lstm_layer_input_dimension, first_lstm_layer_num_units,
                              second_lstm_layer_num_units, second_lstm_layer_input_dimension])

    # train our model with the fit function
    model.fit(
        x_train,
        y_train,
        batch_size=batch_size,  # 512 #Lower batch sizes tend to work better with bigger datasets
        # and higher batch sizes tend to work better with smaller datasets
        # why?
        nb_epoch=epochs,
        validation_split=0.05)

    # seq_len is how many steps the model will predict for at several points in our graph

    # get our predictions
    predictions = predict_sequence_full(model, x_test, seq_len, num_days_in_future)

    print('Training duration (s) : ', time.time() - global_start_time)

    print('\nlast %d days (normalized):' % seq_len)
    last_days = y_test[-seq_len:]
    # last_days = lstm.data[-seq_len:]
    print(last_days)
    print('\nlast %d days (denormalized):' % seq_len)
    last_days_denormalized = denormalize_window(last_days, windows_first_data_point[-1])
    print(last_days_denormalized)

    # print('\n\n')
    # print(lstm.windows_first_data_point[-1])
    # print('\n\n')
    predictions = predictions[seq_len:]
    print('\nnext %d days (normalized):' % num_days_in_future)
    print(predictions)
    print('\nnext %d days (denormalized):' % num_days_in_future)
    predictions_denormalized = denormalize_window(predictions, windows_first_data_point[-1])
    print(predictions_denormalized)
    print(len(predictions_denormalized))

    # print(y_test[])

    # print(predictions)

    # plot_results(predictions, y_test)
    return last_days, last_days_denormalized, predictions, predictions_denormalized



@app.route('/simple')
def simple():
    import datetime
    import StringIO
    import random

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response
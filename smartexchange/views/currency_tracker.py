from app import app, render_template, flash, session, redirect, url_for, Prediction, TradeRate

@app.route('/currency_tracker')
def currency_tracker():
    predictions = Prediction.query.filter(Prediction.user.username == session['username']).descending(Prediction.date)

    return render_template("currency_tracker.html", predictions=predictions)

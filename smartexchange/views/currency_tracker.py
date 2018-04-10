from app import app, render_template, flash, session, redirect, url_for

@app.route('/currency_tracker')
def currency_tracker():
    return render_template("currency_tracker.html")

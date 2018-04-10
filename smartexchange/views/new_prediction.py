from app import app, render_template, flash, session, redirect, url_for

@app.route('/new_prediction')
def new_prediction():
    return render_template("new_prediction.html")

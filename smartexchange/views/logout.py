from app import app, render_template, flash, session

@app.route('/logout')
def logout():
    session['username'] = None
    flash("You have been logged out!", "success")
    return render_template('home.html')

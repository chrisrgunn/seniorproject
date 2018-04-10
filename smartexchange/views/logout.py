from app import app, render_template, flash, session, redirect, url_for

@app.route('/logout')
def logout():
    session['username'] = None
    flash("You have been logged out!", "success")
    return redirect(url_for("index"))
    # return render_template('home.html')

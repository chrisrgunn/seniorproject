from app import app, render_template, flash, redirect, request, url_for, session, User, salt, CurrencyRates
import bcrypt

@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    curr_rates = CurrencyRates()
    eur_usd_rate = curr_rates.get_rate('EUR', 'USD')
    gbp_usd_rate = curr_rates.get_rate('GBP', 'USD')
    inr_usd_rate = curr_rates.get_rate('USD', 'INR')
    jpy_usd_rate = curr_rates.get_rate('USD', 'JPY')

    if request.method == 'POST':
        if request.form['form-btn'] == "SIGN IN":
            login_user = User.query.filter(User.username == request.form['username/email']).first()
            if login_user:
                if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user.password.encode('utf-8')) == login_user.password.encode('utf-8'):
                    session['username'] = request.form['username/email']
                    flash("Sign in successful!", "success")
                    return redirect(url_for("index", eur_usd_rate=eur_usd_rate, gbp_usd_rate=gbp_usd_rate, inr_usd_rate=inr_usd_rate, jpy_usd_rate=jpy_usd_rate))
                flash("Invalid password!", "danger")
                return redirect(url_for("index", eur_usd_rate=eur_usd_rate, gbp_usd_rate=gbp_usd_rate, inr_usd_rate=inr_usd_rate, jpy_usd_rate=jpy_usd_rate))
            flash('Invalid username!', "danger")
            return redirect(url_for("index", eur_usd_rate=eur_usd_rate, gbp_usd_rate=gbp_usd_rate, inr_usd_rate=inr_usd_rate, jpy_usd_rate=jpy_usd_rate))
        elif request.form['form-btn'] == "SIGN UP":
            if User.query.filter(User.username == request.form['username']).first() is not None:
                flash ("Username already taken!", "danger")
                return render_template('home.html', eur_usd_rate=eur_usd_rate, gbp_usd_rate=gbp_usd_rate, inr_usd_rate=inr_usd_rate, jpy_usd_rate=jpy_usd_rate)
            if User.query.filter(User.email == request.form['email']).first() is not None:
                flash("Email already taken!", "danger")
                return render_template('home.html', eur_usd_rate=eur_usd_rate, gbp_usd_rate=gbp_usd_rate, inr_usd_rate=inr_usd_rate, jpy_usd_rate=jpy_usd_rate)

            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), salt)
            new_user = User(name=request.form['name'], username=request.form['username'], password=hashpass.decode("utf-8"), email=request.form['email'])
            new_user.save()
            flash("Account created successfully!", "success")
    return render_template('home.html', eur_usd_rate=eur_usd_rate, gbp_usd_rate=gbp_usd_rate, inr_usd_rate=inr_usd_rate, jpy_usd_rate=jpy_usd_rate)
from app import app, render_template
#
# @app.route('/')
# @app.route('/index')
# @app.route('/home')
# def home_page():
#     online_users = mongo.db.users.find({'online': True})
#     return render_template('user.html',
#         online_users=online_users)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():

    #
    # if 'username' in session:
    #     return 'You are logged in as ' + session['username']
    return render_template('index.html')
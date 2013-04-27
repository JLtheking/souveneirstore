from flask import *
from functools import wraps
import sqlite3

# DATABASE = '/home/polaricicle/mysite/sales.db'

app = Flask(__name__)
# app.config.from_object(__name__)

# def connect_db():
    # return sqlite3.connect(app.config['DATABASE'])

app.secret_key = 'bleepbloopilikeponies'

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/store')
def store():
		#g.db  = connect_db()
		#cur = g.db.execute('select rep_name, amount from reps')
		#sales = [dict(rep_name=row[0], amount=row[1]) for row in cur.fetchall()]
		#g.db.close()
		return render_template('store.html')

@app.route('/confirm')
def confirm():
  return render_template('confirm.html')

@app.route('/aboutUs')
def aboutUs():
  return render_template('aboutUs.html')

def login_required(test):
  @wraps(test)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return test(*args, **kwargs)
    else:
      flash('You need to login first.')
      return redirect(url_for('log'))
  return wrap

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('log'))

@app.route('/myAccount')
@login_required
def myAccount():
  return render_template('myAccount.html')

@app.route('/log', methods=['GET', 'POST'])
def log():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('myAccount'))
	return render_template('log.html', error = error)

if __name__ == '__main__':
  app.run(debug=True)
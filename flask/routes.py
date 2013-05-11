from flask import *
from functools import wraps
import sqlite3
import datetime

DB = 'DATABASE.db'

#DB = '/home/polaricicle/mysite/DATABASE.db'

app = Flask(__name__)
app.config.from_object(__name__)



def connect_db():
    return sqlite3.connect(app.config['DB'])

app.secret_key = 'friendshipismagic'

def login_required(test):
  @wraps(test)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return test(*args, **kwargs)
    else:
      flash('You need to login first.')
      return redirect(url_for('log'))
  return wrap

def admin_required(test):
  @wraps(test)
  def wrap(*args, **kwargs):
    if 'logged_in' in session and session['logged_in'] == "admin":
      return test(*args, **kwargs)
    else:
      flash('You need administrator privileges to access this page.')
      return redirect(url_for('log'))
  return wrap

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/store')
@login_required
def store():
	return render_template('store.html')

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')

@app.route('/add_td', methods = ['POST'])
def add_td():
	tc = request.form['total']
	if tc == "0.00":
		flash('You have to purchase something first!')
		return redirect(url_for('store'))
	else:
		atd = connect_db()
		atd.execute('DROP TABLE IF EXISTS TD')
		atd.execute('CREATE TABLE TD(Total_price TEXT, A4_lecture_pad INT, Seven_colour_sticky_note_with_pen INT, A5_note_book_with_zip_bag INT, Pencil INT, Stainless_steel_tumbler INT, A4_clear_holder INT, A4_vanguard_file INT, Name_card_holder INT, Umbrella INT, School_badge_Junior_High INT, School_badge_Senior_High INT, Dunman_dolls_pair INT)')
		atd.execute('INSERT INTO TD (Total_price, A4_lecture_pad, Seven_colour_sticky_note_with_pen, A5_note_book_with_zip_bag, Pencil, Stainless_steel_tumbler, A4_clear_holder, A4_vanguard_file, Name_card_holder, Umbrella, School_badge_Junior_High, School_badge_Senior_High, Dunman_dolls_pair) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',[request.form['total'], request.form['list1'], request.form['list2'], request.form['list4'], request.form['list5'], request.form['list6'], request.form['list7'], request.form['list8'], request.form['list9'], request.form['list10'], request.form['list11'], request.form['list12'], request.form['list13']])
		atd.commit()
		atd.close()
		return redirect(url_for('confirm'))

@app.route('/confirm')
def confirm():
	atd = connect_db()
	cur = atd.execute('SELECT Total_price, A4_lecture_pad, Seven_colour_sticky_note_with_pen, A5_note_book_with_zip_bag, Pencil, Stainless_steel_tumbler, A4_clear_holder, A4_vanguard_file, Name_card_holder, Umbrella, School_badge_Junior_High, School_badge_Senior_High, Dunman_dolls_pair from TD')
	orders = [dict(Total_price=row[0], A4_lecture_pad=row[1], Seven_colour_sticky_note_with_pen=row[2], A5_note_book_with_zip_bag=row[3], Pencil=row[4], Stainless_steel_tumbler=row[5], A4_clear_holder=row[6], A4_vanguard_file=row[7], Name_card_holder=row[8], Umbrella=row[9], School_badge_Junior_High=row[10], School_badge_Senior_High=row[11], Dunman_dolls_pair=row[12]) for row in cur.fetchall()]
	
	atd.close()
	return render_template('confirm.html', orders = orders)

@app.route('/add_pd', methods = ['POST'])
def add_pd():
	tc = request.form['total']
	if tc == "0.00":
		flash('You have to purchase something first!')
		return redirect(url_for('confirm'))
	else:
		current_time = datetime.datetime.now()
		totalCost = "${0:.2f}".format(float(request.form['total']))
		atd = connect_db()
		#atd.execute('DROP TABLE IF EXISTS PD')
		#atd.execute('CREATE TABLE PD(User_id TEXT, Order_date TEXT, Total_price REAL, A4_lecture_pad INT, Seven_colour_sticky_note_with_pen INT, A5_note_book_with_zip_bag INT, Pencil INT, Stainless_steel_tumbler INT, A4_clear_holder INT, A4_vanguard_file INT, Name_card_holder INT, Umbrella INT, School_badge_Junior_High INT, School_badge_Senior_High INT, Dunman_dolls_pair INT)')
		atd.execute('INSERT INTO PD(User_id, Order_date, Total_price, A4_lecture_pad, Seven_colour_sticky_note_with_pen, A5_note_book_with_zip_bag, Pencil, Stainless_steel_tumbler, A4_clear_holder, A4_vanguard_file, Name_card_holder, Umbrella, School_badge_Junior_High, School_badge_Senior_High, Dunman_dolls_pair) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',[session['logged_in'],current_time.strftime("%H:%M:%S, %a %d-%b-%Y"),totalCost, request.form['list1'], request.form['list2'], request.form['list4'], request.form['list5'], request.form['list6'], request.form['list7'], request.form['list8'], request.form['list9'], request.form['list10'], request.form['list11'], request.form['list12'], request.form['list13']])
		atd.commit()
		atd.close()
		flash('Your order has been confirmed')
		return redirect(url_for('myAccount'))

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('log'))

@app.route('/allAccounts')
@admin_required
def allAccounts():
	db = connect_db()
	cur = db.execute("SELECT * FROM PD ORDER BY User_id ASC")
	orders = [dict(User_id = row[0], Order_date = row[1], Total_price=row[2], A4_lecture_pad=row[3], Seven_colour_sticky_note_with_pen=row[4], A5_note_book_with_zip_bag=row[5], Pencil=row[6], Stainless_steel_tumbler=row[7], A4_clear_holder=row[8], A4_vanguard_file=row[9], Name_card_holder=row[10], Umbrella=row[11], School_badge_Junior_High=row[12], School_badge_Senior_High=row[13], Dunman_dolls_pair=row[14]) for row in cur.fetchall()]
	
	return render_template('console.html', orders = orders)


@app.route('/myAccount')
@login_required
def myAccount():
	db = connect_db()
	cur = db.execute("SELECT * FROM PD WHERE User_id=(?)",[session['logged_in']])
	orders = [dict(Order_date = row[1], Total_price=row[2], A4_lecture_pad=row[3], Seven_colour_sticky_note_with_pen=row[4], A5_note_book_with_zip_bag=row[5], Pencil=row[6], Stainless_steel_tumbler=row[7], A4_clear_holder=row[8], A4_vanguard_file=row[9], Name_card_holder=row[10], Umbrella=row[11], School_badge_Junior_High=row[12], School_badge_Senior_High=row[13], Dunman_dolls_pair=row[14]) for row in cur.fetchall()]
	
	return render_template('myAccount.html', orders = orders)

@app.route('/log', methods=['GET', 'POST'])
def log():
	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username == "admin" and password == "pony":
			session['logged_in'] = username
			flash('You are now logged in into the administrator account')
			return redirect(url_for('myAccount'))
		db = connect_db()
		cur = db.execute('SELECT Username, Password FROM ACCOUNTS')
		users = cur.fetchall()
		for e in users:
			if e[0]==username:
				if password != e[1]:
					error = 'Invalid password'
					break
				else:
					session['logged_in'] = username
					flash('You were logged in')
					return redirect(url_for('myAccount'))
		else:
				error = "The username you entered does not exist."
	return render_template('log.html', error = error)

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		db = connect_db()
		cur = db.execute('SELECT Username, Password FROM ACCOUNTS')
		email = request.form['username']
		emails = cur.fetchall()
		for e in emails:
			if e[0]==email:
				error = 'Email currently in use'
				break
		else:
				db.execute('INSERT INTO ACCOUNTS (Username, Password) values (?, ?)',
										[request.form['username'], request.form['password']])
				db.commit()
				flash('Successfully registered')
				session['logged_in'] = email
				return redirect(url_for('store'))
	return render_template('register.html', error = error)

if __name__ == '__main__':
  app.run(debug=True)
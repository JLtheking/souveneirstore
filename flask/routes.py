from flask import *
#from flask.ext.sendmail import Mail, Message
from functools import wraps
import sqlite3
import datetime

DB = 'DATABASE.db'

#DB = '/home/polaricicle/mysite/DATABASE.db'

app = Flask(__name__)
app.config.from_object(__name__)

mail = Mail(app)



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
@login_required
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
@login_required
def confirm():
	atd = connect_db()
	cur = atd.execute('SELECT Total_price, A4_lecture_pad, Seven_colour_sticky_note_with_pen, A5_note_book_with_zip_bag, Pencil, Stainless_steel_tumbler, A4_clear_holder, A4_vanguard_file, Name_card_holder, Umbrella, School_badge_Junior_High, School_badge_Senior_High, Dunman_dolls_pair from TD')
	orders = [dict(Total_price=row[0], A4_lecture_pad=row[1], Seven_colour_sticky_note_with_pen=row[2], A5_note_book_with_zip_bag=row[3], Pencil=row[4], Stainless_steel_tumbler=row[5], A4_clear_holder=row[6], A4_vanguard_file=row[7], Name_card_holder=row[8], Umbrella=row[9], School_badge_Junior_High=row[10], School_badge_Senior_High=row[11], Dunman_dolls_pair=row[12]) for row in cur.fetchall()]
	
	atd.close()
	return render_template('confirm.html', orders = orders)

@app.route('/add_pd', methods = ['POST'])
@login_required
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
		flash('Your order has been submitted. Please wait for us to process the order, and we will contact you through SMS to confirm your purchase and inform you after your order is available for collection.')
		return redirect(url_for('orderHistory'))



@app.route('/log', methods=['GET', 'POST'])
def log():
	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username == "admin" and password == "pony":
			session['logged_in'] = username
			flash('You are now logged in into the administrator account')
			return redirect(url_for('allAccounts'))
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
					return redirect(url_for('orderHistory'))
		else:
				error = "The username you entered does not exist."
	return render_template('log.html', error = error)

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		password = request.form['password']
		confirmPassword = request.form['confirmPassword']
				
		if password != confirmPassword:
				error = "Passwords do not match"
		else:
				db = connect_db()
				cur = db.execute('SELECT * FROM ACCOUNTS')
				username = request.form['username']
				usernames = cur.fetchall()
				for u in usernames:
					if u[0]==username:
						error = 'Username currently in use'
						break
				else:
						email = request.form['email']
						mobile_number = request.form['mobile_number']
						
						db.execute('INSERT INTO ACCOUNTS (Username, Password, Email, Mobile_number) VALUES (?, ?, ?, ?)',
												[username, password, email, mobile_number])
						db.commit()
						flash('Successfully registered')
						session['logged_in'] = username
						
						##mail user
						##for some reason could not get mail function to work from pythonanywhere. Using manual "phone SMS confirmation fallback idea"
						#msg = Message("DHS Souveneir Store - Registration Successful",
						#							sender = "leow.justin@dhs.sg",
						#							recipients = [username],
						#							html = """
						#							<h1>You have successfully registered for DHS Souveneir Store!</h1>
						#							<p>Your username is {0}</p>
						#							<p>Your password is {1}</p>
						#							""".format(username, password)
						#						)
						#mail.send(msg)
						
						return redirect(url_for('store'))
	return render_template('register.html', error = error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('log'))

@app.route('/myAccount')
@login_required
def myAccount():
	db = connect_db()
	cur = db.execute("SELECT * FROM ACCOUNTS WHERE Username=(?)",[session['logged_in']])
	info = [dict(Username = row[0], Email = row[2], Mobile_number = row[3]) for row in cur.fetchall()]
	
	return render_template('myAccount.html', error = None, info = info)

@app.route('/updateAccount', methods = ['POST'])
@login_required
def updateAccount():
	error = None
	
	db = connect_db()
	cur = db.execute("SELECT * FROM ACCOUNTS WHERE Username=(?)",[session['logged_in']])
	row = cur.fetchone()
	currentUsername = row[0]
	currentPassword = row[1]
	currentEmail = row[2]
	currentMobile_number = row[3]
	
	username = request.form['username']
	oldPassword = request.form['oldPassword']
	password = request.form['password']
	confirmPassword = request.form['confirmPassword']
	email = request.form['email']
	mobile_number = request.form['mobile_number']
	
	info = [dict(Username = username, Email = email, Mobile_number = mobile_number)]
	
	if oldPassword != "" and password != "" and confirmPassword != "":
		if oldPassword != currentPassword:
				error = 'Your password does not match with the record in the database'
		else:
				if password != confirmPassword:
						error = 'Your new passwords do not match'
				else:
						db.execute('UPDATE ACCOUNTS SET Password=(?)', [password])
						flash('Your password has been successfully changed!')
						
	if currentUsername != username:
		db.execute('UPDATE ACCOUNTS SET Username=(?)', [username])
		flash("Your username has been successfully changed from " + currentUsername + " to " + username)
		session['logged_in'] = username
	if currentEmail != email:
		db.execute('UPDATE ACCOUNTS SET Email=(?)', [email])
		flash("Your email has been successfully changed from " + currentEmail + " to " + email)
	if currentMobile_number != mobile_number:
		db.execute('UPDATE ACCOUNTS SET Mobile_number=(?)', [mobile_number])
		flash("Your mobile number has been successfully changed from " + currentMobile_number + " to " + mobile_number)
		
	db.commit()
	db.close()
	
	return render_template('myAccount.html', error = error, info = info)

@app.route('/orderHistory')
@login_required
def orderHistory():
	db = connect_db()
	cur = db.execute("SELECT * FROM PD WHERE User_id=(?)",[session['logged_in']])
	orders = [dict(Order_date = row[1], Total_price=row[2], A4_lecture_pad=row[3], Seven_colour_sticky_note_with_pen=row[4], A5_note_book_with_zip_bag=row[5], Pencil=row[6], Stainless_steel_tumbler=row[7], A4_clear_holder=row[8], A4_vanguard_file=row[9], Name_card_holder=row[10], Umbrella=row[11], School_badge_Junior_High=row[12], School_badge_Senior_High=row[13], Dunman_dolls_pair=row[14]) for row in cur.fetchall()]
	
	return render_template('orderHistory.html', orders = orders)

@app.route('/allAccounts')
@admin_required
def allAccounts():
	db = connect_db()
	cur = db.execute("SELECT * FROM ACCOUNTS ORDER BY Username ASC")
	accounts = [dict(Username = row[0], Email=row[2], Mobile_number=row[3]) for row in cur.fetchall()]
	
	return render_template('allAccounts.html', accounts = accounts)

@app.route('/allOrders')
@admin_required
def allOrders():
	db = connect_db()
	cur = db.execute("SELECT * FROM PD ORDER BY User_id ASC")
	orders = [dict(User_id = row[0], Order_date = row[1], Total_price=row[2], A4_lecture_pad=row[3], Seven_colour_sticky_note_with_pen=row[4], A5_note_book_with_zip_bag=row[5], Pencil=row[6], Stainless_steel_tumbler=row[7], A4_clear_holder=row[8], A4_vanguard_file=row[9], Name_card_holder=row[10], Umbrella=row[11], School_badge_Junior_High=row[12], School_badge_Senior_High=row[13], Dunman_dolls_pair=row[14]) for row in cur.fetchall()]
	
	return render_template('allOrders.html', orders = orders)



if __name__ == '__main__':
  app.run(debug=True)
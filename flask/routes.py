from flask import *
from functools import wraps
import sqlite3

# DATABASE = '/home/polaricicle/mysite/sales.db'

app = Flask(__name__)
# app.config.from_object(__name__)

# def connect_db():
    # return sqlite3.connect(app.config['DATABASE'])

app.secret_key = 'bleepbloopilikeponies'

from flask import *
from functools import wraps
import sqlite3

TD = 'td.db'
PD = 'pd.db'
# AD = 'ad.db'

# PD = '/home/polaricicle/mysite/pd.db'
# TD = '/home/polaricicle/mysite/td.db'
# AD = '/home/polaricicle/mysite/ad.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_pd():
    return sqlite3.connect(app.config['PD'])

def connect_td():
    return sqlite3.connect(app.config['TD'])

# def connect_ad():
    # return sqlite3.connect(app.config['ad'])

app.secret_key = 'S9621257G'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/store')
def store():
	# atd = connect_td()
	# cur = atd.execute('SELECT Order_id, User_id, Total_price, A4_lecture_pad, Seven_colour_sticky_note_with_pen, A5_ring_book, A5_note_book_with_zip_bag, Pencil, Stainless_steel_tumbler, A4_clear_holder, A4_vanguard_file, Name_card_holder, Umbrella, School_badge_Junior_High, School_badge_Senior_High, Dunman_dolls_pair from td')
	# orders = [dict(Order_id=row[0], User_id=row[1], Total_price=row[2], A4_lecture_pad=row[3], Seven_colour_sticky_note_with_pen=row[4], A5_ring_book=row[5], A5_note_book_with_zip_bag=row[6], Pencil=row[7], Stainless_steel_tumbler=row[8], A4_clear_holder=row[9], A4_vanguard_file=row[10], Name_card_holder=row[11], Umbrella=row[12], School_badge_Junior_High=row[13], School_badge_Senior_High=row[14], Dunman_dolls_pair=row[15]) for row in cur.fetchall()]
	return render_template('store.html')

@app.route('/add_td', methods = ['POST'])	
def add_td():
	atd = connect_td()
	# cur = atd.execute('SELECT Order_id, User_id, Total_price, A4_lecture_pad, Seven_colour_sticky_note_with_pen, A5_ring_book, A5_note_book_with_zip_bag, Pencil, Stainless_steel_tumbler, A4_clear_holder, A4_vanguard_file, Name_card_holder, Umbrella, School_badge_Junior_High, School_badge_Senior_High, Dunman_dolls_pair from td')
	# orders = [dict(Order_id=row[0], User_id=row[1], Total_price=row[2], A4_lecture_pad=row[3], Seven_colour_sticky_note_with_pen=row[4], A5_ring_book=row[5], A5_note_book_with_zip_bag=row[6], Pencil=row[7], Stainless_steel_tumbler=row[8], A4_clear_holder=row[9], A4_vanguard_file=row[10], Name_card_holder=row[11], Umbrella=row[12], School_badge_Junior_High=row[13], School_badge_Senior_High=row[14], Dunman_dolls_pair=row[15]) for row in cur.fetchall()]
	atd.execute('INSERT INTO TD (User_id, Total_price, A4_lecture_pad, Seven_colour_sticky_note_with_pen, A5_note_book_with_zip_bag, Pencil, Stainless_steel_tumbler, A4_clear_holder, A4_vanguard_file, Name_card_holder, Umbrella, School_badge_Junior_High, School_badge_Senior_High, Dunman_dolls_pair) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',["Guest", request.form['total'], request.form['list1'], request.form['list2'], request.form['list4'], request.form['list5'], request.form['list6'], request.form['list7'], request.form['list8'], request.form['list9'], request.form['list10'], request.form['list11'], request.form['list12'], request.form['list13']])
	atd.commit()
	atd.close()
	return redirect(url_for('confirm'))

@app.route('/delete/<int:Order_id>',)
def delete_Order_id(Order_id):
	atd = connect_td()
	cur = atd.execute('delete from TD where Order_id='+str(Order_id))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:Total_price>',)
def delete_Total_price(Total_price):
	atd = connect_td()
	cur = atd.execute('delete from TD where Total_price='+str(Total_price))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:A4_lecture_pad>',)
def delete_A4_lecture_pad(A4_lecture_pad):
	atd = connect_td()
	cur = atd.execute('delete from TD where A4_lecture_pad='+str(A4_lecture_pad))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:Seven_colour_sticky_note_with_pen>',)
def delete_Seven_colour_sticky_note_with_pen(Seven_colour_sticky_note_with_pen):
	atd = connect_td()
	cur = atd.execute('delete from TD where Seven_colour_sticky_note_with_pen='+str(Seven_colour_sticky_note_with_pen))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:A5_ring_book>',)
def delete_A5_ring_book(A5_ring_book):
	atd = connect_td()
	cur = atd.execute('delete from TD where A5_ring_book='+str(A5_ring_book))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:A5_note_book_with_zip_bag>',)
def delete_A5_note_book_with_zip_bag(A5_note_book_with_zip_bag):
	atd = connect_td()
	cur = atd.execute('delete from TD where A5_note_book_with_zip_bag='+str(A5_note_book_with_zip_bag))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:Pencil>',)
def delete_Pencil(Pencil):
	atd = connect_td()
	cur = atd.execute('delete from TD where Pencil='+str(Pencil))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:Stainless_steel_tumbler>',)
def delete_Stainless_steel_tumbler(Stainless_steel_tumbler):
	atd = connect_td()
	cur = atd.execute('delete from TD where Stainless_steel_tumbler='+str(Stainless_steel_tumbler))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:A4_clear_holder>',)
def delete_A4_clear_holder(A4_clear_holder):
	atd = connect_td()
	cur = atd.execute('delete from TD where A4_clear_holder='+str(A4_clear_holder))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:A4_vanguard_file>',)
def delete_A4_vanguard_file(A4_vanguard_file):
	atd = connect_td()
	cur = atd.execute('delete from TD where A4_vanguard_file='+str(A4_vanguard_file))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:Name_card_holder>',)
def delete_Name_card_holder(Name_card_holder):
	atd = connect_td()
	cur = atd.execute('delete from TD where Name_card_holder='+str(Name_card_holder))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:Umbrella>',)
def delete_Umbrella(Umbrella):
	atd = connect_td()
	cur = atd.execute('delete from TD where Umbrella='+str(Umbrella))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:School_badge_Junior_High>',)
def delete_School_badge_Junior_High(School_badge_Junior_High):
	atd = connect_td()
	cur = atd.execute('delete from TD where School_badge_Junior_High='+str(School_badge_Junior_High))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:School_badge_Senior_High>',)
def delete_School_badge_Senior_High(School_badge_Senior_High):
	atd = connect_td()
	cur = atd.execute('delete from TD where School_badge_Senior_High='+str(School_badge_Senior_High))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/delete/<int:Dunman_dolls_pair>',)
def delete_Dunman_dolls_pair(Dunman_dolls_pair):
	atd = connect_td()
	cur = atd.execute('delete from TD where Dunman_dolls_pair='+str(Dunman_dolls_pair))
	atd.commit()
	atd.close()
	flash('Your order was deleted')
	return redirect(url_for('confirm'))

@app.route('/confirm')
def confirm():
	atd = connect_td()
	cur = atd.execute('SELECT Order_id, User_id, Total_price, A4_lecture_pad, Seven_colour_sticky_note_with_pen, A5_note_book_with_zip_bag, Pencil, Stainless_steel_tumbler, A4_clear_holder, A4_vanguard_file, Name_card_holder, Umbrella, School_badge_Junior_High, School_badge_Senior_High, Dunman_dolls_pair from TD')
	orders = [dict(Order_id=row[0], User_id=row[1], Total_price=row[2], A4_lecture_pad=row[3], Seven_colour_sticky_note_with_pen=row[4], A5_note_book_with_zip_bag=row[5], Pencil=row[6], Stainless_steel_tumbler=row[7], A4_clear_holder=row[8], A4_vanguard_file=row[9], Name_card_holder=row[10], Umbrella=row[11], School_badge_Junior_High=row[12], School_badge_Senior_High=row[13], Dunman_dolls_pair=row[14]) for row in cur.fetchall()]
	atd.close()
	return render_template('confirm.html', orders = orders)

@app.route('/add_pd', methods = ['GET', 'POST'])
def add_pd():
	apd = connect_pd()
	atd = connect_td()
	aaa = atd.execute('SELECT Order_id, User_id, Total_price, A4_lecture_pad, Seven_colour_sticky_note_with_pen, A5_note_book_with_zip_bag, Pencil, Stainless_steel_tumbler, A4_clear_holder, A4_vanguard_file, Name_card_holder, Umbrella, School_badge_Junior_High, School_badge_Senior_High, Dunman_dolls_pair from TD')
	apd.execute('INSERT INTO PD(Order_id, User_id, Total_price, A4_lecture_pad, Seven_colour_sticky_note_with_pen, A5_note_book_with_zip_bag, Pencil, Stainless_steel_tumbler, A4_clear_holder, A4_vanguard_file, Name_card_holder, Umbrella, School_badge_Junior_High, School_badge_Senior_High, Dunman_dolls_pair) SELECT * FROM TD')
	apd.commit()
	apd.close()
	atd.execute('DROP TABLE')
	atd.close()
	flash('Your order has been confirmed')
	return redirect(url_for('store'))

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
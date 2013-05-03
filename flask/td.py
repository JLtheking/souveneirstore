import sqlite3 as lite
import sys

con = lite.connect('td.db')

with con:

				cur = con.cursor()
				
				cur.execute("DROP TABLE IF EXISTS TD")
				cur.execute("CREATE TABLE TD(Order_id INTEGER PRIMARY KEY AUTOINCREMENT, User_id TEXT, Total_price MONEY, A4_lecture_pad TEXT, Seven_colour_sticky_note_with_pen TEXT, A5_note_book_with_zip_bag TEXT, Pencil TEXT, Stainless_steel_tumbler TEXT, A4_clear_holder TEXT, A4_vanguard_file TEXT, Name_card_holder TEXT, Umbrella TEXT, School_badge_Junior_High TEXT, School_badge_Senior_High TEXT, Dunman_dolls_pair TEXT)")

con.close()

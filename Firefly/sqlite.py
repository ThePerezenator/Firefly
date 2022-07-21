import sqlite3
import os
from sqlite3 import Error
import shutil
import time
from datetime import datetime


conn = sqlite3.connect('master.db', check_same_thread=False)
c = conn.cursor()

def create_database(setlist):
	setlist = f"{setlist}" 
	try:
		os.chdir("/home/perez/Desktop/Python Projects/Firefly/Setlists")
		conn = sqlite3.connect(f"{setlist}")
		c = conn.cursor()
		c.execute(f'CREATE TABLE IF NOT EXISTS {setlist}(song Text)')
		print(f"{setlist} CREATED")
	except Error as e:
		print(e)
	finally:
		if conn:
			conn.close()

def open(setlist):
	try:
		os.chdir("/home/perez/Desktop/Python Projects/Firefly/Setlists")
		setlist = str(setlist)[2:-2]
		print(f"opening {setlist}")
		conn = sqlite3.connect(setlist)
		c = conn.cursor()
		c.execute(f"SELECT * from {setlist} ORDER BY song COLLATE NOCASE ASC")
		return(c.fetchall())
	except Error as e:
		print(e)
	finally:
		if conn:
			conn.close()

def add_song(setlist, song):
	try:
		os.chdir("/home/perez/Desktop/Python Projects/Firefly/Setlists")
		conn = sqlite3.connect(f"/home/perez/Desktop/Python Projects/Firefly/Setlists/{setlist}")
		print(f"Setlist: {setlist} Song: {song}")
		c = conn.cursor()
		c.execute(f"INSERT INTO {setlist} (song) VALUES (?)",
		(song, ))
		conn.commit()
	except Error as e:
		print(e)
	finally:
		if conn:
			conn.close()
		
def remove_song(setlist, song):
	try:
		os.chdir("/home/perez/Desktop/Python Projects/Firefly/Setlists")
		conn = sqlite3.connect(f"/home/perez/Desktop/Python Projects/Firefly/Setlists/{setlist}")
		print(f"Setlist: {setlist} Song: {song}")
		c = conn.cursor()
		c.execute(f"DELETE from {setlist} WHERE song = '{song}'")
		conn.commit()
	except Error as e:
		print(e)
	finally:
		if conn:
			conn.close()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS requests(song Text, name TEXT, status TEXT, unix TEXT)')
	c.execute('CREATE TABLE IF NOT EXISTS standard(song TEXT, status TEXT)')

def refresh_requests():
	c.execute("SELECT * FROM requests")
	return(c.fetchall())

def refresh_standard():
	c.execute("SELECT * FROM standard ORDER BY song COLLATE NOCASE ASC")
	return(c.fetchall())

def refresh_standard_tags():
	c.execute("SELECT FROM standard WHERE tags ")
	return(c.fetchall())
def new_request(name, song):
	unix = datetime.now().strftime("%H:%M:%S")
	name = name
	song = f"‍{song}" #zero width joiner https://emojipedia.org/zero-width-joiner/
	status = 'Requested'
	c.execute("INSERT INTO requests (song, name, status, unix) VALUES (?, ?, ?, ?)",
	(song, name, status, unix))
	conn.commit()

def new_standard(song):
	song = f"‍{song}" #zero width joiner https://emojipedia.org/zero-width-joiner/
	status = 'Not played'
	c.execute("INSERT INTO standard (song, status) VALUES (?, ?)",
	(song, status))
	conn.commit()

def play_song(nowplaying):
	c.execute("UPDATE standard SET status = 'Played' WHERE rowid = 2")
	print(f"attempting {nowplaying}")
	conn.commit()

def check_request(name, song):
	c.execute("SELECT * FROM requests WHERE song=:song", {'song': song})
	if None in c.fetchall():
		return "Database error"
	else:
		return "Check"

def video_text_update():
	c.execute("SELECT song FROM requests")
	songs = c.fetchmany(4)
	c.execute("SELECT name FROM requests")
	names = c.fetchmany(4)
	return (tup(songs, names))

def song_row_delete(song):
	try:
		c.execute(f"DELETE from standard WHERE Song='‍{song}'") #SWITCH STANDARD TO REQUESTS WHEN DEPLYED
		conn.commit()
		print(f"DELETED {song} FROM DATABASE")
	except:
		print(f"{song} DOES NOT EXIST | UNABLE TO DELETE FROM DATABASE")

# Using map() and lambda
def tup(l1, l2):
    return list(map(lambda x, y:(x,y), l1, l2))


create_table()

















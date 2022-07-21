import sqlite3
import os
from sqlite3 import Error
import shutil
import time
from datetime import datetime

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


remove_song("testing", "song1")
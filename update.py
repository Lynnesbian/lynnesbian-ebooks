#!/usr/bin/env python3
import os, sqlite3
files = ['toots.db']
for f in files:
	print(f)
	db = sqlite3.connect("{}".format(f))
	c = db.cursor()
	toots = c.execute("SELECT * FROM `toots`").fetchall()
	for toot in toots:
		c.execute("REPLACE INTO toots (id, userid, content) VALUES (?, ?, ?)", (toot[0], toot[1], toot[2].replace("\0", "\n")))
	db.commit()
	db.execute("VACUUM") #compact db
	db.commit()
	db.close()

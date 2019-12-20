#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mastodon import Mastodon
from os import path
from bs4 import BeautifulSoup
import shutil, os, sqlite3, signal, sys, json
# import re

scopes = ["read:statuses", "read:accounts", "read:follows", "write:statuses"]
cfg = json.load(open('config.json', 'r'))


def get_toots(client, id, since_id):
	i = 0
	toots = client.account_statuses(id, since_id = since_id)
	while toots is not None and len(toots) > 0:
		for toot in toots:
			t = parse_toot(toot)
			if t != None:
				yield {
					"content": t,
					"id": toot.id
				}
		try:
			toots = client.fetch_next(toots)
		except TimeoutError:
			print("Operation timed out, committing to database and exiting.")
			db.commit()
			db.close()
			sys.exit(1)
		i += 1
		if i%10 == 0:
			print(i)

client = Mastodon(
		client_id="clientcred.secret", 
		access_token="usercred.secret", 
		api_base_url=cfg['site'])

me = client.account_verify_credentials()
following = client.account_following(me.id)

db = sqlite3.connect("toots.db")
db.text_factory=str
c = db.cursor()

def handleCtrlC(signal, frame):
	print("\nPREMATURE EVACUATION - Saving chunks")
	db.commit()
	sys.exit(1)

signal.signal(signal.SIGINT, handleCtrlC)

c.execute("ALTER TABLE toots RENAME TO toots_old")
c.execute("CREATE TABLE toots (id INTEGER, userid INTEGER, uri TEXT, content TEXT)")
c.execute("INSERT INTO toots (id, userid, content) SELECT id, userid, content FROM toots_old")
c.execute("DROP TABLE toots_old")

db.commit()
db.execute("VACUUM") #compact db
db.commit()
db.close()
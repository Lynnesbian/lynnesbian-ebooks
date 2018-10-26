#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import mastodon
import os, random, re, json
import create
from bs4 import BeautifulSoup

cfg = json.load(open('config.json', 'r'))
client = mastodon.Mastodon(
        client_id=cfg['client']['id'],
        client_secret=cfg['client']['secret'], 
        access_token="usercred.secret", 
        api_base_url=cfg['site'])

def extract_toot(toot):
	#copied from main.py, see there for comments
	soup = BeautifulSoup(toot, "html.parser")
	for lb in soup.select("br"):
		lb.insert_after("\n")
		lb.decompose()
	for p in soup.select("p"):
		p.insert_after("\n")
		p.unwrap()
	for ht in soup.select("a.hashtag"):
		ht.unwrap()
	for link in soup.select("a"):
		link.insert_after(link["href"])
		link.decompose()
	text = map(lambda a: a.strip(), soup.get_text().strip().split("\n"))
	text = "\n".join(list(text))
	text = re.sub("https?://([^/]+)/(@[^ ]+)", r"\2@\1", text) #put mentions back in
	text = re.sub("^(@[^@]+@[^ ]+ *)+", r"", text) #...but remove the initial ones
	text = text.lower() #for easier matching
	return text

class ReplyListener(mastodon.StreamListener):
	def on_notification(self, notification):
		if notification['type'] == 'mention':
			acct = "@" + notification['account']['acct']
			post_id = notification['status']['id']
			mention = extract_toot(notification['status']['content'])
			toot = create.make_toot(True)['toot']
			# compat = re.match("^compatibility check: (@[^@]+@[^ ]+) (?:and|&) (@[^@]+@[^ ]+)", mention)
			talk_about = re.match("^ *(?:talk|tell me|post|toot) about (.*)\\.*", mention)
			print(acct + " says " + mention)
			#special functions
			if mention.startswith("yes or no:"):
				replies = ["yes", "nope", "no", "definitely!", "of course!", "no way.",
				"um, i don't actually know!", "i mean, i guess...", "sure!", "nah.",
				"maybe.", "i think you know the answer.", "yeah it's not looking good.",
				"probably.", "sure!", "heck no!"]
				toot = random.choice(replies)
			elif mention.startswith("override: "):
				#mistress wants direct control <3
				if acct not in ["@lynnesbian@deadinsi.de", "@00dani@vulpine.club", "@lynnesbian@fedi.lynnesbian.space"]:
					toot = "Insufficient privileges. This action has been reported to @lynnesbian@fedi.lynnesbian.space."
				else:
					command = mention[len("override: "):]
					swaps = {
						"you": "i",
						"yours": "mine",
						"your": "my",
						"you're": "i'm",
					}
					gross_hack = "///DON'T_USE_THIS_PHRASE_IN_A_TOOT///"
					command = re.sub("\\bme\\b", "i", command)
					for one, two in swaps.items():
						command = re.sub("\\b{}\\b".format(one), gross_hack, command)
						command = re.sub("\\b{}\\b".format(two), one, command)
						command = re.sub(gross_hack, two, command)

					toot = command
			elif "apologise" in mention:
				apologies = ["please forgive me!", "i'm so sorry!", "sorry!",
				"my mistake!", "i'm always trying to do better!",
				"i'm sorry, i didn't mean it!", "sorry...", "oh, sorry..."]
				if acct == "@lynnesbian@fedi.lynnesbian.space":
					apologies = ["f-forgive me, mistress!",
					"i'm so sorry, mistress!", "mistress lynne! i'm so sorry for this!",
					"i'm so sorry... y-you can punish me if you want...",
					"am i going to get punished for this? 0////0",
					"i've been a naughty bot... do i need punishment?",
					"lynne, i am not worthy of your love!",
					"mistress lynne, i cannot express my regret... how can i make this up to you?",
					"from the bottom of my heart, i apologise, mistress!",
					"no, no, no! how could i have let this happen in front of mistress?!",
					"m-maybe you'll have to punish me..."]
				toot = random.choice(apologies)
			elif re.match(r"^\s*fortune\s*$", mention) != None:
				fortunes = ["not looking good.", "things are gonna go well!",
				"you're gonna have a great day!", "terrible day ahead. do NOT go outside.",
				"it's a good day to be gay!", "um... good luck! 0u0;",
				"honestly you're kinda fucked for today", "don't accept the offer.",
				"that thing you've always wanted to do? go for it.",
				"i don't know, i'm just a bot :L", "hmm... what? i was thinking about girls...",
				"make the best of a bad situation.", "this is going to be a great day!",
				"when god closes a door, she opens a window~", "i mean i've seen worse?"]
				toot = random.choice(fortunes)
			# elif compat != None:
				# toot = "{} and {} are {}% compatible.".format(compat.group(1), compat.group(2), random.randint(0,100))
				# toot = "Feature disabled"
			elif talk_about != None:
				#toot = create.make_toot_markov(talk_about.group(1))['toot']
				pass #broken, disabled
			toot = acct + " " + toot
			if acct == "@lynnesbian@fedi.lynnesbian.space":
				prefixes = ["h-hello, mistress...", "hi lynne!",
				"(omg, mistress is talking to me!)", "m-mistress!", "lynne!",
				"hello, my favourite lesbian!", "hey lynne~", "o-oh, hi lynne!"]
				if random.randint(1,15) == 3:
					toot = random.choice(prefixes) + " " + toot
			if acct == "@lynnesbian@fedi.lynnesbian.space":
				if random.randint(1,1000) == 666:
					toot = "@lynnesbian@fedi.lynnesbian.space" +  ("i love you " * random.randint(10, 20))
			client.status_post(toot, post_id, visibility=notification['status']['visibility'])

rl = ReplyListener()
client.stream_user(rl)

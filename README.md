# lynnesbian-ebooks

# DON'T USE THIS CODE. USE [THIS CODE](https://github.com/Lynnesbian/mstdn-ebooks) INSTEAD. DO NOT USE THIS CODE!!!

This version makes quite a few changes from [the original](https://github.com/Jess3Jane/mastodon-ebooks), such as:
- Unicode support
- Non-Markov stuff
- Meme generation with ImageMagick
- Stores toots in a sqlite database rather than a text file
  - Doesn't unecessarily redownload all toots every time
- its very cute

## Install/usage guide
If you really, really want to install this, rather than mstdn-ebooks, you can follow [this guide](https://cloud.lynnesbian.space/s/jozbRi69t4TpD95) and make changes where appropriate. However, I strongly recommend against this.

## Original README
hey look it's an ebooks bot

python3

install the requirements with `sudo pip3 install -r requirements.txt`

make a bot (probably on bots in space) and follow the target accounts

run `python3 main.py` to login and scrape

run `python3 gen.py` to make a toot

cron is an okay choice to make it toot regularly

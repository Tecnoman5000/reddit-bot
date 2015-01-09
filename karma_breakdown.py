__author__ = 'Tecnoman5000'

import praw
import pprint
from sys import exit

def get_user_karam(user_name):

	"""
	Connect to Reddit
	"""
	print('Connecting...')
	r = praw.Reddit(user_agent='The bot to hoard it all') # Bot information
	try:
		user = r.get_redditor(user_name) # Get reddit user information
	except Exception as http_err:
		print(http_err)
		exit(0)

	"""
	Pull Information from Reddit
	"""
	print('Gathering Information...')
	thing_limit = 10 # Limit the number of items to retrieve
	gen = user.get_submitted(limit=thing_limit) # Connection to Reddit and hold information returned

	"""
	Sort Information
	"""
	print('Sorting Information...')
	karma_by_subreddit = {}
	for thing in gen:
		subreddit = thing.subreddit.display_name # Get subreddit name that the user's post is in, held by 'thing'
		karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) + thing.score)  # add post karam by subreddit to dict

	pprint.pprint(karma_by_subreddit)

get_user_karam(str(input('Get karma for user: ')))
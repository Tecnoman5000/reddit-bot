__author__ = 'tecnoman5000'

import praw
from sys import meta_path

def voting_main(user_name):

	if user_name == '':
		print('Input was null, reverting to default! (tecnoman)')
		user_name = 'tecnoman'

	### Connect to Reddit
	print('Connecting...')
	r = praw.Reddit(user_agent='The bot to hoard it all')
	r.login('datahoardingbot', 'fuckYouC0g3c0')

	try:
		reddit_user = r.get_redditor(user_name) # Get reddit user information
	except Exception as http_err:
		print(http_err)
		exit(0)

	### Get Submission
	print('Pulling Information...')
	user_submits = reddit_user.get_submitted() # Connection to Reddit and hold information returned

	for thing in user_submits:
		submission = r.get_submission(submission_id=thing.id)

		## Interact with Submission
		print('Up Voting...')
		submission.upvote()

voting_main(str(input('Username to upvote: ')))
__author__ = 'tecnoman5000'

import praw
from sys import meta_path

def voting_main(user_name):

	if user_name == '':
		print('Input was null, reverting to default! (tecnoman)')
		user_name = 'tecnoman'

	post_id = []

	### Open post_id_'user_name' file and read in already voted ids
	try:
		with open('post_id_'+user_name, 'r') as post_id_file:
			print('Previously up voted IDs found')
			for line in post_id_file.read().splitlines():
				post_id.append(line)
	except FileNotFoundError as no_file_err:
		print('No previously up voted IDs found')

	### Connect to Reddit
	print('Connecting...')
	r = praw.Reddit(user_agent='The bot to hoard it all') # Bot information
	r.login('datahoardingbot', 'fuckYouC0g3c0') # bot login information

	try:
		reddit_user = r.get_redditor(user_name) # Get reddit user information
	except Exception as http_err: # If the username returns 404
		print(http_err)
		exit(0)

	### Get Submission
	print('Pulling Information...')
	user_submits = reddit_user.get_submitted() # Connection to Reddit and hold information returned

	print('Checking posts...')
	for thing in user_submits:
		if not any(thing.id in ids for ids in post_id): # Check to see if the id was previously up voted
			## Interact with Submission
			submission = r.get_submission(submission_id=thing.id)
			print('Up Voting...')
			submission.upvote()
			with open('post_id_'+user_name, 'a') as post_id_file: # Append to the bottom of the file the new post id
				post_id_file.write(thing.id+'\n')
		else:
			print('Post Already Up Voted, ID: ', thing.id)


voting_main(str(input('Username to up vote: ')))
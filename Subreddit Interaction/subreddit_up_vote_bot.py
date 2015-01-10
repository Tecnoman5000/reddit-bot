__author__ = 'tecnoman5000'

import praw
from time import sleep
from os import name, system
import warnings

def subreddit_up_vote(input_subreddit_name,bot_pass,category):
	for subreddit_name in input_subreddit_name:
		post_id = []

		### Open post_id_'subreddit_name' file and read in already voted ids
		try:
			with open('post_id_'+subreddit_name, 'r') as post_id_file:
				print('Previously up voted IDs found')
				for line in post_id_file.read().splitlines():
					post_id.append(line)
		except FileNotFoundError:
			print('No previously up voted IDs found')

		### Connect to Reddit
		print('Connecting...')
		r = praw.Reddit(user_agent='The bot to hoard it all') # Bot information
		r.login('datahoardingbot',bot_pass) # bot login information

		try:
			subreddit = r.get_subreddit(subreddit_name) # Get subreddit information
		except Exception as http_err: # If the username returns 404
			print(http_err)
			exit(0)

		### Get Submission
		print('Pulling Information...')
		if category == 'hot':
			subreddit_posts = subreddit.get_hot(limit=100) # Connection to Reddit and hold information returned
		elif category == 'top':
			subreddit_posts = subreddit.get_top(limit=100) # Connection to Reddit and hold information returned
		else:
			subreddit_posts = subreddit.get_new(limit=100) # Connection to Reddit and hold information returned

		print('Checking posts new posts in',subreddit_name,'...')

		post_num = 0
		for post in subreddit_posts:
			print_out = str(post_num) + '%'
			print(print_out, end='') # just print and flush
			if not any(post.id in ids for ids in post_id): # Check to see if the id was previously up voted
				## Interact with Submission
				submission = r.get_submission(submission_id=post.id)
				#print('Up Voting... ID: ', post.id)

				submission.upvote()
				with open('post_id_'+subreddit_name, 'a') as post_id_file: # Append to the bottom of the file the new post id
					post_id_file.write(post.id+'\n')
			sleep(0.01)
			print('\r' * len(print_out), end='') # use '\r' to go back
			post_num += 1
		print(subreddit_name,' Up Voting Finished!')
	print(' Up Voting Finished!')



def voting_main():
	user_input = [str(input('Subreddit to up vote: '))]
	if user_input[0] == '':
		print('Input was null, reverting to default! (default_subreddits file)')
		print('Edit "default_subreddits" to up vote new posts on multi subreddits')
		user_input.remove('')
		with open('default_subreddits', 'r') as default_subreddits:
			for line in default_subreddits.read().splitlines():
				user_input.append(line)
			default_subreddits.close()

	cat = str(input('Choose Categories for up voting (hot;new;top): '))
	input_password =  str(input('Data Hoarding Bot password: '))
	if str(input('Do you want recursive mode? (y/n)')) == 'y':
		while 0 < 1:
			subreddit_up_vote(user_input,input_password,cat)
			print('Waiting 1 minute till next check...')
			sleep(60)
			system('cls' if name == 'nt' else 'clear')  # Clear screen before use
	else:
		subreddit_up_vote(user_input,input_password,cat)

voting_main()

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings(): # To fix the sys / resource warnings
	warnings.simplefilter("ignore")
	fxn()
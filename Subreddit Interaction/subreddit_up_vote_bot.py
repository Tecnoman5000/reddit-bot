__author__ = 'tecnoman5000'

import praw
from time import sleep
from os import name, system

def voting_main(subreddit_name,bot_pass):
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
	print('Up Voting Finished!')

user_input = str(input('Subreddit to up vote: '))
if user_input == '':
	print('Input was null, reverting to default! (pcmasterrace)')
	user_input = 'pcmasterrace'

input_password =  str(input('Data Hoarding Bot password: '))
if str(input('Do you want recursive mode? (y/n)')) == 'y':
	while 0 < 1:
		voting_main(user_input,input_password)
		print('Waiting 1 minute till next check...')
		sleep(60)
		system('cls' if name == 'nt' else 'clear')  # Clear screen before use
else:
	voting_main(user_input,input_password)
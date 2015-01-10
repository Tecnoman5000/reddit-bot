__author__ = 'Tecnoman5000'

import praw
from time import sleep
from os import name, system
import warnings
import unicodedata
import string
valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

def tifu_arch_main(bot_pass):
	post_id = []

	### Open post_id_'subreddit_name' file and read in already voted ids
	try:
		with open('post_id_tifu_arch', 'r') as post_id_file:
			print('Previously up voted IDs found')
			for line in post_id_file.read().splitlines():
				post_id.append(line)
		post_id_file.close()
	except FileNotFoundError:
		print('No previously archived IDs found')

	### Connect to Reddit
	print('Connecting...')
	r = praw.Reddit(user_agent='The bot to hoard it all') # Bot information
	r.login('datahoardingbot',bot_pass) # bot login information

	try:
		sub_tifu = r.get_subreddit('tifu') # Get subreddit information
	except Exception as http_err: # If the username returns 404
		print(http_err)
		exit(0)

	tifu_posts = sub_tifu.get_hot(limit=100) # Connection to Reddit and hold information returned

	print('Checking posts new posts in TIFU...')
	post_num = 0
	for post in tifu_posts:
		print_out = str(post_num) + '%'
		print(print_out, end='') # just print and flush
		if not any(post.id in ids for ids in post_id): # Check to see if the id was previously up voted
			## Interact with Submission
			submission = r.get_submission(submission_id=post.id)
			if submission.title[:4] != 'TIFU':
				print('Skipping TIFU Post ',post.id,', Bad Title')
			else:
				with open('tifu_archived_posts/'+remove_disallowed_filename_chars(submission.title+'.txt'), 'w+') as tifu_post_file:
					tifu_post_file.write(submission.selftext)
				tifu_post_file.close()
				with open('post_id_tifu_arch', 'a') as post_id_file: # Append to the bottom of the file the new post id
					post_id_file.write(post.id+'\n')
		sleep(0.01)
		print('\r' * len(print_out), end='') # use '\r' to go back
		post_num += 1

	print('All new Hot TIFU posts archived!')



def remove_disallowed_filename_chars(file_name):
	valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	return ''.join(c for c in file_name if c in valid_chars)

def __init__():
	input_password =  str(input('Data Hoarding Bot password: '))
	if str(input('Do you want recursive mode? (y/n)')) == 'y':
		while 0 < 1:
			tifu_arch_main(input_password)
			print('Waiting 1 minute till next check...')
			sleep(60)
			system('cls' if name == 'nt' else 'clear')  # Clear screen before use
	else:
		tifu_arch_main(input_password)

__init__()

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings(): # To fix the sys / resource warnings
	warnings.simplefilter("ignore")
	fxn()

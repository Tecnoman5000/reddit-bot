__author__ = 'tecnologic'

import praw
from time import sleep, time, localtime
import datetime
from os import name, system
from sys import stdin
import urllib3
import imghdr
import warnings
import getpass
# warnings.filterwarnings("ignore")  # Ignore all warnings
warnings.simplefilter('ignore', ResourceWarning)  # Ignore resource warnings


def main(bot_pass):
    img_dl = 0
    post_id = []

    ''' Open post_id_'subreddit_name' file and read in already voted ids '''

    try:
        with open('post_id_archive', 'r') as post_id_file:
            print('Previously up voted IDs found')
            for line in post_id_file.read().splitlines():
                post_id.append(line)
        post_id_file.close()
    except FileNotFoundError:
        print('No previously archived IDs found')

    ''' Connect to Reddit '''
    print('Connecting...')
    r = praw.Reddit(user_agent="The scripts to hoard it all")  # Bot information
    # while True:
    try:
        r.login('datahoardingbot', bot_pass)  # bot login information
    # break
    except Exception as login_err:
        print(login_err)
    # continue

    try:
        subreddit = r.get_subreddit('wallpapers')  # Get subreddit information
    except Exception as http_err:  # If the subreddit returns 404
        print(http_err)
        exit(0)
    grab_limit = 200
    subreddit_posts = subreddit.get_new(limit=grab_limit)  # Pull post information

    print('Checking for new wallpaper posts...')
    post_num = 0
    http = urllib3.PoolManager()
    for submission in subreddit_posts:
        # print(str(post_num), '%', end='')  # just print and flush
        if not any(submission.id in ids for ids in post_id):  # Check to see if the id was previously up voted
            # Interact with Submission
            single_submission = r.get_submission(submission_id=submission.id)
            print(post_num + 1, '/', grab_limit, ' :', single_submission.title, sep='')
            # print(single_submission.url)
            url = link_format(single_submission.url)  # Grab submission link url
            if url == 'bad':
                with open('post_id_archive', 'a') as post_id_file:  # Append to the bottom of the file the new post id
                    post_id_file.write(submission.id + '\n')
                with open('bad_links', 'a') as bad_links_file:  # Append to the bottom of the file the new post id
                    bad_links_file.write(single_submission.title + ': ' + single_submission.url + '\n')
                print('')
                post_num += 1
                continue

            imgur_id = get_id(url)
            url = 'https://imgur.com/download/' + imgur_id
            print('URL: ', url)
            image = http.request('GET', url)
            img_ext = imghdr.what(imgur_id, image.data)
            if img_ext is None:
                img_ext = 'jpg'
            print('Ext: ', img_ext)

            image_name = name_format(single_submission.title, imgur_id, img_ext)
            with open('/home/tecno/Scripts/reddit-bot/Subreddit Interaction/wallpaper_scraper/saved/' + image_name,
                      'wb') as out:
                data = image.data
                out.write(data)
                img_dl += 1
            out.close()  # Close image file
            # image.headers['connection:close']

            with open('post_id_archive', 'a') as post_id_file:  # Append to the bottom of the file the new post id
                post_id_file.write(submission.id + '\n')

            print('')
        else:
            print(post_num + 1, '/', grab_limit, ': Post already downloaded! \r', end='', sep='')
            sleep(0.1)
        post_num += 1
    return img_dl


def name_format(title, imgur_id, extension):
    for ch in ['(', '{']:
        if ch in title:
            title = title.replace(ch, '[')
    for ch in [')', '}']:
        if ch in title:
            title = title.replace(ch, ']')
    title = title.replace('[OC]', '_OC_')

    res_start = ''
    res_finish = ''
    res = ''

    if title.find('[') != -1:
        res_start = title.find('[')
    elif title.find('(') != -1:
        res_start = title.find('(')
    if title.find(']') != -1:
        res_finish = title.find(']')
    elif title.find(')') != -1:
        res_finish = title.find(')')
    if res_start != '' and res_finish != '':
        res = title[res_start:res_finish + 1]
        title = title[:res_start]
        title = title.strip()
        title = title.replace(" ", "_")

    if len(title) <= 15:
        img_title = title
    else:
        img_title = imgur_id

    if res != '' and (res.find('x') != -1 or res.find('X') != -1 or res.find('×') != -1) and len(res) <= 12:
        img_name = img_title + ' ' + res + '.' + extension
    else:
        img_name = img_title + '.' + extension
    print('Name: ', img_name)
    return img_name


def link_format(url):
    url_pass = False
    imgur_id = ''
    if url.find('http://imgur.com/r/wallpaper/') != -1:  # if url in subreddit imgur format
        imgur_id = url[29:]
        url = 'http://i.imgur.com/' + imgur_id + '.jpg'  # Turn imgur link into image url
        url_pass = True
        # print(url)
    elif url.find('/a/') != -1:  # if url in imgur album format
        url_pass = False
        if url.find('#') != -1:
            imgur_id = url[url.find('/a/') + 3:url.find('#')]
        else:
            imgur_id = url[19:]
        print('Album Link Found, id: ', imgur_id)
        with open('albums', 'a') as albums_id_file:  # Append to the bottom of the file the new post id
            albums_id_file.write(imgur_id + '\n')
    elif url.find('http://i.imgur.com/') != -1:  # if url in imgur image format
        url_pass = True
        # print('Download Link Found: ', url)
    elif url.find('http://imgur.com/') != -1 and len(url) == 24:  # if url in imgur single id format
        imgur_id = url[17:]
        url = 'http://i.imgur.com/' + imgur_id + '.jpg'
        url_pass = True
        # print(url)
    elif url.find('/gallery/') != -1:
        print('Gallery Link Found, id: ', url[25:])
        url_pass = False
    else:  # if url does not fit any formatting rules
        print('non-standard url Found: ', url)
        url_pass = False
    if len(url) == 30 and url_pass:
        return url
    else:
        print('Bad Link: ', url)
        return 'bad'


def get_id(url):
    url = url[:len(url) - 4]
    imgur_id = url[len(url) - 7:]
    print('ID: ', imgur_id)
    if len(imgur_id) != 7:
        return
    else:
        return imgur_id


def __init__():
    num_img_dl = 0
    input_password = getpass.getpass(prompt='Data Hoarding Bot Password: ')

    if str(input('Do you want recursive mode? (y/n)')) == 'y':
        wait_time = str(input('Wait time? (Default 60 seconds): '))
        if wait_time == '':
            wait_time = 60
        else:
            while True:
                if wait_time == '':
                    wait_time = 60
                    break
                try:
                    wait_time = int(wait_time)
                    if wait_time > 60:
                        wait_time /= 60
                        time_unit = 'minute/s'
                    else:
                        time_unit = 'seconds'
                    break
                except ValueError:
                    print('Invalid Input!')
                    wait_time = str(input('Wait time? (Default 60 seconds): '))
        times_run = 0
        start_time = time()
        while True:
            system('cls' if name == 'nt' else 'clear')  # Clear screen before use
            run_time = time() - start_time
            if run_time > 60:
                run_time /= 60
                run_time_unit = 'minute/s'
            else:
                run_time_unit = 'seconds'

            num_img_dl += main(input_password)
            times_run += 1

            sleep(5)
            system('cls' if name == 'nt' else 'clear')  # Clear screen before use

            current_time = str(localtime()[3]) + ':' + str(localtime()[4]) + ':' + str(localtime()[5]) + ' - ' + str(
                localtime()[2]) + '/' + str(localtime()[1]) + '/' + str(localtime()[0])

            log_msg = current_time + ':: Total Images DL: ' + str(num_img_dl) + ' -- Total Times run: ' + str(
                times_run) + ' -- Recursive mode: ON'

            with open('ws_log', 'a') as ws_log:  # Append to the bottom of the file the new post id
                ws_log.write(log_msg + '\n')

            print('Times run: ', times_run, ' -- Total Run Time: ', round(run_time, 0), ' ', run_time_unit,
                  ' -- Total # of Images Downloaded: ', num_img_dl, sep='')
            next_run_time = datetime.datetime.now() + datetime.timedelta(minutes=round(wait_time, 2))

            print('Waiting ', round(wait_time, 2), time_unit, '[', next_run_time, '] till next check...')

            if time_unit == 'seconds':
                sleep(wait_time)
            else:
                sleep(wait_time * 60)
    else:
        system('cls' if name == 'nt' else 'clear')  # Clear screen before use
        num_img_dl = main(input_password)
        current_time = str(localtime()[3]) + ':' + str(localtime()[4]) + ':' + str(localtime()[5]) + ' - ' + str(
            localtime()[2]) + '/' + str(localtime()[1]) + '/' + str(localtime()[0])
        log_msg = current_time + ':: Total Images DL: ' + str(num_img_dl) + ' -- Recursive mode: OFF'
        with open('ws_log', 'a') as ws_log:  # Append to the bottom of the file the new post id
            ws_log.write(log_msg + '\n')


if __name__ == '__main__':
    __init__()
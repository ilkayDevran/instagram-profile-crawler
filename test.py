#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @author: Ilkay Tevfik Devran
# @updatedDate: 22.04.2019
# @version: 1.0 

import os
from time import sleep
from instacrawler.browser import Browser
from instacrawler.instaCrawler import InstaCrawler, Profile, Post
from imageDownloader import ImageDownloader
import json 
import re


def test_browser():
    url='https://www.instagram.com/'
    userName = 'jannaaaeeee'

    browser = Browser(run_locally=True)
    browser.get(url+userName)
    asd= browser.find_one('.g47SY')


    print asd.text
    sleep(5)
    sleep(5)
    browser.scroll_down()
    #asd.click()
    sleep(5)

def test_instaCrawler():
    url='https://www.instagram.com/'
    userName = 'jannaaaeeee'
    crawler = InstaCrawler()
    posts = crawler.get_posts_from_profile(userName, total_post_count=None)

    print json.dumps(posts,indent=4)
    
    # think that another lambda hereeee
    print ("Start downloading...")
    downloader = ImageDownloader()
    downloader.download_images(posts['Posts'])

def remove_emoji(data):
    if not data:
        return data
    if not isinstance(data, basestring):
        return data
    try:
    # UCS-4
        patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
    # UCS-2
        patt = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
    return patt.sub('', data)

def test():
    #userName_list = ['jannaaaeeee']
    userName_list = ['furkanvardar']
    #userName_list = ['iceland.blog']
    
    stalker = InstaCrawler(retry_limit=5, total_post_count=7)
    profiles=[]
    for userName in userName_list:
        profile = Profile(userName)
        stalker.get_profile_details(profile)
        profiles.append(profile)
    data = json.dumps(profiles[0].get_json(), indent=4, ensure_ascii=False).encode('utf-8')
    print data

test()

def test_urls():
    urls = [
        'https://www.instagram.com/iceland.blog/', 
        'https://www.instagram.com/trailofus/',
        'https://www.instagram.com/travelandleisure/',
        'https://www.instagram.com/turkey_home/',
        'https://www.instagram.com/gopro/',
        'https://www.instagram.com/sony/',
        'https://www.instagram.com/djiglobal/',
        'https://www.instagram.com/canonusa/',
        'https://www.instagram.com/trendyolcom/',
        'https://www.instagram.com/asos/',
        'https://www.instagram.com/topshop/',
        'https://www.instagram.com/mavi/',
        'https://www.instagram.com/lcwaikiki/'
        ]
    stalker = InstaCrawler(retry_limit=5, total_post_count=2)

    profiles=[]
    for url in urls:
        profile = Profile(profileUrl=url)
        stalker.get_profile_details(profile)
        profiles.append(profile)
        
        data = json.dumps(profile.get_json(), indent=4, ensure_ascii=False).encode('utf-8')
        print (data)
        print("\n\n")
        break

#test_urls()


def test_get_post_details():
    jsn = {
        "Profile": {
            "UserName": "jannaaaeeee", 
            "Url": "https://www.instagram.com/jannaaaeeee/", 
            "PostCount": 154, 
            "Following": 591, 
            "Followers": 171312
        }, 
        "Posts": [
            {
            "PostDate": "null", 
            "Key": "https://www.instagram.com/p/BfECCktDc_5/", 
            "Tags": [], 
            "ImageUrl": "https://instagram.fsaw1-6.fna.fbcdn.net/vp/b6e6c65c101d5fd514456f41cb302a38/5D61700A/t51.2885-15/sh0.08/e35/c0.135.1080.1080a/s640x640/41322810_370780943464388_5955088283229749248_n.jpg?_nc_ht=instagram.fsaw1-6.fna.fbcdn.net", 
            "CaptionInProfilePage": "🌞day", 
            "CrawledTime": "", 
            "CaptionInPostPage": "", 
            "LikeCount": "null"
        }, 
        {
            "PostDate": "null", 
            "Key": "https://www.instagram.com/p/Be5mg4lDd_c/", 
            "Tags": [], 
            "ImageUrl": "https://instagram.fsaw1-6.fna.fbcdn.net/vp/c1dc0df45ddd7e42ee601413a98e4faf/5D7783D4/t51.2885-15/sh0.08/e35/c0.135.1080.1080a/s640x640/41415338_342567346487621_6773846398606508032_n.jpg?_nc_ht=instagram.fsaw1-6.fna.fbcdn.net", 
            "CaptionInProfilePage": "Favorite place 🌴", 
            "CrawledTime": "", 
            "CaptionInPostPage": "", 
            "LikeCount": "null"
        }, 
        {
            "PostDate": "null", 
            "Key": "https://www.instagram.com/p/Be0eKUoDFLU/", 
            "Tags": [], 
            "ImageUrl": "https://instagram.fsaw1-6.fna.fbcdn.net/vp/cc7de90219bc2b49f80b07d3cb6d14e6/5D56EDDA/t51.2885-15/sh0.08/e35/c127.0.825.825/s640x640/41337039_2091735581155085_7448479039460737024_n.jpg?_nc_ht=instagram.fsaw1-6.fna.fbcdn.net", 
            "CaptionInProfilePage": "Paradise 🌴", 
            "CrawledTime": "", 
            "CaptionInPostPage": "", 
            "LikeCount": "null"
        }
        ] 
    }
    profile = Profile()
    profile.load_from_json(jsn)
    #print(json.dumps(profile.get_json(),indent=4, ensure_ascii=False))
    stalker = InstaCrawler()
    #stalker.get_profile_details(profile)
    stalker.test_post(profile)
    data = profile.get_json()
    print type(data)

    print(json.dumps(data, indent=4, ensure_ascii=False))

#test_get_post_details()

def progressbar_test():
    from progress.bar import FillingCirclesBar
    import time

    with FillingCirclesBar('Processing', max=5) as bar:
        for i in range(5):
            # Do some work
            time.sleep(.5)
            bar.next()
    bar.finish()

def snipper_test():
    import time    
    from progress.spinner import Spinner

    #spinner = Spinner('Loading ')
    with Spinner('Loading ') as spinner:
        while 1:
            # Do some work
            time.sleep(1)
            spinner.next()
    spinner.finish()

#snipper_test()
"""
a = {
        "Profile": {
            "UserName": "jannaaaeeee", 
            "Url": "https://www.instagram.com/jannaaaeeee/", 
            "PostCount": 154, 
            "Following": 591, 
            "Followers": 171312
        }, 
        "Posts": [
            {
            "PostDate": "null", 
            "Key": "https://www.instagram.com/p/BfECCktDc_5/", 
            "Tags": [], 
            "ImageUrl": "https://instagram.fsaw1-6.fna.fbcdn.net/vp/b6e6c65c101d5fd514456f41cb302a38/5D61700A/t51.2885-15/sh0.08/e35/c0.135.1080.1080a/s640x640/41322810_370780943464388_5955088283229749248_n.jpg?_nc_ht=instagram.fsaw1-6.fna.fbcdn.net", 
            "CaptionInProfilePage": "🌞day", 
            "CrawledTime": "", 
            "CaptionInPostPage": "", 
            "LikeCount": "null"
        }, 
        {
            "PostDate": "null", 
            "Key": "https://www.instagram.com/p/Be5mg4lDd_c/", 
            "Tags": [], 
            "ImageUrl": "https://instagram.fsaw1-6.fna.fbcdn.net/vp/c1dc0df45ddd7e42ee601413a98e4faf/5D7783D4/t51.2885-15/sh0.08/e35/c0.135.1080.1080a/s640x640/41415338_342567346487621_6773846398606508032_n.jpg?_nc_ht=instagram.fsaw1-6.fna.fbcdn.net", 
            "CaptionInProfilePage": "Favorite place 🌴", 
            "CrawledTime": "", 
            "CaptionInPostPage": "", 
            "LikeCount": "null"
        }, 
        {
            "PostDate": "null", 
            "Key": "https://www.instagram.com/p/Be0eKUoDFLU/", 
            "Tags": [], 
            "ImageUrl": "https://instagram.fsaw1-6.fna.fbcdn.net/vp/cc7de90219bc2b49f80b07d3cb6d14e6/5D56EDDA/t51.2885-15/sh0.08/e35/c127.0.825.825/s640x640/41337039_2091735581155085_7448479039460737024_n.jpg?_nc_ht=instagram.fsaw1-6.fna.fbcdn.net", 
            "CaptionInProfilePage": "Paradise 🌴", 
            "CrawledTime": "", 
            "CaptionInPostPage": "", 
            "LikeCount": "null"
        }
        ] 
    }

a = remove_emoji(json.dumps(a,indent=4, ensure_ascii=False))
#print(json.dumps(a,indent=4, ensure_ascii=False))
print a"""



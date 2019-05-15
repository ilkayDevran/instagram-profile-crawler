#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @author: Ilkay Tevfik Devran
# @updatedDate: 07.05.2019
# @version: 1.0.7 
from __future__ import unicode_literals

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

from instacrawler.browser import Browser
from datetime import datetime, timedelta
from progress.bar import FillingCirclesBar
from progress.spinner import Spinner

import re
import json
import random
from time import sleep



class Post:
    def __init__(self):
        # Info that's gotten from PROFILE page
        self.key='' 
        self.imageUrl='' 
        self.captionInProfilePage=''
        
        # Info that's gotten from POST page
        self.postDate=None # time class = _1o9PC Nzb55
        self.likeCount=None # a class = zV_Nj span
        self.captionInPostPage=''
        self.tags=[]
        self.crawledTime=''
        self.viewCount = None
        self.mentions = []
        self.captionByUser = ''
        self.postType = ''
        self.facebookCaption = ''

    def set_attributes(self, postDate, likeCount, captionInPostPage, tags, viewCount, captionByUser, mentions):
        self.postDate = postDate
        self.likeCount = likeCount
        self.tags = tags
        self.captionInPostPage = captionInPostPage
        self.crawledTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mentions = mentions
        self.viewCount = viewCount
        self.captionByUser = captionByUser 

    @property
    def meta_data(self):
        captionInProfilePage = self.captionInProfilePage.encode('utf-8')
        captionInPostPage = self.captionInPostPage.encode('utf-8')
        captionByUser = self.captionByUser.encode('utf-8') 
        
        if 'Image may contain:' in captionInProfilePage and captionInProfilePage != captionByUser:
            self.facebookCaption =  captionInProfilePage 
        elif 'Image may contain:' in captionInPostPage and captionInPostPage != captionByUser:
            self.facebookCaption = captionInPostPage 
        
        data = {    
                    "Key": self.key,
                    "ImageUrl": self.imageUrl,
                    "PostDate": self.postDate,
                    "LikeCount": self.likeCount,
                    "Tags": self.tags,
                    "CrawledTime": self.crawledTime,
                    "ViewCount": self.viewCount,
                    "Mentions": self.mentions,
                    "CaptionByUser": self.captionByUser.encode('utf-8'),
                    "PostType": self.postType,
                    "FacebookCaption": self.facebookCaption
                }


        return data

    def __str__(self):
        print (
            "\nDate: " + self.postDate + "\n" +
            "CaptionInProfilePage: " + self.captionInProfilePage.encode('utf-8') + "\n" +
            "CaptionInPostPage: " + self.captionInPostPage.encode('utf-8') + "\n" +
            "Like: " + str(self.likeCount) + "\n" +
            "ViewCount: " + str(self.viewCount) + "\n" +
            "CaptionByUser: " + self.captionByUser.encode('utf-8') + "\n" +
            "Key: " + self.key + "\n" +
            "ImageUrl: " + self.imageUrl + 
            "PostType:" + self.postType + 
            "FacebookCaption" + self.facebookCaption + "\nTags: ") 
        
        if len(self.tags) == 0:
            print("[]")
        else:    
            for t in self.tags:
                print(t,)
        print("\n")

        print("Mentions: ")
        if len(self.mentions) == 0:
            print("[]")
        else:    
            for m in self.mentions:
                print(m,)
        print("\nCrawlTime: " + self.crawledTime)

    def load_from_json(self, jsn):
        jsn = json.dumps(jsn, ensure_ascii=False)
        jsn = json.loads(jsn)
        try:
            self.key = jsn['Key']
            self.imageUrl = jsn['ImageUrl']
            self.captionInProfilePage = jsn['CaptionInProfilePage']

            self.postDate = jsn['PostDate'].replace("T"," ").replace("Z","")
            self.likeCount = jsn['LikeCount']
            self.captionInPostPage = jsn['CaptionInPostPage']
            self.tags = jsn['Tags']
            self.crawledTime =jsn['CrawledTime']

        except Exception as e:
            raise Exception("|ERROR|--- Post Class ---\n load_from_json()\n \
                Json fromat is not acceptable.\n"+e.__str__()+"\n\n")


class Profile:
    def __init__(self, userName=None, profileUrl=None):
        
        if userName != None:
            self.userName = str(userName)
            self.url = ''.join(['https://www.instagram.com/',str(userName),'/'])
        elif profileUrl != None:
            self.userName = profileUrl.split('/')[-2]
            self.url = profileUrl
        else:
            print("User Name or Profile Url is not determined!")
            exit(1)
        
        self.followingCount = 0
        self.followersCount = 0
        self.postCount = 0
        self.postsList = []
    
    def set_meta_info(self, metaInfo):
        self.postCount = int( metaInfo[0].text.replace(',','').replace('.','') )
        self.followersCount = int( metaInfo[1].get_attribute('title').replace(',','').replace('.','') )
        self.followingCount = int( metaInfo[2].text.replace(',','').replace('.','') )
        self.profileCrawledTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def addPost(self, p):
        self.postsList.append(p)
    
    def __str__(self):
        print("\nUserName:" + self.userName + 
            " Post: " + str(self.postCount) + 
            " Followers: " + str(self.followersCount) + 
            " Following: " + str(self.followingCount) +
            "\nProfileUrl: " + self.url+"\n")
    
    def get_json(self):
        jsn = {}
        jsn['Profile'] = {}
        jsn['Profile']['UserName'] = self.userName
        jsn['Profile']['Url'] = self.url
        jsn['Profile']['Followers'] = self.followersCount
        jsn['Profile']['Following'] = self.followingCount
        jsn['Profile']['PostCount'] = self.postCount
        jsn['Profile']['CrawledDate'] = self.profileCrawledTime
        jsn['Posts'] = [p.meta_data for p in self.postsList]
        
        return jsn

    def load_from_json(self, jsn):
        jsn = json.dumps(jsn, ensure_ascii=False)
        jsn = json.loads(jsn)
        try:
            self.userName = jsn['Profile']['UserName']
            self.url = jsn['Profile']['Url']
            self.followingCount = jsn['Profile']['Following']
            self.followersCount = jsn['Profile']['Followers']
            self.postCount = jsn['Profile']['PostCount']
            for p in jsn['Posts']:
                post = Post()
                post.load_from_json(p)
                self.postsList.append(post)
        except Exception as e:
            raise Exception("|ERROR|--- Profile Class ---\n load_from_json()\n \
                Json fromat is not acceptable.\n"+e.__str__()+"\n\n")
            exit(1)


class InstaCrawler:
    def __init__(self, retry_limit=5, run_locally=True, total_post_count=0):
        self.browser = Browser(run_locally) # CHANGE run_locally ot False WHEN IT DEPLOYED INTO LAMBDA
        self.retry_limit = retry_limit
        self.total_post_count = total_post_count
    
    # Private Functions
    def __get_posts_from_profile(self, profile, try_limit):
        browser = self.browser
        rng = self.total_post_count
        if self.total_post_count == 0:
            rng = profile.postCount

        print("To be processed post count: " + str(rng))
        with Spinner(profile.userName + "'s profile is crawling ") as spinner:
            posts = []
            key_set = set()
            post_counter = 0
            while post_counter < rng:
                if try_limit == 0:
                    break
                try:
                    dozen_posts = browser.find('.v1Nh3 a', waittime=1)
                    for p in (dozen_posts):
                        if post_counter >= self.total_post_count:
                            break
                        key = p.get_attribute('href')
                        if key not in key_set:
                            p_img = browser.find_one('.KL4Bh img', p)

                            post = Post()
                            post.captionInProfilePage = p_img.get_attribute('alt')  # NOTE: Emojis in captionInProfilePage may be a problem for future...
                            post.imageUrl = p_img.get_attribute('src')
                            post.key = key

                            profile.addPost(post)

                            key_set.add(key)
                            post_counter+=1

                    browser.scroll_down()
                    browser.randmized_sleep()
                except Exception as e:
                    print (e.__str__())
                    try_limit -= 1
                spinner.next()
        
        spinner.finish()
        
        #return profile
    
    def __get_details_of_posts(self, profile):
        browser = self.browser
        posts = profile.postsList
        with FillingCirclesBar('Processing', max=len(posts)) as bar:
            for p in posts:
                likeCount = 0
                viewCount = 0
                captionByUser = ''
                try:
                    browser.go(p.key) # Go to post page on browser
                    browser.randmized_sleep()
                    postDate = browser.find_one('._1o9PC').get_attribute('datetime').replace('T', ' ').replace('.000Z','')
                    try:
                        likeCount = int(browser.find_one('.zV_Nj').text.split()[0].replace(",","").replace(".",""))
                        captionInPostPage = browser.find_one('.KL4Bh img').get_attribute('alt')
                        p.postType = 'photo'
                    except:
                        # Actually it is viewCount if the post is a video content
                        try:
                            viewCount = int(browser.find_one('.vcOH2').text.split()[0].replace(",","").replace(".",""))
                        except:
                            likeCount = int(browser.find_one('.zV_Nj').text.split()[0].replace(",","").replace(".",""))
                        captionInPostPage = '*-Video Content-*'
                        p.captionInProfilePage = '*-Video Content-*'
                        p.postType = 'video'
                    # Extract Tags and Mentions from post caption
                    tags=set()
                    mentions=set()
                    firstCaptionForPost = browser.find_one('.C4VMK')
                    # Check if first caption for the post is really belongs to the profile User to extract tags
                    if str(browser.find_one('._6lAjh a', firstCaptionForPost).get_attribute('href')) == str(browser.find_one('.BrX75 a').get_attribute('href')):
                        captionByUser = re.sub(r'#.*?(\s+|$)', '', re.sub(r'@.*?(\s+|$)', '', firstCaptionForPost.text)).replace(profile.userName, '').replace('\n', ' ') # username in caption issue....
                        tmp = browser.find(firstCaptionForPost, x_path='//a')
                        for a in tmp:
                            if '#' in a.text:
                                tags.add(str(a.get_attribute('href')).replace('https://www.instagram.com/explore/tags/','').replace('/',''))
                            elif '@' in a.text:
                                mentions.add(str(a.get_attribute('href')).replace('https://www.instagram.com/','').replace('/',''))
                    tags = list(tags)
                    mentions = list(mentions)
                    p.set_attributes(postDate, likeCount, captionInPostPage, tags, viewCount, captionByUser, mentions)
                except Exception as e:
                    print(e.__str__())
                
                #sleep(random.uniform(2, 4)) # SLEEP before next http request!
                bar.next()
        bar.finish()

    # Public Functions
    def get_profile_details(self, profile):
        browser = self.browser
        try_limit = self.retry_limit
        browser.go(profile.url) # Go to user profile on browser
        
        meta_profile_info = browser.find('.g47SY', waittime=4)
        profile.set_meta_info(meta_profile_info)
        self.__get_posts_from_profile(profile, try_limit)
        self.__get_details_of_posts(profile)
    
#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @author: Ilkay Tevfik Devran
# @updatedDate: 14.05.2019
# @version: 1.0 

from instacrawler.instaCrawler import InstaCrawler, Profile, Post
import json


def main():
    crawler = InstaCrawler(retry_limit=5, total_post_count=7)

    profileURLS = ['https://www.instagram.com/gopro/'] # add here profile urls that u'd like to crawl

    profiles=[]
    for url in profileURLS:
        profile = Profile(profileUrl=url)
        crawler.get_profile_details(profile)
        profiles.append(profile)
        meta_data = profile.get_json()
        print (json.dumps(meta_data, indent=4, ensure_ascii=False).encode('utf-8'))


if __name__ == "__main__":
    main()

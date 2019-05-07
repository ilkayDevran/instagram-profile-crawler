#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @author: Ilkay Tevfik Devran
# @updatedDate: 22.04.2019
# @version: 1.0 

from instacrawler.browser import Browser

class ImageDownloader:

    def __init__(self):
        self.browser = Browser(run_locally=True) # CHANGE run_locally ot False WHEN IT DEPLOYED INTO LAMBDA
    
    def img(self, postList):
        
        def send_request(url):
            s = requests.Session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            } 
            try:  
                return s.get(url, headers=headers)
            except Exception:
                print ('ERROR:(SEND REQUEST METHOD)\n' + url)
                return None

        for i, post in enumerate(postList):
            try:
                response = send_request(post['key'])
                parsed_post_page = BeautifulSoup(response.content, 'html.parser')  # Parse main page
                img_in_post_page = parsed_post_page.find_all('img', attrs={'class':'FFVAD'})[0]
                print img_in_post_page
                #print  img_in_post_page
                #post['alt'] = img_in_post_page.alt
            except Exception as e:
                post['alt'] = ''
                raise e
            postList[i] = post

        return postList


    def download_images(self, postList):
        pass


import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import time
import threading

"""
This file performs the first pass of the web scraping as outlined in the methodology.
"""

# this is an error string that will show up in the raw html file
# if you try to download a post which does not exist
err="""The School of Life is a global organisation committed to emotional well-being, especially around relationships and work. We're about wisdom, emotional intelligence and self-understanding. This is the place where our community connects, shares insights, chats, learns and meets up."""

posts=[]
def fetch(url):
    # download and returns the raw html content
    response=urllib.request.urlopen(url)
    
    # converts from UTF-8 to ascii
    data=response.read().decode('utf-8')
    
    # instantiates BeautifulSoup which parses the html response into an object
    # that can be easily queried in
    parsed_html = BeautifulSoup(data,features='html5lib')
    
    # posts contain a tag like this
    # <meta content="Knowledge theory, sociology, identity, feminism." name="description">
    # that contains the first 200 characters of the post
    # here we try to search for the meta tag with the property 'name' and value 'description'
    # if we find such a tag, extract the value of the 'content' property
    out=(parsed_html.find('meta', attrs={'name':'description'})['content'])
    
    # 
    guid=(url.split('/')[-1])
    
    # if it is an invalid post the content of the meta tag will be the 'err' variable defined above
    # in this case simply print the post guid for reference
    if out==err:
        print(guid)
    else:
        # it is a valid post, keep track of the guid and the content of the post
        posts.append(str(guid)+":"+out+'\n')
        print (guid,out)

if __name__ == "__main__":
    # open a file to write records to
    fid=open('posts-200','w')
    
    # iterate through possible GUIDS in the range [2200000, 2000000] in decreasing order
    # for each iteration of the loop look at 100 GUIDs at a time
    for start in np.arange(2200000,2000000,-100):
        tt=time.time()
        
        # generate all the 100 GUIDs to look at
        nums=np.arange(start,start+100)
        
        # generate the full URL for each GUID
        urls=["https://community.theschooloflife.com/posts/"+str(i) for i in nums]
        
        # concurrently ping 100 urls at the same time using 100 threads
        # create 100 threads, each thread will call the fetch() method with the appropriate url
        threads = [threading.Thread(target=fetch, args=(url,)) for url in urls]
        
        # start 100 threads
        for thread in threads:
            thread.start()
            
        # wait for 100 threads to finish
        for thread in threads:
            thread.join()
        
        # write all collected records of valid posts to disk
        for post in posts:
            fid.write(post)
        fid.flush()
        
        # 'reset' the list of records for the next loop iteration
        posts=[]
        
        # print how long it took to finish one iteration of this loop
        print(time.time()-tt,start)
        
    # close the file
    fid.close()


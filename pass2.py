from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os

"""
This does pass 2 as described in the methodology of the document
"""

# instantiate a headless version of Firefox with the Selenium driver
# only need to do this once
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

def fetch(guid,cc):
    tt=time.time()
    
    # create a file to save the contents of the post to
    fname='./users/'+str(guid)+'.html'

    # check if file exists
    if not os.path.isfile(fname):
        # generate the url
        url='https://community.theschooloflife.com/members/'+str(id)
        
        # ask selenium to render
        driver.get(url)
        
        # keep checking the render status until the word 'post-location' occurs in the html
        # this is a safe check to ensure the post has fully rendered
        for j in range(120):
            html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')

            # returns character index of the substring 'post-location'
            # if it doesn't exist -1 is returned
            ll=html.find('post-location')
            
            # if post-location exists, we are done, break out of the loop
            if ll > 0:
                print ('done',id,cc,time.time()-tt)
                break

            # timeout and if we can't find that tag, maybe no location associated with that post
            # or that post has some kind of error
            if j == 119:
                print ('timeout',id)
                
            # sleep a bit wait for browser to render
            time.sleep(.5)
        
        # return the post contents to disk
        fid=open(fname,'w+')
        fid.write(html)
        fid.close()

if __name__ == "__main__":
    # open the file containing all valid post ids, and get each individual line, close the file
    ids=open('/home/justin/eclipse-workspace/tsol/postids-master')
    lines=sorted(ids.read().split('\n'))
    ids.close()
    
    # look at all records starting from record i
    i=2430
    for guid in lines[i:]:
        # examine record if line length > 0
        if len(guid)>0:
            # if there is an exception/failure due to a bad network connection
            # keep trying to get the record
            while True:
                try:
                    fetch(guid,i)
                    break
                except:
                    # wait 5 seconds for network to become good again, keep retrying
                    time.sleep(5)
                    continue
        i+=1


































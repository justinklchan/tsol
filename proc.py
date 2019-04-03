import os
from bs4 import BeautifulSoup
import textstat
import operator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
stop_words = set(stopwords.words('english')) 

def getcontent(soup):
    div=soup.find("div", {"class": "detail-layout-description"})
    if div:
        return div.contents[0].strip()
    return None

def getuser(soup):
    div=soup.find("a", {"class": "mighty-attribution-name"}).contents[0].contents[0]
    return div

def getdate(soup):
    div=soup.find('span',{'class':'detail-layout-post-created-at'}).contents[0][7:]
    return div

def getmobile(soup):
    ss=soup.find('a',{'class':'detail-layout-from-mobile-app'})
    if not ss:
        return 'PC'
    else:
        div=ss.contents[0]
        if 'Android' in div:
            return 'Android'
        elif 'iOS' in div:
            return 'iOS'

dd='/home/justin/tsol/posts/'
fs=sorted(os.listdir(dd))

def procmobile():
    cc=0
    histo={}
    for i in fs[:200]:
        ff=open(dd+i,'r')
        data=ff.read()
        ff.close()
        soup = BeautifulSoup(data, 'html.parser')
        u=getmobile(soup)
        if u not in histo.keys():
            histo[u]=0
        else:
            histo[u]+=1
        print (cc,i)
        cc+=1    
    ff=open('./qa/mobile','w+')
    for i in histo.keys():
        ff.write(i+','+str(histo[i])+'\n')
    ff.close()

def excontent():
    cc=0
    for i in fs[:200]:
        ff=open(dd+i,'r')
        data=ff.read()
        ff.close()
        soup = BeautifulSoup(data, 'html.parser')
        u=getcontent(soup)
        if u:
            f2=open('/home/justin/tsol/content/'+i[:-5],'w+')
            f2.write(u)
            f2.close()
            print(cc,i)
        else:
            print('!!!!',cc,i)
        cc+=1

def compcontent():
    f2=open('/home/justin/tsol/content/master','w+')
    for i in os.listdir('/home/justin/tsol/content/'):
        ff=open('/home/justin/tsol/content/'+i)
        f2.write(ff.read())
        ff.close()
    f2.close()
        
def exflesch():
    cc=0
    for i in fs[:200]:
        fname='/home/justin/tsol/content/'+i[:-5]
        if os.path.exists(fname):
            ff=open(fname,'r')
            data=ff.read().encode('ascii', 'ignore').decode("utf-8")
            ff.close()
            if len(data)>100:
                u=textstat.flesch_reading_ease(data)
                f2=open('/home/justin/tsol/flesch/'+i[:-5],'w+')
                f2.write(str(u))
                f2.close()

def procflesch():
    cc=0
    histo={'0-29':0,
           '30-49':0,
           '50-59':0,
           '60-69':0,
           '70-79':0,
           '80-89':0,
           '90-100':0}
    for i in os.listdir('/home/justin/tsol/flesch/'):
        ff=open('/home/justin/tsol/flesch/'+i,'r')
        data=float(ff.read())
        ff.close()
        if 0 <= data and data <= 29:
            histo['0-29']+=1
        elif 30 <= data and data <= 49:
            histo['0-29']+=1
        elif 50 <= data and data <= 59:
            histo['50-59']+=1
        elif 60 <= data and data <= 69:
            histo['60-69']+=1
        elif 70 <= data and data <= 79:
            histo['70-79']+=1
        elif 80 <= data and data <= 89:
            histo['80-89']+=1
        elif 90 <= data and data <= 100:
            histo['90-100']+=1
    ff=open('./qa/flesch','w+')
    for i in histo.keys():
        ff.write(i+','+str(histo[i])+'\n')
    ff.close()                

def proccontent():
    ff=open('/home/justin/tsol/content/master','r')
    
    toks = word_tokenize(ff.read()) 
    
    stop_words.add('i')
    filt = [w.lower() for w in toks if w.lower() not in stop_words and w.isalpha()] 

    ff.close()
    
    histo={}
    for i in filt:
        if i not in histo.keys():
            histo[i]=0
        histo[i]+=1
        
    ff=open('./qa/words','w+')
    ss = sorted(histo.items(), key=operator.itemgetter(1),reverse=True)
    cc=0
    for i in ss:
        if i[1]>10:
            ff.write(i[0]+','+str(i[1])+'\n')
            cc+=1
    print (cc)
    ff.close()
    
# excontent()
# exflesch()
# procflesch()
# compcontent()
proccontent()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
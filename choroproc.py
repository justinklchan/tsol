import os
from bs4 import BeautifulSoup
import pycountry
import operator

"""
genlocs()
Outputs files that can be plotted for a global or USA-only choropleth
The output file is structured as 
<GUID>:<ISO-3-identifier>
or
<GUID>:<US-state-identifier>

genhisto()
Outputs histogram files like
USA,54
IND,36
GBR,8
"""

# TSOL uses non-conventional representations of country names
# hard-code a map mapping the non-conventional representation to a conventional one
creplace={
    'Italia':'Italy',
    'Brasil':'Brazil',
    'Việt Nam':'Viet Nam',
    'Vietnam':'Viet Nam',
    'België':'Belgium',
    "O'zbekiston":'Uzbekistan',
    'South Korea':'Korea, Republic of',
    'Deutschland':'Germany',
    'Lietuva':'Lithuania',
    'Србија':'Serbia',
    'España':'Spain',
    'الجزائر':'Algeria',
    'Schweiz':'Switzerland',
    'Türkiye':'Turkey',
    'Sverige':'Sweden',
    'Россия':'Russian Federation',
    'República Bolivariana De Venezuela':'Venezuela, Bolivarian Republic of',
    'México':'Mexico',
    'Nederland':'Netherlands',
    '香港-中國':'Hong Kong',
    'Česká Republika':'Czechia',
    'República de Chile':'Chile',
    'Suisse':'Switzerland',
    'Tanzania':'Tanzania, United Republic of',
    'Bosna i Hercegovina':'Bosnia and Herzegovina',
    'السعودية':'Saudi Arabia',
    'لبنان':'Lebanon'
}

# get location information for each post
def genlocs(usa=False):
    cc=0
    if usa:
        ll=open('./qa/locs-usa','w+')
    else:
        ll=open('./qa/locs','w+')
    
    # iterate through each post
    dd='/home/justin/tsol/posts/'
    fs=sorted(os.listdir(dd))
    for i in fs[:200]:
        # read content of post
        ff=open(dd+i,'r')
        data=ff.read()
        ff.close()
        
        # parse out its unformatted location
        soup = BeautifulSoup(data, 'html.parser')
        span=soup.find("span", {"class": "detail-layout-post-location"})
        longloc=span.contents[0]
        
        # get the ISO-3 or shortened US state representation
        shortloc=string2loc(longloc,usa)
        print (cc,i,longloc,shortloc)
        
        # write to disk
        ll.write(str(i)+":"+shortloc+"\n")
        cc+=1
    ll.close()

# use pycountry interface to map countries to ISO-3 representation
def string2loc(tt,usa=False):
    country=tt.split(',')[1].strip()
    if len(country) == 2 and country.isupper():
        if usa:
            return country
        else:
            country='United States'
    if country in creplace.keys():
        country=creplace[country]
    return pycountry.countries.get(name=country).alpha_3

# build histogram
def genhisto(usa=False):
    if usa:
        ff=open('qa/locs-usa','r')
    else:
        ff=open('qa/locs','r')
    lines=ff.read().split('\n')
    
    histo={}
    for line in lines:
        if len(line)>0:
            place=line.split(':')[1]
            if place not in histo.keys():
                histo[place]=0
            histo[place]+=1
    ff.close()
    
    if usa:
        f2=open('qa/locshisto-usa','w+')
    else:
        f2=open('qa/locshisto','w+')
        
    f2.write('CODE,POPULATION\n')
    ss = sorted(histo.items(), key=operator.itemgetter(1),reverse=True)
    for i in ss:
        if usa and len(i[0]) == 2:
            f2.write(i[0]+','+str(i[1])+'\n')
        elif not usa:
            f2.write(i[0]+','+str(i[1])+'\n')
    f2.close() 

# genlocs(True)
# genlocs()
genhisto(True)
genhisto()





































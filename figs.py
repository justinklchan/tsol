import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

def mobile():
    ff=open('./qa/mobile')
    lines=ff.read().split('\n')
    
    x=[]
    y=[]
    for line in lines:
       elts=line.split(',')

       if len(elts)>1:
           x.append(elts[0])
           y.append(int(elts[1]))
    df=pd.DataFrame(data={'Computing platform':x,'Count':y,'hue':[1]*len(y)})
    
    ff.close()
    
    sns.set()
    fig=plt.figure()
    sns.barplot(x="Computing platform", y="Count", hue='hue',data=df)
    plt.legend().remove()
    plt.tight_layout()
    plt.savefig('./mobile.png',dpi=fig.dpi)
    plt.show()
    
def flesch():
    ff=open('./qa/flesch')
    lines=ff.read().split('\n')
    
    x=[]
    y=[]
    for line in lines:
       elts=line.split(',')

       if len(elts)>1:
           x.append(elts[0])
           y.append(int(elts[1]))
    
    labels=['Very Confusing','Difficult','Fairly Difficult','Standard','Fairly Easy','Easy','Very Easy']
    df=pd.DataFrame(data={'Reading level':labels,'Count':y,'hue':[1]*len(y)})
    
    ff.close()
    
    sns.set()
    fig=plt.figure(figsize=(10,5))
    plt.title('Flesch Reading Ease Score')
    sns.barplot(x="Reading level", y="Count", hue='hue',data=df)
    plt.legend().remove()
    plt.tight_layout()
    plt.savefig('./flesch.png',dpi=fig.dpi)
    plt.show()

def wordcloud():
    ff=open('/home/justin/tsol/content/master','r')
    text=ff.read()
    ff.close()
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(background_color="white",stopwords=stopwords,
                          max_font_size=60,collocations=False,
                          ).generate_from_text(text)
    fig=plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('./wordcloud.png',dpi=fig.dpi)
    plt.show()
    
def wordfreq():
    ff=open('./qa/words','r')
    lines=ff.read().split('\n')
    
    x=[]
    y=[]
    for line in lines:
       elts=line.split(',')
       if len(elts)>1:
           x.append(elts[0])
           y.append(int(elts[1]))
    df=pd.DataFrame(data={'Words':x,'Count':y,'hue':[1]*len(y)})
    
    ff.close()
    
    sns.set()
    fig=plt.figure(figsize=(5,10))
    sns.barplot(y="Words", x="Count", hue='hue',data=df)
    plt.legend().remove()
    plt.tight_layout()
    plt.savefig('./words.png',dpi=fig.dpi)
    plt.show()

wordfreq()
# wordcloud()
# flesch()
# mobile()































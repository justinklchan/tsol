import plotly.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import seaborn as sns

cscale=[]
jet=open('jet','r').read().split('\n')
nlines=len(jet)-1
counter=0.0
for line in jet:
    cc=line.split()
    cc=[255*float(i) for i in cc]
    
    cscale.append([counter/nlines,'rgb('+str(cc[0])+','+str(cc[1])+','+str(cc[2])+')'])
    counter+=1

def graph(usa=False):
    if usa:
        lmode = 'USA-states'
        df=pd.read_csv('./qa/locshisto-usa')
    else:
        lmode='ISO-3'
        df=pd.read_csv('./qa/locshisto')
            
    data = [go.Choropleth(
        locations = df['CODE'],
        z = df['POPULATION'],
        colorscale = cscale,
        locationmode=lmode
    )]
    
    if usa:
        gg = go.layout.Geo(
            scope = 'usa',
            projection = go.layout.geo.Projection(type = 'albers usa'),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)')
    else:
        gg=go.layout.Geo(
            showframe = False,
            showcoastlines = False,
            projection = go.layout.geo.Projection(
            type = 'equirectangular'))
    
    layout = go.Layout(
        geo=gg
    )
    
    sns.set()
    fig = go.Figure(data = data, layout = layout)
    
    if usa:
        pio.write_image(fig, 'choro-usa.png')
    else:
        pio.write_image(fig, 'choro.png')

graph()
graph(True)






























"""
From the file containing records of all posts, each line is like;

123456:the quick brown fox 

Extract just the GUID and print the GUID to another file

"""

fid=open('posts-master','r')
fid2=open('postids-master','w')

lines=fid.read().split('\n')

for line in lines:
    # check if it is a valid line then print
    if line[:1] == '2':
        fid2.write(line[:7]+'\n')

fid2.close()
fid.close()
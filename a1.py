#https://towardsdatascience.com/build-your-own-whatsapp-chat-analyzer-9590acca9014
import re 
import pandas as pd 
import matplotlib.pyplot as plot 

def starts_with_Date(s) : 
    pattern = r"^([0-9][0-9]|3([0-1]))(\/)((0[1-9])|(1[0-2]))(\/)([0-9][0-9]|\d{4}),\s(([0-9][0-9])|([0-9])):(([0-9][0-9])|([0-9]))\s[ap]m\s-"
    result = re.match(pattern , s)
    # print(result)
    if result : 
        return True 
    return False 

def starts_with_author(s) :
    # print(s) 
    pattern = r"([\w]+\s[\w]+):"
    result1 = re.findall(pattern , s)
    pattern = r"([\w]+):"
    result2 = re.findall(pattern , s)
    # print(result1 , result2)
    result3 = result1 + result2
    # print(result3)
    if result3 : 
        return True 
    return False

def getData_point(line) : 
    splitLine = line.split(' - ')
    datetime = splitLine[0] ; 
    date , time = datetime.split(', ')
    message = ' '.join(splitLine[1:])
    # print(message)

    if starts_with_author(message) : 
        splitMsg = message.split(": ")
        # print(splitMsg)
        author = splitMsg[0]
        message = ' '.join(splitMsg[1:])
        # print(author)
        # print(message)
    else :
        author = None 
        # print("Found nothing")
    # print(message)
    return date , time , author , message 


parsedData = [] 
with open('../chat.txt' ,'r', encoding = 'utf-8') as fp : 
    messagebuffer = [] 
    date , time , author = None , None , None 

    while True : 
        line = fp.readline()
        if not line : 
            break 
        line = line.strip() 
        if starts_with_Date(line) : 
            if len(messagebuffer) > 0 : 
                parsedData.append([date , time , author , ' '.join(messagebuffer)])
            messagebuffer.clear()
            date , time , author , message = getData_point(line)
            messagebuffer.append(message)
        else : 
            messagebuffer.append(line)


df = pd.DataFrame(parsedData ,columns=['Date','Time','Author','Message'])

desc = df.describe()
print(desc)

author_value_counts = df['Author'].value_counts()
print(author_value_counts)

top_5_author_value_counts = author_value_counts.head(5)
top_5_author_value_counts.plot.barh(x = "Authors" , y = "Message_count" , title = "Top 5 authors in sharma family")
plot.show(block = True)

media = df[df['Message'] == '<Media omitted>']
media_count = media['Author'].value_counts()
print(media_count)
top_5_media = media_count.head(5)
top_5_media.plot.barh(x = "Authors" , y = "Media_count" , title = "Top 5 media senders in sharma family")
plot.show(block = True)

null_authors_df = df[df['Author'].isnull()]
newdf = df.drop(null_authors_df.index)
newdf = newdf.drop(media.index)

newdf['Letter_count'] = newdf['Message'].apply(lambda s : len(s))
newdf['Word_count'] = newdf['Message'].apply(lambda s : len(s.split(" ")))
print(newdf.head(20))

some_cols = ['Letter_count' , 'Word_count']
desc = newdf[some_cols].describe()
print(desc)
total_words = newdf['Word_count'].sum()
letter_words = newdf['Letter_count'].sum()
print(total_words)
print(letter_words)

word_count = newdf[['Author' , 'Word_count']].groupby('Author').sum()
sort_word_count = word_count.sort_values('Word_count' , ascending = False)
top_5_word = sort_word_count.head(5)
top_5_word.plot.bar()
plot.show()

newdf['Date'].value_counts().head(10).plot.barh()
plot.xlabel("number of messages")
plot.ylabel("Authors")
plot.show()

newdf['Time'].value_counts().head(10).plot.barh()
plot.xlabel("Number of massage")
plot.ylabel("TIME")
plot.show()

month_map = {
    '01' : "January" , 
    '02' : "February" , 
    '03' : "March" , 
    '04' : "April" , 
    '05' : "May" , 
    '06' : "June" , 
    '07' : "July" , 
    '08' : "August" , 
    '09' : "September" , 
    '10' : "October" , 
    '11' : "November" , 
    '12' : "December" , 
}
newdf['Month'] = newdf['Date'].apply(lambda s : month_map[s.split('/')[1]])
print(newdf['Month'].describe())

newdf['Month'].value_counts().plot.barh()
plot.xlabel("number of message")
plot.ylabel("Months")
plot.show()






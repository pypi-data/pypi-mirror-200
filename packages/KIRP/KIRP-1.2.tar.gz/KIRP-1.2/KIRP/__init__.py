def KIRP1():
    print("""
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download("stopwords")
nltk.download("punkt")
data = "This is a sample sentence, showing off the stop words filteration"
print(data)
stopwords1 = set(stopwords.words('English'))
print('list of stopwords are: ')
print(stopwords1)
words = word_tokenize(data)
wordsfiltered = []
for w in words:
    if w not in stopwords1:
        wordsfiltered.append(w)
print('Words which are not stopwords in a given string are: ')
print(wordsfiltered)

    
    """)

def KIRP2():
    print("""
def iterative_levenshtein(s,t):
    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]

    cnt = 0
    for i in range(1, rows):
        cnt = cnt + 1
        dist[i][0] = cnt

    cnt = 0
    for i in range(1, cols):
        cnt = cnt + 1
        dist[0][i] = cnt

    for row in range(1, rows):
        for col in range(1, cols):
            if(s[row - 1] == t[col - 1]):
                dist[row][col] = dist[row - 1][col - 1]
            else:
                dist[row][col] = min(dist[row - 1][col] + 1, dist[row][col - 1] + 1, dist[row - 1][col - 1] + 1)

    for r in range(rows):
        print(dist[r])
    return dist[row][col]

Str1 = input("Enter First String: ")
Str2 = input("Enter Second String: ")
print("Distance is ", iterative_levenshtein(Str1, Str2))
    
    """)

def KIRP3():
    print(""" 
import requests
from bs4 import BeautifulSoup
def web(page, url):
    if(page > 0):
        print("The Links are: ")
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")

        for link in s.findAll('a'):
            result = link.get("href")
            print(result)

web(1, "https://www.facebook.com")  
    
    """)

def KIRP4():
    print(""" 
plays = {"Anthony and Cleopatra":"Anthony is there, Brutus is Caeser is with Cleopatra mercy worser.","Julius Caeser":"Anthiny is there, Brutus is Caeser is but Calpurnia is.","The Tempest":"mercy worser","Hamlet":"Caeser and Brutus are present with mercy and worser","Othello":"Caeser is present with mercy and worser","Macbeth":"Anthony is there, Caeser, mercy."}
words = ["Anthony","Brutus","Caeser","Calpurnia","Cleopatra","mercy","worser"]

vector_matrix = [[0 for i in range(len(plays))] for j in range(len(words))]
text_list = list((plays.values()))

for i in range(len(words)):
    for j in range(len(text_list)):
        if words[i] in text_list[j]:
            vector_matrix[i][j] = 1
        else:
            vector_matrix[i][j] = 0

for i in vector_matrix:
    print(i)

    string_list = []
    for vector in vector_matrix:
        mystring = ""

        for digit in vector:
            mystring += str(digit)
        string_list.append(int(mystring, 2))

print(string_list)
print("The output is ", bin(string_list[0] &string_list[1] &string_list[2] &string_list[3]).replace("ob", ""))

    
    """)

def KIRP5():
    print("""
import  pandas as pd
from sklearn.feature_extraction.text  import CountVectorizer
docs=['why hello there','omg hello pony','she went there? omg']

v=CountVectorizer() #count all docs
x=v.fit_transform(docs) #transform in columnformat

df=pd.DataFrame(x.toarray(),columns=v.get_feature_names_out())
#array rowformat and display in matrix
print(df)

       """)
    
def KIRP6():
    print("""
from nltk.tokenize import word_tokenize
import numpy as np
import nltk
nltk.download('punkt')

def process(file):
    raw=open (file).read()
    tokens=word_tokenize(raw)
    count = 0
    count=nltk.defaultdict(int)
    for word in tokens:
        count[word]+=1
    print('file: ', file , count)
    return count;

def cos_sim(a,b):
    dot_product=np.dot(a,b)
    norm_a=np.linalg.norm(a)
    print('norm_a: ',norm_a)
    norm_b=np.linalg.norm(b)
    print('norm_b: ',norm_b)
    return dot_product/(norm_a * norm_b)

def getSimilarity(dict1,dict2):
    all_words_list=[]
    for key in dict1:
        all_words_list.append(key)
    for key in dict2:
        all_words_list.append(key)
    print('all_wors_list: ',all_words_list)
    all_words_list_size=len(all_words_list)

    v1=np.zeros(all_words_list_size,dtype=np.int)
    v2=np.zeros(all_words_list_size,dtype=np.int)
    i=0
    for  (key) in all_words_list:
        v1[i]=dict1.get(key,0)
        print('v1',v1)
        v2[i]=dict2.get(key,0)
        print('v2',v2)
        i=i+1
    return cos_sim(v1,v2)

if __name__ == '__main__':
    dict1=process("D:/IR/t1.txt")
    dict2=process("D:/IR/t2.txt")
    print("Similarity between two text documents",getSimilarity(dict1,dict2))

       """)
    
def KIRP7():
    print(""" 
import tweepy 
from tkinter import * 
from time import sleep
from datetime import datetime
from textblob import TextBlob 
import matplotlib.pyplot as plt 

consumer_key = 'AU8Ym4iZoM3deqTn3i6AWDRme' 
consumer_secret = 'h1aT9QPHdtWvjLbPx57di9hnspYFnFT34eG6kTylbC5Tv2C0Nm'
access_token = '700594962556014592-9NIgRPd60o4YySxlrgQda4uzO97iozW'
access_token_secret = 'rPaSPPgEWQZpVS0zVjePj8dhlvkBmvbHZQ0FvswEYygXh'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
#user = api.me()   # Works on tweeter version below 4.0
user= api.verify_credentials()
#print (user.name)
#GUI
root = Tk()

label1 = Label(root, text="Search")
E1 = Entry(root, bd =5)

label2 = Label(root, text="Sample Size")
E2 = Entry(root, bd =5)

def getE1():
    return E1.get()

def getE2():
    return E2.get()

def getData():
    getE1()
    keyword = getE1()

    getE2()
    numberOfTweets = getE2()
    numberOfTweets = int(numberOfTweets)

    #Where the tweets are stored to be plotted
    polarity_list = []
    numbers_list = []
    number = 1

    positive=0
    negative=0
    neutral=0
    
    for tweet in tweepy.Cursor(api.search, keyword, lang="en").items(numberOfTweets):   #Works on tweeter version below 4.0
    #for tweet in tweepy.Cursor(api.search_tweets, keyword, lang="en").items(numberOfTweets):
        try:
            analysis = TextBlob(tweet.text)
            analysis = analysis.sentiment
            polarity = analysis.polarity
            if polarity>0:
                positive+=1
            elif polarity <0:
                negative+=1
            else:
                neutral+=1
            polarity_list.append(polarity)
            numbers_list.append(number)
            number = number + 1

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break

    print(polarity)
    print(numbers_list)
    print(polarity_list)
    print(f'Amount of positive tweets : {positive}')
    print(f'Amount of negative tweets : {negative}')
    print(f'Amount of neutral tweets : {neutral}')
    
    #Plotting
    axes = plt.gca()
    axes.set_ylim([-1, 1])

    plt.scatter(numbers_list, polarity_list)

    averagePolarity = (sum(polarity_list))/(len(polarity_list))
    averagePolarity = "{0:.0f}%".format(averagePolarity * 100)
    time  = datetime.now().strftime("At: %H:%M\nOn: %m-%d-%y")

    plt.text(1, 0.92, "Average Sentiment:  " + str(averagePolarity) + "\n" + time, fontsize=12,
             bbox = dict(facecolor='none', edgecolor='black', boxstyle='square, pad = 1'))

    plt.title("Sentiment of " + keyword + " on Twitter")
    plt.xlabel("Number of Tweets")
    plt.ylabel("Sentiment")
    plt.show()

submit = Button(root, text ="Submit", command = getData)

label1.pack()
E1.pack()
label2.pack()
E2.pack()
submit.pack(side =BOTTOM)

root.mainloop()

    """)

def KIRP8():
    print(""" 
def pagerank():
           print('Enter the matrix')
           array_input = []
           for x in range(3):
               array_input.append([float(y) for y in input().split()])
           print(array_input)

           # initialize the final matrix
           finalmat=[1,1,1]

           # Enter the number of iterations
           itr=int(input('Enter the number of iteraions'))

           #Execute code for number of iterations mentioned.
           for loop in range(itr):
                      print('Iteration :', loop+1)
                      cnt=0
                      # Traverse through rows of matrix
                      for row in range(len(array_input)):
                                 sum=0
                                 # Traverse through columns of matrix
                                 for col in range(len(array_input[row])):
                                            #Checks the incoming edges from the web pages
                                            if (array_input[col][row] == 1):
                                                       #Checking the number of out links of the web page
                                                       for i in range(3):
                                                                  if(array_input[col][i]==1):
                                                                             cnt=cnt+1                                            
                                                       sum+=finalmat[col]/cnt
                                            cnt=0
                                 #Updating the final
                                 finalmat[row]=0.5+(0.5*sum)
                                 print(finalmat[row],' ')


pagerank()

    """)

def KIRP9():
    print(""" 
Text="MapReduce is a processing technique and a program model for distributed computing based on java."
from collections import OrderedDict
for char in '_.,\n':
    Text = Text.replace(char,'.')
    Text = Text.lower()
    word_list = Text.split()

from collections import Counter
Counter(word_list).most_common()
d = {}
for word in word_list:
    d[word] = d.get(word,0)+1
    d = OrderedDict(sorted(d.items()))
print(d)

    
    """)

def KIRP10():
    print("""
def iterative_levenshtein(s, t):

    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]

    cnt=0
    for i in range(1, rows):
           cnt=cnt+1
           dist[i][0] = cnt

    cnt=0
    for i in range(1, cols):
           cnt=cnt+1
           dist[0][i] = cnt
	
    for row in range(1, rows):
        for col in range(1, cols):
            if s[row-1] == t[col-1]:
                dist[row][col] = dist[row-1][col-1] 
            else:
                dist[row][col] = min(dist[row-1][col] + 1,      
                                 dist[row][col-1] + 1, 
                                 dist[row-1][col-1] + 1)

            
    for r in range(rows):
        print(dist[r])


    return dist[row][col]

s1=input("Enter String  1 : ")
s2=input("Enter String  2 : ")
print("Edit distance between ",s1," and ",s2," is ",iterative_levenshtein(s1, s2))
      
        """)



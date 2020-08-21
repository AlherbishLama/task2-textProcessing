import re
from nltk.tokenize import RegexpTokenizer
from mosestokenizer import *
import csv
import itertools

# tweets_file = open('files/Task_2_Tweets.txt', 'r')

hashtags_list = []
characters = ['!', '@', '$', '%', '^', '&', '*', '/', '{', '}', '[', ']',
              '\'', '+', '=', '>', '<', '?', '|', '~', ':', ';', ',', '.',
              '-', '(', ')' , '\"' , '\\', '،', '…', '‐']

clean_tweets = []
tweets_date = []
tweets_ID = []

tweets_file = open('files/Task_2_Tweets.txt', 'r')

with tweets_file as f:
    lines = f.readlines()
    for line in lines:
        # Extract tweet text
        text_line = line[42:]


        # Remove @usernames from tweet text
        text = re.sub(r'@\S+', '', text_line)

        # Remove URLs
        text2 = re.sub(r'http\S+', '', text)

        # Extract hashtags & add them to hashtags_list
        hashtags_list.append(re.findall(r"#(\w+)", text2))

        # Replace multi Spaces with one space
        text2 = re.sub(' +', ' ', text2)
        # Replace multi Tabs with one space
        text2 = re.sub('\t +', ' ', text2)
        # Replace multi Newlines with one space
        text2 = re.sub('\n +', ' ', text2)

        # Remove characters
        for char in characters:
            text2 = text2.replace(char, "")

        # Remove duplicated characters
        text2 = ''.join(char for char, _ in itertools.groupby(text2))

        # tokenize
        tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
        tokenized_tweet = tokenizer.tokenize(text2)

        # Remove Digits
        tokenized_tweet = [''.join(x for x in i if not re.search(r'[0-9٠١٢٣٤٥٦٧٨٩]',
                                                      x))for i in tokenized_tweet]
        # Remove English words
        tokenized_tweet = [''.join(x for x in i if not re.search(r'[a-zA-Z]',
                                                 x)) for i in tokenized_tweet]

        # Untokenize
        with MosesDetokenizer() as detokenize:
            clean_tweet = detokenize(tokenized_tweet)
            clean_tweets.append(clean_tweet)

        # tweet Date
        day = line[8:10]
        month = line[4:7]
        year = line[26:30]
        tweet_date = "{}-{}-{}".format(year, month, day)
        tweets_date.append(tweet_date)

        # tweet ID
        tweet_ID = line[31:42]
        tweets_ID.append(tweet_ID)

tweets_file.close()

# Cleaning the hashtags_list and clean_tweets by removing empty strings
hashtags_list = list(filter(None, hashtags_list))
clean_tweets = list(filter(None, clean_tweets))



# method to remove duplicated hashtags from hashtags_list and flatten hashtags_list
def flatten(listt):
    return {x for y in [[x] if not isinstance(x, list) else flatten(x) for x in listt] for x in y}

# Create hashtags.text file and write all the hashtags then close the file
hashtags_file = open('files/hashtags.txt', 'w')
hashtags_list = list(flatten(hashtags_list))
for hashtag in hashtags_list:
    hashtags_file.write(hashtag+'\n')
hashtags_file.close()

# Create final.csv file and write all the tweets data then close the file
final_file = open('files/final.csv', 'w')
wr = csv.writer(final_file)
wr.writerow(['tweetID', 'tweet Date', 'clean_tweet'])
for id, date, text in zip(tweets_ID, tweets_date, clean_tweets):
    wr.writerow([id, date, text])
final_file.close()

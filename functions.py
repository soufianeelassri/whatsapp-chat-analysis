from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def basic_stats(df):

    total_messages = df.shape[0]
    total_words = []
    for message in df['message']:
        total_words.extend(message.split())
    media_shared = df['message'].str.contains('<Media omitted>').sum()
    links_shared = df['message'].apply(lambda x: extract.find_urls(x)).explode().dropna().unique()
    return total_messages, len(total_words), media_shared, len(links_shared)

def monthly_timeline(df):

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(df):

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def most_busy_day(df):

    timeline = df.groupby('day_name').count()['message'].reset_index()
    custom_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    timeline['day_name'] = pd.Categorical(timeline['day_name'], categories=custom_order, ordered=True)
    timeline = timeline.sort_values(by='day_name')
    return timeline

def must_busy_month(df):
    timeline = df.groupby('month').count()['message'].reset_index()
    timeline = timeline.sort_values(by='month', ascending=False)
    return timeline

def remove_emojis(text):
    return emoji.demojize(text)

def most_common_words(df):

    f = open('stop_words.txt','r', encoding='utf-8')
    stop_words = f.read()
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            cleaned_word = remove_emojis(word)
            if not cleaned_word.startswith(':') and not cleaned_word.endswith(':'):
                if cleaned_word not in stop_words:
                    words.append(cleaned_word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
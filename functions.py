from urlextract import URLExtract
import pandas as pd

extract = URLExtract()

def basic_stats(df):

    # fetch the number of messages
    total_messages = df.shape[0]

    # fetch the total number of words
    total_words = []
    for message in df['message']:
        total_words.extend(message.split())

    # fetch number of media messages
    media_shared = df['message'].str.contains('<Media omitted>').sum()

    # fetch number of links shared
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

    timeline = df.groupby('only_date').count()['message'].reset_index()

    return timeline

def most_busy_days(df):

    timeline = df.groupby('day_name').count()['message'].reset_index()

    custom_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    timeline['day_name'] = pd.Categorical(timeline['day_name'], categories=custom_order, ordered=True)
    timeline = timeline.sort_values(by='day_name')

    return timeline
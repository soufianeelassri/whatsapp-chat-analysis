from urlextract import URLExtract

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
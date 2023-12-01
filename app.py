from flask import Flask, render_template, request
import preprocessing
import helper

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def analyze():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        bytes_data = uploaded_file.read()
        data = bytes_data.decode("utf-8")
        df = preprocessing.preprocessing(data)

        #fetch unique users
        user_list = df['user'].unique().tolist()
        user_list.remove('group notification')
        user_list.sort()
        
        num_messages, num_words, num_media_messages, num_links = helper.fetch_stats(df)

        return render_template(
                'results.html',
                num_messages=num_messages,
                num_words=num_words,
                num_media_messages=num_media_messages,
                num_links=num_links
            )

if __name__ == '__main__':
    app.run(debug=True)

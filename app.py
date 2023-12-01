from flask import Flask, render_template, request
import preprocessing
import functions

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
        
        total_messages, total_words, media_shared, link_shared = functions.basic_stats(df)

        return render_template(
                'results.html',
                total_messages = total_messages,
                total_words = total_words,
                media_shared = media_shared,
                link_shared = link_shared
            )

if __name__ == '__main__':
    app.run(debug=True)

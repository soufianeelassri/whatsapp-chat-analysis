from flask import Flask, render_template, request
import preprocessing
import functions
import matplotlib.pyplot as plt
from wordcloud import WordCloud


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

        monthly_timeline = functions.monthly_timeline(df)
        must_busy_month = functions.must_busy_month(df)
        daily_timeline = functions.daily_timeline(df)
        most_busy_day = functions.most_busy_day(df)
        most_common_words = functions.most_common_words(df)

        fig1, ax1 = plt.subplots(figsize=(10, 4))
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        fig4, ax4 = plt.subplots(figsize=(10, 4))
        fig5, ax5 = plt.subplots(figsize=(10, 4))

        ax1.plot(monthly_timeline['time'], monthly_timeline['message'], color='green')
        ax1.set_title('Monthly Timeline')

        plot_filename1 = 'static/monthly_timeline_plot.png'
        ax1.figure.savefig(plot_filename1)
        plt.close(fig1)

        ax2.bar(must_busy_month['month'], must_busy_month['message'], color='green')
        ax2.set_title('Most Busy Month')

        plot_filename2 = 'static/most_busy_month_plot.png'
        ax2.figure.savefig(plot_filename2)
        plt.close(fig2)

        ax3.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        ax3.set_title('Daily Timeline')

        plot_filename3 = 'static/daily_timeline_plot.png'
        ax3.figure.savefig(plot_filename3)
        plt.close(fig3)

        ax4.bar(most_busy_day['day_name'], most_busy_day['message'], color='green')
        ax4.set_title('Most Busy Day')

        plot_filename4 = 'static/most_busy_day_plot.png'
        ax4.figure.savefig(plot_filename4)
        plt.close(fig4)

        wordcloud = WordCloud(width=800, height=400, background_color='lightyellow').generate_from_frequencies(dict(zip(most_common_words[0], most_common_words[1])))
        ax5.imshow(wordcloud, interpolation='bilinear')
        ax5.axis('off')
        ax5.set_title('Most Common Words Plot')

        plot_filename5 = 'static/most_common_words_plot.png'
        ax5.figure.savefig(plot_filename5)
        plt.close(fig5)

        return render_template(
                'results.html',
                total_messages = total_messages,
                total_words = total_words,
                media_shared = media_shared,
                link_shared = link_shared,

                plot_filename1 = plot_filename1,
                plot_filename2 = plot_filename2,
                plot_filename3 = plot_filename3,
                plot_filename4 = plot_filename4,
                plot_filename5 = plot_filename5
            )

if __name__ == '__main__':
    app.run(debug=True)

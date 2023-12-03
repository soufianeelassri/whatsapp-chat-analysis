from flask import Flask, render_template, request
import preprocessing
import functions
import matplotlib.pyplot as plt

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
        daily_timeline = functions.daily_timeline(df)
        most_busy_days = functions.most_busy_days(df)

        fig1, ax1 = plt.subplots(figsize=(10, 4))
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        fig4, ax4 = plt.subplots(figsize=(10, 4))

        ax1.plot(monthly_timeline['time'], monthly_timeline['message'], color='green')
        ax1.set_title('Monthly Timeline')
        ax1.set_ylabel('Message')

        plot_filename1 = 'static/monthly_timeline_plot.png'
        ax1.figure.savefig(plot_filename1)
        plt.close(fig1)

        ax2.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        ax2.set_title('Daily Timeline')
        ax2.set_ylabel('Message')

        plot_filename2 = 'static/daily_timeline_plot.png'
        ax2.figure.savefig(plot_filename2)
        plt.close(fig2)

        ax3.bar(most_busy_days['day_name'], most_busy_days['message'], color='green')
        ax3.set_title('Most Busy Days')
        ax3.set_ylabel('Message')

        plot_filename3 = 'static/most_busy_days_plot.png'
        ax3.figure.savefig(plot_filename3)
        plt.close(fig3)

        ax4.bar(monthly_timeline['time'], monthly_timeline['message'], color='green')
        ax4.set_title('Most Busy Months')
        ax4.set_ylabel('Message')

        plot_filename4 = 'static/most_busy_months_plot.png'
        ax4.figure.savefig(plot_filename4)
        plt.close(fig4)

        return render_template(
                'results.html',
                total_messages = total_messages,
                total_words = total_words,
                media_shared = media_shared,
                link_shared = link_shared,

                plot_filename1 = plot_filename1,
                plot_filename2 = plot_filename2,
                plot_filename3 = plot_filename3,
                plot_filename4 = plot_filename4
            )

if __name__ == '__main__':
    app.run(debug=True)

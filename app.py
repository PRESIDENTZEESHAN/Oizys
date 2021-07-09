import pandas as pd
import snscrape.modules.twitter as sntwitter
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)


class user_details(db.Model):  # table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    profession = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<user_details %r>' % self.id


class cesd_questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    pt_1 = db.Column(db.Integer, nullable=False)
    pt_2 = db.Column(db.Integer, nullable=False)
    pt_3 = db.Column(db.Integer, nullable=False)
    pt_4 = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<cesd_questions %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == 'GET':
        return render_template('details.html')
    if request.method == 'POST':
        user_name = request.form['fullName']
        user_age = request.form['Age']
        user_sex = request.form['Sex']
        user_country = request.form['Country']
        user_profession = request.form['Profession']
        u_details = user_details(name=user_name, age=user_age, sex=user_sex,
                                 country=user_country, profession=user_profession)

        try:
            db.session.add(u_details)
            db.session.commit()
            return redirect('/cesd')
        except:
            return 'not entered in the table'

result =0
@app.route('/cesd', methods=['GET', 'POST'])
def cesd_form():
    if request.method == 'GET':
        data = cesd_questions.query.all()
        return render_template('cesd.html', data=data)
    if request.method == 'POST':
        score = []
        for i in range(0, 20):
            temp = int(request.form[str(i)])
            score.append(temp)  # 0-19
        res = sum(score)
        result = res
        return render_template('testresults.html',res=res) #redirect isn't used here because we're passing information from one page to another
        #return redirect(url_for('test_results', res=res))


@app.route('/results', methods=['GET', 'POST'])
def test_results():
    if request.method=='GET':
        return render_template('testresults.html')
    
    if request.method=='POST': #take username and scrape tweets
        #taking username
        username = request.form['twitter-username']

        #list to store tweet data
        tweets_list1 = []

        # Using TwitterSearchScraper to scrape data and append tweets to list
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:jack').get_items()):
            if i > 100:  # add date limit here
                break
            tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

        # Creating a dataframe from the tweets list above
        tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
        #now you have to call the function that runs the model
        return tweets_list1
'''@app.route('/analysis')
def analyse_tweets():
    
    # Creating list to append tweet data to
    tweets_list1 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:jack').get_items()):
        if i > 100: #add date limit here
            break
        tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

    # Creating a dataframe from the tweets list above
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username']) '''



if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask
from flask_bootstrap import Bootstrap
from front_end import *

app = Flask(__name__)

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # return render_template('my-form.html')
    return render_template('/home.html') #, title='Welcome', username=name)


@app.route('/job-title-results', methods=['POST'])
def job_title_results():
    query_title = request.form['query']
    results = calculate_job_title_results(query_title)
    return render_template('/results.html', query=query_title, results=results)

@app.route('/job-title-results-test')
def job_title_results_test():

    return render_template('/results.html', query="test", results=[["Skill1","Skill2"],["Attribute1","Attribute2"]])


@app.route('/job-url-results', methods=['POST'])
def job_url_results():
    query_title = request.form['query']
    # results = calculate_job_url_results(query_title)
    return render_template('/results.html', query=query, results=results)


def calculate_job_title_results(query):
    data = scrape_data(query)
    processed_data = process_data(data)
    tagged_data = tag_data(processed_data)
    print(tagged_data)
    return sort_results(tagged_data)

def calculate_job_url_results(query):

    return

if __name__ == '__main__':
    Bootstrap(app)
    app.run()
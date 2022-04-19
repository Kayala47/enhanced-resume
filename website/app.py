from flask import Flask
from flask_bootstrap import Bootstrap
from front_end import *
import nltk
nltk.download('punkt')

app = Flask(__name__)

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # return render_template('my-form.html')
    return render_template('/home.html') #, title='Welcome', username=name)


@app.route('/job-query-results', methods=['POST'])
def job_query_results():
    job_query = request.form['query']
    print(job_query)
    #path = request.form['file']
    print(request.files['file'])
    results = calculate_job_query_results(job_query)
    return render_template('/results.html', query=job_query, results=results)

@app.route('/job-title-results', methods=['POST'])
def job_url_results():
    title_query = request.form['title']
    company_query = request.form['company']
    #path = request.form['file']
    print(request.files['file'])
    results = calculate_job_title_results(title_query, company_query)
    return render_template('/results.html', query=f"{title_query}, {company_query}", results=results)


def calculate_job_query_results(query):
    data = scrape_data(query)
    processed_data = process_data(data)
    tagged_data = tag_data(processed_data)
    print(tagged_data)
    return sort_results(tagged_data)

def calculate_job_title_results(title, company):
    data = scrape_data_single(title, company)
    processed_data = process_data(data)
    tagged_data = tag_data(processed_data)
    print(tagged_data)
    return sort_results(tagged_data)

if __name__ == '__main__':
    Bootstrap(app)
    app.run()
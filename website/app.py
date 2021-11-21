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


@app.route('/results', methods=['POST'])
def my_form_post():
    query = request.form['query']

    results = calculate_results(query)
    return render_template('/results.html', query=query, results=results)





def calculate_results(query):
    data = scrape_data(query)
    processed_data = process_data(data)
    tagged_data = tag_data(processed_data)
    print(tagged_data)
    return sort_results(tagged_data)



if __name__ == '__main__':
    Bootstrap(app)
    app.run()
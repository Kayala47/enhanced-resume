from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


import sys

def get_job_title():
    title = input('Enter a job title or job search query: ')
    return title

def scrape_data(query):
    #somehow need to specfy
    println("Scraping job listings for " + query + "...")
    scraped_data = glassdoor_scraper.scrape5(query)
    println("Scraping complete")
    return scraped_data



def tag_data(jobs_list):
    println("Tagging scraped data...")
    tagged_data_list = []
    for listing in jobs_list:
        description = listing.description
        joined_description = ". ".join(description)

    tagged_data_list = run_ner_model(joined_description)
    
    println("Tagging complete")
    return tagged_data_list


def output_results(tagged_data):
    skills_dict = {}
    attributes_dict = {}

    for data in tagged_data:
        
        value = data[0]
        tag = data[1]
        if tag == 'SKILL':
            if value in skills_dict.keys():
                skills_dict[value] += 1
            else:
                skills_dict[value] = 1
        else:
            if value in attributes_dict.keys():
                attributes_dict[value] += 1
            else:
                attributes_dict[value] = 1

    sorted_skills = sorted(skills_dict, key=skills_dict.get, reverse=True)
    sorted_attributes = sorted(attributes_dict, key=attributes_dict.get,reverse=True)

    return [sorted_skills, sorted_attributes]
    


def main():
    query = get_job_title()
    data = scrape_data(query) # JobListing[]
    tagged_data = tag_data(data)


def cli_output(sorted_skills, sorted_attributes):
    print("-----------------------------------------------------------")
    print("Here are the key skills you should have in your resume:")
    print("-----------------------------------------------------------")
    for skill in sorted_skills:
        print(skill)
    print("")
    print("-----------------------------------------------------------")
    print("Here are the key attributes you should have in your resume:")
    print("-----------------------------------------------------------")
    for attribute in sorted_attributes:
        print(attribute)
    print("-----------------------------------------------------------")


if __name__ == "__main__":
    
    outputs = output_results([["python","SKILL"],["C++","SKILL"],["python","SKILL"],["python","SKILL"],["Java","SKILL"],
    ["Java","SKILL"],["C++","SKILL"],["C++","SKILL"],["C++","SKILL"],["C++","SKILL"],["Java","SKILL"],
    ["hard-working","ATTRIBUTE"],["passionate","ATTRIBUTE"],["passionate","ATTRIBUTE"],["passionate","ATTRIBUTE"],["enthusiastic","ATTRIBUTE"]])

    cli_output(outputs[0],outputs[1])
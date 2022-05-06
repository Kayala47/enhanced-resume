from flask import Flask
import sys
import model_runner
import back_end
import pandas

sys.path.insert(0, "../data_processing")
import stopword_remover
import tokenizer


def get_job_title():
    title = input("Enter a job title or job search query: ")
    return title


def scrape_data(query):
    # somehow need to specfy
    print("Scraping job listings for " + query + "...")
    scraped_data = back_end.scrape_amount(query, 50)
    print("Scraping complete")
    return scraped_data["Job Description"].values.tolist()


def scrape_data_single(title, company):
    print(f"Scraping job listings for {title}, {company}...")
    scraped_data = back_end.scrape_single(title, company)
    print("Scraping complete")
    print(scraped_data)
    return scraped_data.split(" ")


def process_data(data):
    output = []

    for description in data:
        tokenized_data = tokenizer.tokenize(description)
        stopwords_removed = stopword_remover.remove_from(tokenized_data)
        finished = " ".join(stopwords_removed)
        output.append(finished)

    return output


def tag_data(jobs_list):
    print("Tagging scraped data...")
    tagged_data_list = model_runner.run_ner_model(jobs_list)

    print("Tagging complete")
    return tagged_data_list


def sort_results(tagged_data):
    skills_dict = {}
    attributes_dict = {}
    experience_dict = {}

    for data in tagged_data:
        for item in data:
            value = item[0]
            tag = item[1]
            if tag == "SKILL":
                if value in skills_dict.keys():
                    skills_dict[value] += 1
                else:
                    skills_dict[value] = 1
            elif tag == "ATTRIBUTE":
                if value in attributes_dict.keys():
                    attributes_dict[value] += 1
                else:
                    attributes_dict[value] = 1
            else:
                if value in experience_dict.keys():
                    experience_dict[value] += 1
                else:
                    experience_dict[value] = 1

    sorted_skills = sorted(skills_dict, key=skills_dict.get, reverse=True)
    sorted_attributes = sorted(attributes_dict, key=attributes_dict.get, reverse=True)
    sorted_experience = sorted(experience_dict, key=experience_dict.get, reverse=True)
    # print(skills_dict)
    # print(attributes_dict)
    return [sorted_skills, sorted_attributes, sorted_experience]


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


def main():
    query = get_job_title()
    data = scrape_data(query)  # JobListing[]
    processed_data = process_data(data)
    tagged_data = tag_data(processed_data)
    sorted_results = sort_results(tagged_data)
    cli_output(sorted_results[0], sorted_results[1])


if __name__ == "__main__":

    main()

    # outputs = output_results([["python","SKILL"],["C++","SKILL"],["python","SKILL"],["python","SKILL"],["Java","SKILL"],
    # ["Java","SKILL"],["C++","SKILL"],["C++","SKILL"],["C++","SKILL"],["C++","SKILL"],["Java","SKILL"],
    # ["hard-working","ATTRIBUTE"],["passionate","ATTRIBUTE"],["passionate","ATTRIBUTE"],["passionate","ATTRIBUTE"],["enthusiastic","ATTRIBUTE"]])

    # cli_output(outputs[0],outputs[1])

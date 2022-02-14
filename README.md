# enhanced-resume
Project for p-ai: creating a resume generator based on using Named Entity Recognition on web-scraped job listings to prioritize keywords on a user's resume.

## Collaborators:
- Kevin Ayala
- Evan Von Oehsen
- Aidan Wu
- Marghi Andreassi


## Workflow

### Scraping
1. Run scraper/data_collector.py, which produces lots of csv files with raw data, saving them into /output_csvs
2. Run scraper/coallescer.py, which coallesces all the previous files into one file and saves it in the root directory as final_output.csv

### Data Processing
1. Run data_processing/main.py with the path to the final_output.csv file we received in the last step. This will produce an identical csv with columns for stopwords removed and tokenized text. The result will be in data_processing/processed_output_csvs

### Tagging
1. we run tagging/assign_tags.py with the assignees flag followed by names of all active collaborators and a num flag of 50. That gets us 50 assigned listings per week. By default, it will take examples from the file we got in the last step.
2. each collaborator is assigned a file by the previous process. We normally post those in the discord for everyone to complete
3. completed files are posted back to the discord by all collaborators. those are compiled in the tagging/hand_tagged folder
4. from there, we run tagging/combine_tags.py to combine all the tagged files together, then tagging/split_data.py to categorize it into train and test datasets

### Model
1. Once data processing is done, we run ner_model.py. It overwrites ner/spacy_model with a newly trained model
2. You can test the current model by running model_validatory.py. It pulls the model saved at ner/spacy_model and tests it against data from ner/test_data.json

### Front End
To access and interact with the front-end code, follow below steps:
1. In a command line window within the main project directory, enter ``cd website``.
2. Start the Flask website by entering ``python app.py``. Within the CLI instructional output, there should be a line which says ```Running on http://127.0.0.1:5000/```. 
3. Copy the URL portion of the message, and paste it into a browser while the process is still running. The home page should now appear.
4. Terminate the process anytime with the ```CTRL+C``` keys, or as specified in the initial CLI instructional output.

## TODO
- fix scraper and model (periodic updates required)
- train model on un-tokenized data
- get it to modify a word doc

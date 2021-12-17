# enhanced-resume
Project for p-ai: creating a resume generator based on using Named Entity Recognition on web-scraped job listings to prioritize keywords on a user's resume.

## Collaborators:
- Kevin Ayala
- Evan Von Oehsen
- Marghi Andreassi
- Alida Schefers
- Aidan Wu


## Workflow

### Tagging
1. we run tagging/assign_tags.py with the arguments flag followed by names of all active collaborators and a num flag of 50. That gets us 50 assigned listings per week
2. each collaborator is assigned a file by the previous process. We normally post those in the discord for everyone to complete
3. completed files are posted back to the discord by all collaborators. those are compiled in the tagging/hand_tagged folder
4. from there, we run tagging/combine_tags.py to combine all the tagged files together, then tagging/split_data.py to categorize it into train and test datasets

### Model
1. Once data processing is done, we run ner_model.py. It overwrites ner/spacy_model with a newly trained model
2. You can test the current model by running model_validatory.py. It pulls the model saved at ner/spacy_model and tests it against data from ner/test_data.json

### Front End


## TODO
- fix scraper and model (periodic updates required)
- train model on un-tokenized data
- get it to modify a word doc

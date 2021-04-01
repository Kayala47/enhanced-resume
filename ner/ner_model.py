import numpy as np
import pandas as pd
import spacy
import re

nlp = spacy.load("en_core_web_sm")

#import data
df = pd.read_csv('../scraper/output.csv')

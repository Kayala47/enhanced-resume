import re
from glassdoor_selenium import take_one

f = open('outfile.txt', 'w')

skills = ["python", "java", "react", "SQL", "MERN", "C++", "C",
"rust", "Haskell", "Ruby", "Leadership", "English"]

f.write(" ".join(skills))
f.write("\n")

job = take_one()

desc = str(job)
desc = desc.replace("\\n", '')
desc = desc.replace(".", ' ')
desc = desc.replace(",", ' ')
desc = desc.replace("  ", ' ') #replace two spaces with one
print(desc)



f.write(desc)
f.close()
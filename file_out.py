import re
from glassdoor_selenium import take_one

f = open('outfile.txt', 'w')

job = take_one()

desc = str(job)
desc = desc.replace("\\n", '')
desc = desc.replace(".", ' ')
desc = desc.replace(",", ' ')
desc = desc.replace("  ", ' ') #replace two spaces with one
print(desc)

f.write(desc)
f.close()
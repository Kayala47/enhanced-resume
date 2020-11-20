#take in a dictionary of skills and their values (prob how many
# times it got repeated). Also take a number of skills that can fit.
#assuming a non-column resume (recommended by CDO), this should 
# be number of lines dedicated to skills
import random 


VALUES = {"python": (3, 1), "javascript": (2, 1), "react": (4, 1), 
"public speaking": (2, 1), "html": (1, 1), "rust": (1000, 1), "ruby": (5, 1), 
"leadership": (4, 1), "full stack": (13, 1), "SQL": (10, 1)}

def main():
    lines_available = random.randint(1, 10)

    print("You should include the following skills: \n")
    print(single_weight(VALUES, lines_available))

class Skill:
    def __init__(self, string, value, weight):
        self.value = value
        self.string = string 
        self.weight = weight

def objectify(dict):
    new_list = []
    for k in dict.keys():
        val, wt = dict.get(k)
        new_obj = Skill(k, val, wt)
        new_list.append(new_obj)
    return new_list 


def single_weight(skills, num_lines):
    #returns a list of the skills you should include
    #we assume the weight of each skill is the same fo rnow
    #if we want to get fancy later, with columns, we can
    #say something like 'phrases shorter than x letters take
    #up 1 column, otherwise they take 2'

    #in this case, we sort by values, and go until we can't 
    #fit any more

    skill_list = objectify(skills)

    skill_list.sort(key=lambda x:x.value, reverse=True)

    if num_lines >= len(skills):
        ret = [x.string for x in skill_list] 
    else:
        ret = []
        for i in range(0, num_lines):
            ret.append(skill_list[i].string)

    return ret


    



if __name__ == "__main__":
    main()
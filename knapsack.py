#take in a dictionary of skills and their values (prob how many
# times it got repeated). Also take a number of skills that can fit.
#assuming a non-column resume (recommended by CDO), this should 
# be number of lines dedicated to skills
import random 


VALUES = {"python": (3, 1), "javascript": (2, 1), "react": (4, 1), 
"public speaking": (2, 1), "html": (1, 1), "rust": (1000, 1), "ruby": (5, 1), 
"leadership": (4, 1), "full stack": (13, 1), "SQL": (10, 1)}

def main(skill_file):
    lines_available = random.randint(1, 10)
    skill_dict = {}
    f = open(skill_file, 'r') #read in these values and make a dict
    for line in f:
        # line = f.readline()
        parts = line.split(',')
        # print(line)
        skill_dict[parts[0]] = (int(parts[1]), int(parts[2]))


    skill_list = objectify(skill_dict)
    n = len(skill_list)

    dp_table = [[-1 for i in range(lines_available + 1)] for j in range(n + 1)] 
    
    # print("If there were multiple weights, the correct answer is:")
    print(multi_weights(skill_list, lines_available, dp_table, n))


class Skill:
    def __init__(self, string, value, weight):
        self.value = value
        self.string = string 
        self.weight = weight
    def __repr__(self):
        #this is for better printing
        return str(self.string) + ': weight = ' + str(self.weight) + ", value = " + str(self.value) 

def objectify(dict):
    new_list = []
    for k in dict.keys():
        wt, val = dict.get(k)
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

def multi_weights(skills, space_available, dp, n_skills):
    if n_skills == 0 or space_available == 0:
        return (0, []) #no skills left to check or space to 
        #place any of them
    
    if dp[n_skills][space_available] != -1:
        return dp[n_skills][space_available] # we have an answer!

    #now we choose the best option: either taking or skipping
    #the current choice
    if skills[n_skills-1].weight <= space_available:
        #let's consider if its worth adding
        
        #in this case, we select it, so subtract that element from the list as well 
        #as subtract the space used
        add_choice = multi_weights(skills, space_available - skills[n_skills-1].weight, dp, n_skills - 1)
        add_val, add_list = add_choice

        #in this case, we just skip the case, so ignore it in the list
        skip_choice = multi_weights(skills, space_available, dp, n_skills - 1)
        skip_val, skip_list = skip_choice

        if add_val + skills[n_skills -1].value >= skip_val:
            add_list.append(skills[n_skills-1])
            dp[n_skills][space_available] = (skills[n_skills - 1].value + add_val, add_list)
        else:
            dp[n_skills][space_available] = (skip_val, skip_list)

        return dp[n_skills][space_available]

    elif skills[n_skills-1].weight > space_available:
        #can't use this one, so only return the skip
        dp[n_skills][space_available] = multi_weights(skills, space_available, dp, n_skills -1)
        return dp[n_skills][space_available]



if __name__ == "__main__":
    main("weights.txt")
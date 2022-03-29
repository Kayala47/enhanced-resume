def sort_skills(job_skills, resume_skills):
    for js in reversed(job_skills):
        for i,rs in enumerate(resume_skills):
            if js.upper() == rs.upper():
                resume_skills.insert(0,resume_skills.pop(i))

    return resume_skills

js = ['JaVa', 'ruby', 'python']
rs = ['js', 'react', 'java', 'python', 'swift'] 

print(sort_skills(js,rs))
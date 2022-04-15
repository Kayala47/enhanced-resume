import argparse
import docx


def sort_skills(job_skills, resume_skills):
    for js in reversed(job_skills):
        for i, rs in enumerate(resume_skills):
            if js.upper() == rs.upper():
                resume_skills.insert(0, resume_skills.pop(i))

    return resume_skills


def coallesce_skills(resume_skills):
    paragraphs = []
    doc = docx.Document()
    for s in resume_skills:
        skills_list = s.split(",")
        skills = ', '.join(skills_list)
        p = doc.add_paragraph(skills)
        paragraphs.append(p)
   
    doc.save("fake_resume.docx")

    return paragraphs


def main(args):
    sorted_skills, sorted_exp, sorted_attr = get_sorted_lists(args.search)
    (
        present_skills,
        skills_idx,
        present_exp,
        exp_idx,
        present_attr,
        attr_idx,
    ) = scrape_doc(args.filename)

    new_skills = coallesce_skills(sort_skills(sorted_skills, present_skills))
    new_exp = sort_experiences(sorted_exp, present_exp)

    write_paragraphs(new_skills, skills_idx, args.filename)
    write_paragraphs(new_exp, exp_idx, args.filename)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "search",
        type=str,
        help="Job URL or job title that this resume is to be tailored for",
    )
    parser.add_argument("resume_filename", type=str, help="Path to current resume")
    args = parser.parse_args()
    main(args)
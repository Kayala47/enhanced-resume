import argparse


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

from flask import Flask
import front_end
app = Flask(__name__)

@app.route("/")
def hello_world():
    outputs = helper.sort_results([["python","SKILL"],["C++","SKILL"],["python","SKILL"],["python","SKILL"],["Java","SKILL"],
    ["Java","SKILL"],["C++","SKILL"],["C++","SKILL"],["C++","SKILL"],["C++","SKILL"],["Java","SKILL"],
    ["hard-working","ATTRIBUTE"],["passionate","ATTRIBUTE"],["passionate","ATTRIBUTE"],["passionate","ATTRIBUTE"],["enthusiastic","ATTRIBUTE"]])
    sorted_skills = outputs[0]
    sorted_attributes = outputs[1]
    
    print(outputs)

    statement_top = "<p>This is the text for the top</p>"
    html_data = statement_top + "<table>\n<tr>\n<th>Skills</th>\n<th>Attributes</th></tr>\n"

    while len(sorted_skills) > 0 or len(sorted_attributes) > 0:
        skill = ""
        attribute = ""

        if len(sorted_skills) > 0:
            skill = sorted_skills.pop(0)
        else:
            " "

        if len(sorted_attributes) > 0:
            attribute = sorted_attributes.pop(0)
        else:
            " "

        table_row = "<tr><td>"+ skill + "</td><td>"+ attribute + "</td></tr>\n"

        html_data += table_row

    html_data += "</table>"
        
    return html_data
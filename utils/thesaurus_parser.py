import pandas as pd
"""
Author: Marsid Mali
Date: 2024-02-20
Description: 
This script processes a large dataset of textual lines to parse, clean, and categorize terms into a structured format. The script includes several key components:
1. `clean_term` function which cleans individual terms by removing content in brackets and parentheses, trimming additional punctuation, and filtering out terms based on specific criteria.
2. `parser` function which processes a list of text lines, extracting structured information such as class, division, section, and terms according to predefined categories. This function organizes the extracted information into a pandas DataFrame for further analysis or storage.
3. The script utilizes pandas for data manipulation, emphasizing the transformation of raw text into a structured and analyzable format.

Dependencies: pandas
"""


def clean_term(term, boolean):
    """
    Cleans a given term by removing content within brackets and parentheses, and trimming punctuation.

    :param term: The term to clean.
    :param boolean: A boolean value indicating whether to apply additional cleaning logic.
    :return: The cleaned term, or an empty string if the term doesn't meet certain criteria.
    """
    # Remove content in brackets and parentheses and additional punctuation
    term = term.split('[')[0].split('(')[0].strip().rstrip(';')
    # Remove if the term is a number or contains unwanted abbreviations or characters
    if term and ((term[0].isdigit() and (not any(c.isalpha() for c in term))) or ((term[-1] == "]") | (term[-1] == ")") | (term == "?")) and (not boolean)):
        return ""
    return term.strip('"\u0086"')


def parser(text_lines):
    """
    Parses text lines to extract structured information about classes, divisions, sections, and terms.

    :param text_lines: A list of text lines to parse.
    :return: A pandas DataFrame containing the structured information extracted from the text lines.
    """
    rows = []
    current_class = ""
    current_division = None
    current_section = ""
    current_subsection = ""
    current_concept = ""
    current_category = None
    category_mapping = {"N": "Noun", "V": "Verb", "Adj": "Adjective", "Adv": "Adverb", "Int": "Interjection", "Phr": "Phrase"}
    text_lines = text_lines[:131826]

    i = 0
    while i < len(text_lines):
        line = ' '.join(text_lines[i].split()).replace('\r', '')  # Remove extra spaces and carriage returns

        if line.startswith("CLASS"):
            current_class = ' '.join(text_lines[i:i+3]).replace('\r', ' ')
            current_class = ' '.join(current_class.split())
            current_division = None
            current_section = ""
            current_subsection = ""
            current_concept = ""
            i += 2  # Adjusted to skip the next two lines that are part of the CLASS definition

        elif line.startswith("DIVISION"):
            current_division = ' '.join(text_lines[i:i+3]).replace('\r', ' ')
            current_division = ' '.join(current_division.split())
            current_section = ""
            current_subsection = ""
            current_concept = ""
            i += 2  # Adjusted to skip the next two lines that are part of the DIVISION definition

        elif line.startswith("SECTION"):
            current_section = ' '.join(text_lines[i:i+3]).replace('\r', ' ')
            current_section = ' '.join(current_section.split())
            current_subsection = ""
            current_concept = ""
            i += 2  # Adjusted to skip the next two lines that are part of the SECTION definition

        elif line.startswith("#") and line.endswith("."):
            if i + 1 < len(text_lines):
                if text_lines[i + 1].strip().startswith('[') and i + 2 < len(text_lines):
                    current_concept = line + ' ' + text_lines[i + 2].strip()
                    i += 2  # Skip two lines
                else:
                    current_concept = line + ' ' + text_lines[i + 1].strip()
                    i += 1  # Skip one line

                current_concept = ' '.join(current_concept.split()).strip()

                if not current_subsection:
                    current_subsection = "No Subsection"
                current_category = None  # Reset the category for a new concept
            continue  # Skip to the next iteration

        elif len(line) > 1 and line[0].isdigit() and line[1] == '.':
            # Handling subsection titles that span multiple lines
            if i + 1 < len(text_lines):
                next_line = ' '.join(text_lines[i + 1].split())
                current_subsection = line + ' ' + next_line
                i += 1  # Adjust to skip the next line as it's part of the subsection title
            else:
                current_subsection = line
            i += 1  # Move to the next line after handling

        elif current_concept:
            if (line == 'N.') | (line == 'V.') | (line == 'Adj.') | (line == 'Adv.') | (line == 'Int.') | (line == 'Phr.'):
                current_category = line.split('.')[0]
            else:   # Filter out empty or invalid terms
                item = clean_term(line, True if current_concept.startswith('#550.') else False)
                if (len(item) > 1) and ((item.endswith(',') and ',' in item) | (item.endswith('.') and '.' in item)):
                    item = item[:-1]
                if item not in ["&c", "adj", "v", "n", "adv", "&c.", "adj.", "n.", "v.", "adv."]:
                    if item and ((not ((item[-1] == ']') | (item[-1] == ')'))) | ((item == ']') | (item == ')'))) and (current_category in category_mapping.keys() ):
                        row = {
                              "Class": current_class,
                              "Division/Section": current_division if current_division else current_section,
                              "Section": current_section,
                              "Subsection": current_subsection,
                              "Concept": current_concept[1:],
                              "Category": category_mapping[current_category],
                              "Term": item
                            }
                        rows.append(row)
            i += 1
        else:
            i += 1  # Default case to ensure the loop progresses

    df = pd.DataFrame(rows)
    df['Term'] = df['Term'].str.replace('\x86$', '', regex=True)
    return df

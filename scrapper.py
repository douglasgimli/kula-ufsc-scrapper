from lxml import html
import requests

page = requests.get('http://vestibular2017.ufsc.br/provas-anteriores/')
tree = html.fromstring(page.content)

# Get all editions
editions = tree.xpath('//*[@id="post-28"]/div[contains(@class, "content")]/table')

output = []

# Itinerate over all editions
for edition in editions:

    # Get and itirate over all table lines
    lines = edition.xpath('tbody/tr')
    for line in lines:
        
        # Fetch columns to find the lines with three columns
        columns = line.xpath('td')
        if len(columns) >= 3:
            questions = columns[1].xpath('a')
            
            if len(columns) == 4:
                answers = columns[3].xpath('a')
            else:
                answers = columns[2].xpath('a')

            if len(questions) and len(answers):
                label = columns[0].text
                try:
                    day = int(label.split('/')[0])
                except Exception as e:
                    day = 3

                if 'inglês' in label.lower():
                    language = 'english'
                elif 'francês' in label.lower():
                    language = 'french'
                elif 'espanhol' in label.lower():
                    language = 'spanish'
                elif 'italiano' in label.lower():
                    language = 'italian'
                elif 'alemão' in label.lower():
                    language = 'german'
                elif 'francês' in label.lower():
                    language = 'french'

                questions_file = questions[0].attrib['href']
                answers_file = answers[0].attrib['href']
                year = int(questions_file.split('/').pop().split('-')[0])

                if year not in [edition['year'] for edition in output]:
                    output.append({
                        'year': year,
                        'days': [],
                    })

                edition_key = [edition['year'] == year for edition in output]
                output[len(edition_key)-1]['days'].append({
                    'day': day,
                    'label': label,
                    'questions': questions_file,
                    'answers': answers_file,
                    'language': language,
                })

import json
print(json.dumps(output, indent=4))

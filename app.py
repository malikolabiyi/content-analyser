from flask import Flask, render_template, request, url_for

from bs4 import BeautifulSoup

import re 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/analyse", methods=['POST', "GET"])
def analyse():
    if request.method == 'POST':
        headline = request.form['headline']
        focus_keyword = request.form['focus_keyword']
        content = request.form['content']
    else:
        headline = request.args.GET['headline']
        focus_keyword = request.form['focus_keyword']
        content = request.args.GET['content']

    ''' Headline '''

    ''' Word Balance '''

    # Power words
    with open('power-words.txt') as p: 
        pws = list(p.read().split())
        headline_words = headline.lower().split(' ')

        power_words = list(set(pws).intersection(headline_words))

        number_power_words = len(power_words)

        if number_power_words > 0:
            power_word_analysis = "Your content have " + str(number_power_words) + " power words, they are " + str(power_words)  + ". Power words also known as phrases indicates intense trigger words that frequently command a reader's attention and action."
        else:
            power_word_analysis: 'Your content ought to contain atleast one power word.'
    p.close()

    #Common words
    with open('common-words.txt') as c: 
        cws = list(c.read().split())
        headline_words = headline.lower().split(' ')

        common_words = list(set(cws).intersection(headline_words))

        number_common_words = len(common_words)

        if number_common_words > 0:
            common_word_analysis = "Good! Your content have " + str(number_common_words) + " common words. Common words make up the basic structure of readable headlines. It is recommended that a headline should be made up of 2 to 3 common words."
        else:
            common_word_analysis: 'Your content ought to contain atleast 2 common words. Common words make up the basic structure of readable headlines.'
    c.close()

    #Uncommon words
    with open('uncommon-words.txt') as uc: 
        ucws = list(uc.read().split())
        headline_words = headline.lower().split(' ')

        uncommon_words = list(set(ucws).intersection(headline_words))

        number_uncommon_words = len(uncommon_words)

        if number_uncommon_words > 0:
            uncommon_word_analysis = "Good! Your content have " + str(number_uncommon_words) + " uncommon words. Uncommon words should occur less frequently than common words, but it is recommended to give your headline substance by adding 2 uncommon words."
        else:
            uncommon_word_analysis = 'Your content ought to contain atleast a uncommon word. Uncommon words should occur less frequently than common words, but it is recommended to give your headline substance by adding 2 uncommon words.'
    uc.close()

    ''' Word Length for headline '''

    if len(re.findall(r'\w+', headline)) < 3:
        word_length_for_headline = 'Your headline word length is kind of small, can you try to add more words?'   
    elif len(re.findall(r'\w+', headline))  > 20:
        word_length_for_headline = 'Your headline word length is too much, can you try to reduce them?'
    else: 
        word_length_for_headline = 'Awesome! Your headline word length is just perfect!' 

    ''' SEO for headline '''
    # For focus keyword in headline
    if focus_keyword.lower() in headline.lower():
        keyword_in_headline = 'Great! Your focus keyword appeared in your headline.'
    else:
        keyword_in_headline = "Oops! Your focus keyword didn't appear in your headline."

    ''' Content '''

    soup = BeautifulSoup(content, 'lxml')
    content_without_tags = soup.text

    # For readability (flesch reading ease and flesch kincaid socre)
    import textstat

    import math

    reading_ease_ = textstat.flesch_reading_ease(content_without_tags)

    reading_ease = math.ceil(int(reading_ease_))

    if reading_ease in range(90,101):
        reading_ease_score = 'Your content is very easy to read.'
    elif reading_ease in range(80,91):
        reading_ease_score = 'Your content is easy to read.'
    elif reading_ease in range(70,81):
        reading_ease_score = 'Your content is fairly easy to read.'
    elif reading_ease in range(60,71):
        reading_ease_score = 'Your content is of standard to read. It is not difficult and not easy to read.'
    elif reading_ease in range(50,61):
        reading_ease_score = 'Your content is fairly difficult to read.'
    elif reading_ease in range(30,51):
        reading_ease_score = 'Your content is difficult to read.'
    elif reading_ease in range(0,31):
        reading_ease_score = 'Your content is very confusing to read.'
    else:
        reading_ease_score = 'You didn\'t put in any message'
    
    grade_level = textstat.flesch_kincaid_grade(content_without_tags)

    grade_level_score = math.ceil(grade_level)

    grade_level_score = 'Your content can be comprehend by someone in ' + str(grade_level_score) + 'th grade and above.'

    # word length for content
    content_word_length_number = len(re.findall(r'\w+', content_without_tags))
    if content_word_length_number < 300:
        content_word_length = "Your content has " + str(content_word_length_number) + "words. It is fair, unless you want to best for generating discussion, can you try to add more?"
    elif content_word_length_number < 600:
        content_word_length = "Your content has " + str(content_word_length_number) + "words. It is good, unless you are writing about small topic, can you try to add more?"
    elif content_word_length_number in range(600,1501):
        content_word_length = "Your content has " + str(content_word_length_number) + "words. It is better, unless you are writing about small topic, can you try to add more?"
    else:
        content_word_length = "Your content has " + str(content_word_length_number) + "words. Fabulous! It is the best, just want is recommended!"
    
    # SEO for Content

    # Keyword in first paragraph
    paragraphs = []

    paragraphs = soup.find_all('p')

    if focus_keyword in paragraphs[0]:
        keyword_in_first_paragraph = 'Your focus keyword appeared in the first paragraph of your content, +1 for this!'
    else:
        keyword_in_first_paragraph = "Your focus keyword ought to appear in your first paragraph, incase you don't have a meta description, this is going to show on the search engine."

    # Paragraph Length.
    good_paragraph_length = []
    bad_paragraph_length = []

    words_number = []

    for paragraph in paragraphs:
        paragraph = paragraph.text
        for words in paragraph.split(' '):
            words_number.append(words)

            if len(words_number) < 50:
                good_paragraph_length.append(paragraph)
            else:
                bad_paragraph_length.append(paragraph)

    paragraph_analysis = 'Your content has ' + str(len(paragraphs)) + " paragraphs, only " + str(len(good_paragraph_length)) + "paragraphs contains the recommended number of words while " + str(len(bad_paragraph_length)) + " paragraphs contain much words than recommended."

    # Heading

    heading_tags = ['h2', 'h3', 'h4', 'h5', 'h6']

    headings = []

    for heading_tag in heading_tags:
        headings = soup.find_all(heading_tag)
    
    if len(headings) > 0:
        heading_analysis = 'Your content contains some headings, this gives your content more taste!'
    else: 
        heading_analysis = 'Your content is missing some headings.'
    
    return render_template('analyse.html', heading_analysis=heading_analysis, keyword_in_first_paragraph=keyword_in_first_paragraph, paragraph_analysis=paragraph_analysis, uncommon_word_analysis=uncommon_word_analysis, common_word_analysis=common_word_analysis, power_word_analysis=power_word_analysis, keyword_in_headline=keyword_in_headline, word_length_for_headline=word_length_for_headline, reading_ease_score=reading_ease_score, grade_level_score=grade_level_score, content_word_length=content_word_length)
    
if __name__ == "__main__":
    app.run(debug=True)
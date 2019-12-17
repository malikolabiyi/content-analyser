from flask import Flask, render_template, request, url_for

from bs4 import BeautifulSoup

import re 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/algorithms")
def algorithms():
    return render_template('algorithms.html')

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

    ''' HEADLINE '''
    headline_score = 0

    ''' Word Balance '''

    # Power words
    with open('power-words.txt') as p: 
        pws = list(p.read().split())
        headline_words = headline.lower().split(' ')

        power_words = list(set(pws).intersection(headline_words))

        number_power_words = len(power_words)

        if number_power_words > 0:
            power_word_analysis = "Your headline has " + str(number_power_words) + " power words. Power words, also known as phrases, indicate intense trigger words that frequently command a reader's attention and action."
            headline_score += 30
        else:
            power_word_analysis = 'Your headline ought to contain atleast one power word.'
    p.close()

    #Common words
    with open('common-words.txt') as c: 
        cws = list(c.read().split())
        headline_words = headline.lower().split(' ')

        common_words = list(set(cws).intersection(headline_words))

        number_common_words = len(common_words)

        if common_words:
            common_word_analysis = "Good! Your headline have " + str(number_common_words) + " common words. Common words make up the basic structure of readable headlines. It is recommended that a headline should be made up of 2 to 3 common words."
            headline_score += 10
        else:
            common_word_analysis = 'Your headline ought to contain atleast 2 common words. Common words make up the basic structure of readable headlines.'
    c.close()

    #Uncommon words
    with open('uncommon-words.txt') as uc: 
        ucws = list(uc.read().split())
        headline_words = headline.lower().split(' ')

        uncommon_words = list(set(ucws).intersection(headline_words))

        number_uncommon_words = len(uncommon_words)

        if number_uncommon_words > 0:
            uncommon_word_analysis = "Good! Your headline has " + str(number_uncommon_words) + " uncommon words. Uncommon words should occur less frequently than common words, but it is recommended to give your headline substance by adding 2 uncommon words."
            headline_score += 10
        else:
            uncommon_word_analysis = 'Your headline must contain at least 1 uncommon word. Uncommon words should occur less frequently than common words, but it is recommended to give your headline substance by adding 2 uncommon words.'
    uc.close()

    ''' SEO for headline '''
    # For focus keyword in headline
    if focus_keyword.lower() in headline.lower():
        keyword_in_headline = 'Great! Your focus keyword appeared in your headline.'
        headline_score += 20
    else:
        keyword_in_headline = "Oops! Your focus keyword didn't appear in your headline."

    # Number in headline
    for word in headline.split(' '):
        if word.isdigit():
            
            if int(word) % 2 != 0:
                number_in_headline = 'Amazing! Some numbers appeared in your headline. This helps improve your click-through-rate on the search engine.'
                headline_score += 10
            else:
                number_in_headline = 'Though some figures appeared but it is an even number, it is better if an odd number appeared.'
        else:
            number_in_headline = 'Your headline doesn\'t contain a figure, it is recommended to have a figure especially if you\'re writing on listing topics like \'top 9 places to visit\'. This helps to improve your click-through-rate on the search engine.'
            number_in_headline = 'Your headline doesn\'t contain a figure, it is recommended to have a figure especially if you\'re writing on listing topics like top 9 places to visit. This helps to improve your click-through-rate on the search engine.'


    # Word Length for headline

    if len(re.findall(r'\w+', headline)) < 3:
        word_length_for_headline = 'Your headline word length is kind of small, can you try to add more words?'  
    elif len(re.findall(r'\w+', headline))  > 20:
        word_length_for_headline = 'Your headline word length is too much, can you try to reduce them?'
    else: 
        word_length_for_headline = 'Awesome! Your headline word length is just perfect!'
        headline_score += 20
         
    
    
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
        reading_ease_score = 'You didn\'t input any message'
    
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

    for paragraph in soup.find_all('p'):
        paragraphs.append(paragraph)

    if focus_keyword in paragraphs[0]:
        keyword_in_first_paragraph = 'Your focus keyword appeared in the first paragraph of your content, +1 for this!'
    else:
        keyword_in_first_paragraph = "Your focus keyword must appear in your first paragraph, in case you don't have a meta description, this is going to show on the search engine."

    # Paragraph Length.
    good_paragraph_length = []
    bad_paragraph_length = []

    for paragraph in paragraphs:
        paragraph = paragraph.text

        if len(paragraph.split(' ')) < 50:
            good_paragraph_length.append(paragraph)
        else:
            bad_paragraph_length.append(paragraph)

    paragraph_analysis = 'Your content has ' + str(len(paragraphs)) + " paragraphs, only " + str(len(good_paragraph_length)) + " paragraphs contains the recommended number of words while " + str(len(bad_paragraph_length)) + " paragraphs contain more words than recommended."

    # Heading

    heading_tags = ['h2', 'h3', 'h4', 'h5', 'h6']

    headings = soup.find_all(heading_tags)
    
    if len(headings) > 0:
        heading_analysis = 'Your content contains some headings, this gives your content more taste!'
        
    else: 
        heading_analysis = 'Your content is missing some headings.'

    heading_with_focus_keyword = []

    heading_without_focus_keyword = []

    # Focus keyword in heading

    for heading in headings:
        heading = heading.text
        if focus_keyword in heading:
            heading_with_focus_keyword.append(heading)
        else:
            heading_without_focus_keyword.append(heading)
    
    heading_focus_keyword = "Your content has " + str(len(headings)) + " heading(s) only " + str(len(heading_with_focus_keyword)) + " heading(s) contains your focus keyword while " + str(len(heading_without_focus_keyword)) + " heading(s) doesn't contain your focus keyword. It is recommended that your focus keyword should appear atleast in 2 heading but not all to avoid keyword stuffing." 

    # Link
    links = soup.find_all('a')

    if len(links) > 0:
        links_analysis = 'It is so very cool that your content is linking to other people\'s content.'
    else:
        links_analysis = 'At least you should be linking to content.'

    # Sentence Length
    good_sentence_length = []
    bad_sentence_length = []

    for paragraph in paragraphs:
        paragraph = paragraph.text
        sentences = re.split(r'[.!?]+', paragraph)

        for sentence in sentences:
            if len(sentence) < 20:
                good_sentence_length.append(sentence)
            else:
                bad_sentence_length.append(sentence)

    sentence_length = 'Your content has ' + str(len(sentences)) + " sentences, only " + str(len(good_sentence_length)) + " sentences contains the recommended number of words (fewer than 20) while " + str(len(bad_sentence_length)) + " sentences contain more than recommended."

    return render_template('analyse.html', links_analysis=links_analysis, sentence_length=sentence_length, headline_score=headline_score, number_in_headline=number_in_headline, heading_focus_keyword=heading_focus_keyword, heading_analysis=heading_analysis, keyword_in_first_paragraph=keyword_in_first_paragraph, paragraph_analysis=paragraph_analysis, uncommon_word_analysis=uncommon_word_analysis, common_word_analysis=common_word_analysis, power_word_analysis=power_word_analysis, keyword_in_headline=keyword_in_headline, word_length_for_headline=word_length_for_headline, reading_ease_score=reading_ease_score, grade_level_score=grade_level_score, content_word_length=content_word_length)
    
if __name__ == "__main__":
    app.run(debug=True)

import pandas as pd

papers = pd.read_excel('./document_data.xlsx', sheet_name='document_data')


def text_clean(text):
    import re
    # remove punctuations
    text = re.sub('[,\.!?]', '', text)

    # lower case
    text = text.lower()

    return text


def exploratory_analysis(array_words):
    # Import the wordcloud library
    from wordcloud import WordCloud
    # Join the different processed titles together.
    long_string = ','.join(list(array_words))
    # Create a WordCloud object
    wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
    # Generate a word cloud
    wordcloud.generate(long_string)
    # Visualize the word cloud
    wordcloud.to_image()


papers['text_processed'] = papers['document_text'].map(lambda text: text_clean(text))

print(papers['text_processed'])

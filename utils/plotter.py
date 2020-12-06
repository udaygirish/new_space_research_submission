import numpy as np
from wordcloud import WordCloud
from PIL import Image
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

def wordcloud_generator(text_list,filename):
    '''
    Function to generate wordcloud bu taking a text list
    removing stop words and then writing the word cloud 
    image file to disk
    '''
    total_text = " ".join(review for review in text_list)
    print("Total_Text_length:{}".format(len(total_text)))
    text_stop_removed = " ".join([i for i in total_text.split(" ") if i not in stopwords.words('english')])
    print("Total_Text_after_stopword_removal_length:{}".format(len(text_stop_removed)))
    # Generate a wordcloud
    wordcloud = WordCloud(background_color="black").generate(text_stop_removed)
    plt.imshow(wordcloud,interpolation='bilinear')
    plt.axis("off")
    wordcloud.to_file(filename)
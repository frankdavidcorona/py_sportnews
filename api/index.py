import requests
import re
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)


def sanitize_text(text):
    # Remove HTML entities
    text = re.sub(r'&[^;]+;', '', text)

    # Replace multiple spaces or line breaks with a single space
    text = re.sub(r'\s+', ' ', text)

    # Remove all non-ASCII Unicode characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # Strip leading and trailing spaces
    text = text.strip()

    return text


def scrape_news_headlines():
    url = 'https://www.as.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headlines_and_images = []

    # Find all 'article' elements
    articles = soup.find_all('article')

    # Loop through each 'article' element
    for article in articles:
        # Find the 'h2' element within the 'article'
        h2 = article.find('h2')
        if h2 is not None:
            headline = sanitize_text(h2.get_text())
        else:
            continue

        # Find the 'figure' element within the 'article' and extract the image URL
        figure = article.find('figure')
        img_url = None
        if figure is not None:
            img = figure.find('img')
            if img is not None:
                img_url = img.get('src')

        headlines_and_images.append(
            {'headline': headline, 'image_url': img_url})

    return headlines_and_images


@app.route('/')
def home():
    return 'Password Generator and Checker!'


@app.route('/api/news', methods=['GET'])
def get_news():
    headlines = scrape_news_headlines()
    return jsonify(headlines)


if __name__ == '__main__':
    app.run(debug=True)

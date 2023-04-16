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
    url = 'https://as.com/futbol/primera/?omnil=mpal'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles_data = []

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
        if figure is None:
            continue

        img_url = None
        img = figure.find('img')
        if img is not None:
            img_url = img.get('src')

        # Skip the article if the image URL is undefined or null
        if img_url is None:
            continue

        # Find all 'p' elements within the 'article' and extract their text
        paragraphs = article.find_all('p')
        paragraph_texts = [sanitize_text(p.get_text(
        )) for p in paragraphs if p.get_text().strip() and len(p.get_text()) >= 25]

        # Skip the article if the list of paragraphs is empty
        if not paragraph_texts:
            continue

        articles_data.append({
            'headline': headline,
            'image_url': img_url,
            'paragraphs': paragraph_texts
        })

    return articles_data


@app.route('/')
def home():
    return 'Password Generator and Checker!'


@app.route('/api/news', methods=['GET'])
def get_news():
    headlines = scrape_news_headlines()
    return jsonify(headlines)


if __name__ == '__main__':
    app.run(debug=True)

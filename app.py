from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing required parameter: 'query'"}), 400

    base_url = "https://estherox123.github.io/database/"
    index_page = requests.get(base_url)
    soup = BeautifulSoup(index_page.content, 'html.parser')

    links = [a['href'] for a in soup.find_all('a', href=True)]

    search_results = []

    for link in links:
        html_page = requests.get(base_url + link)
        page_soup = BeautifulSoup(html_page.content, 'html.parser')
        page_text = page_soup.get_text().lower()
        page_title = page_soup.find('h1').get_text()
        page_company = page_soup.find('h3').get_text()
        page_date = page_soup.find('h2').get_text()
        
        # If the query is found in the HTML text, add the text snippet to the results
        if query.lower() in page_text:
            start = page_text.find(query.lower())
            end = start + len(query) + 750  # Adjust the range as needed
            snippet = page_text[start:end].replace('\n', ' ').strip()
            search_results.append({"title": page_company + " - " + page_title, "date": page_date, "link": base_url + link, "snippet": snippet})

    return jsonify(search_results)

if __name__ == '__main__':
    app.run(debug=True)

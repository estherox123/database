import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query').lower()
    if not query:
        return jsonify({"error": "Missing required parameter: 'query'"}), 400

    base_path = "path/to/local/html/files"
    search_results = []

    for root, dirs, files in os.walk(base_path):
        for file_name in files:
            if file_name.endswith('.html'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    page_text = soup.get_text().lower()
                    if query in page_text:
                        page_title = soup.find('h1').get_text()
                        page_company = soup.find('h3').get_text()
                        page_date = soup.find('h2').get_text()
                        snippet = "..." + page_text[page_text.find(query)-50:page_text.find(query)+50] + "..."
                        search_results.append({"title": f"{page_company} - {page_title}", "date": page_date, "snippet": snippet})

    return jsonify(search_results)

if __name__ == '__main__':
    app.run(debug=True)

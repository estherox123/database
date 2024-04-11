import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query').lower()
    if not query:
        return jsonify({"error": "Missing required parameter: 'query'"}), 400

    base_path = "C:\\Users\PC05\Downloads\database_app\database"
    search_results = []

    for root, dirs, files in os.walk(base_path):
        for file_name in files:
            if file_name.endswith('.html'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    page_text = soup.get_text().lower()
                    # If the query is found in the HTML text, add the text snippet to the results
                    if query in page_text:
                        start = page_text.find(query)
                        sentence_start = page_text.rfind('.', 0, start)
                        if sentence_start == -1:  # If there's no period, start from the beginning
                            sentence_start = 0
                        else:
                            sentence_start += 2  # Skip past the period and the space after it

                        end = start + 500  # Adjust the range as needed
                        snippet = page_text[sentence_start:end].replace('\n', ' ').strip()
                        search_results.append({"title": file_name, "snippet": snippet})

    return jsonify(search_results)

if __name__ == '__main__':
    app.run(debug=True)

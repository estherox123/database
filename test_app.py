import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

keyword = input("검색어: ")
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
                if keyword in page_text:
                    start = page_text.find(keyword)
                    sentence_start = page_text.rfind('.', 0, start)
                    if sentence_start == -1:  # If there's no period, start from the beginning
                        sentence_start = 0
                    else:
                        sentence_start += 2  # Skip past the period and the space after it

                    end = start + len(keyword) + 500  # Adjust the range as needed
                    snippet = page_text[sentence_start:end].replace('\n', ' ').strip()
                    search_results.append({"title": file_name, "snippet": snippet})
print(search_results)
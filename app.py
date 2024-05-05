from flask import Flask, render_template, request
from inverted_index_loader import load_inverted_index, load_meta_file
from vector_space_model import compute_weight_matrix, retrieve_documents

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    inverted_index = load_inverted_index('inverted_index.csv')
    meta_data = load_meta_file('meta_file.csv')
    weight_matrix = compute_weight_matrix(inverted_index, meta_data)
    ranked_documents = retrieve_documents(query, weight_matrix, meta_data)
    if not ranked_documents:
        return render_template('no_results.html')
    else:
        return render_template('results.html', query=query, documents=ranked_documents)

if __name__ == '__main__':
    app.run(debug=True)

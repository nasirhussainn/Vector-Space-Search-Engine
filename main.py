# main.py

# Import necessary modules
from flask import Flask, render_template, request
from backend.vector_space_model import VectorSpaceModel
from backend.compute_weights import compute_weights

# Initialize Flask app
app = Flask(__name__, template_folder='frontend/templates')

# Specify output path for weight_matrix.csv
output_file = "weight_matrix.csv"

# Compute weights and create VectorSpaceModel instance
# weight_matrix = compute_weights("inverted_index.csv", output_file)
vector_space_model = VectorSpaceModel(output_file, "meta_file.csv")

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        search_results = vector_space_model.query(query)
        return render_template('search_results.html', query=query, search_results=search_results)
    return render_template('frontend/templates/index.html')

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)

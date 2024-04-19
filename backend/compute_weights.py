# compute_weights.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def compute_weights(inverted_index_file, output_file):
    # Load inverted index CSV file
    inverted_index_df = pd.read_csv(inverted_index_file)

    # Combine posting lists into documents
    documents = inverted_index_df['Posting List'].apply(lambda x: ' '.join(x.split('-')))

    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Compute TF-IDF weights
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Get keywords
    keywords = vectorizer.get_feature_names_out()

    # Create weight matrix
    weight_matrix = pd.DataFrame(tfidf_matrix.toarray(), columns=keywords)

    # Save weight matrix to CSV
    weight_matrix.to_csv(output_file, index=False)

    return output_file

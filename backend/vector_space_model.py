import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.impute import SimpleImputer
import numpy as np

class VectorSpaceModel:
    def __init__(self, weight_matrix_file, meta_file):
        self.weight_matrix = pd.read_csv(weight_matrix_file)
        self.meta_file_df = pd.read_csv(meta_file)

    def query(self, query):
        # Vectorize query
        query_vector = self.vectorize_query(query)

        # Handle missing values
        query_vector, self.weight_matrix = self.handle_missing_values(query_vector, self.weight_matrix)

        # Calculate cosine similarity
        similarity_scores = cosine_similarity(query_vector, self.weight_matrix)

        # Get ranked documents
        ranked_documents_indices = similarity_scores.argsort()[0][::-1]
        ranked_documents = self.meta_file_df.iloc[ranked_documents_indices]

        return ranked_documents

    def vectorize_query(self, query):
        # Vectorize query using TF-IDF or any other method
        pass  # Implement vectorization here

    def handle_missing_values(self, query_vector, weight_matrix):
        # Convert query_vector to NumPy array
        query_vector = np.asarray(query_vector)

        # Check if query_vector is a scalar NaN value
        if np.isscalar(query_vector) and np.isnan(query_vector):
            # If query_vector is a scalar NaN value, reshape it to 2D array
            query_vector = query_vector.reshape(1, -1)

        # Convert weight_matrix to NumPy array
        weight_matrix = np.asarray(weight_matrix)

        # Check for NaN values in weight_matrix
        if np.isnan(weight_matrix).any():
            # If weight_matrix contains NaN values, replace them with zeros
            weight_matrix = np.nan_to_num(weight_matrix)

        return query_vector, weight_matrix

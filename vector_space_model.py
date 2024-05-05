import math
import numpy as np
import csv
from collections import defaultdict

def compute_tf(term_frequency):
    return 1 + math.log(term_frequency, 10) if term_frequency > 0 else 0

def compute_idf(total_documents, document_frequency):
    return math.log(total_documents / document_frequency, 10)

def compute_weight_matrix(inverted_index, meta_data):
    weight_matrix = defaultdict(dict)
    total_documents = len(meta_data)
    for keyword, data in inverted_index.items():
        df = len(data['posting_list'])
        idf = compute_idf(total_documents, df)
        for doc_id in data['posting_list']:
            if doc_id in meta_data:
                tf = compute_tf(meta_data[doc_id]['Keywords'].count(keyword))
                weight_matrix[doc_id][keyword] = tf * idf
    return weight_matrix

def cosine_similarity(query_vector, document_vector):
    dot_product = np.dot(query_vector, document_vector)
    query_norm = np.linalg.norm(query_vector)
    doc_norm = np.linalg.norm(document_vector)
    if query_norm == 0 or doc_norm == 0:
        return 0
    return dot_product / (query_norm * doc_norm)


def retrieve_documents(query, weight_matrix, meta_data, top_n=5):
    all_terms = set(term for doc_vector in weight_matrix.values() for term in doc_vector.keys())
    query_vector = np.zeros(len(all_terms))

    terms = query.split()
    for term in terms:
        if term in all_terms:
            query_vector[list(all_terms).index(term)] += 1

    similarity_scores = {}
    for doc_id, document_vector in weight_matrix.items():
        doc_vector = np.array([document_vector.get(term, 0) for term in all_terms])
        similarity = cosine_similarity(query_vector, doc_vector)
        if similarity > 0:
            similarity_scores[doc_id] = similarity

    if not similarity_scores:
        return []

    sorted_documents = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    ranked_documents = []
    for doc_id, similarity in sorted_documents:
        doc_data = meta_data.get(doc_id, {})
        ranked_documents.append({
            'ID': doc_id,
            'URI': doc_data.get('URI', ''),
            'Title': doc_data.get('Title', ''),
            'Description': doc_data.get('Description', ''),
            'Images': doc_data.get('Images', ''),
            'Similarity': similarity
        })
    return ranked_documents



def save_weight_matrix_to_csv(weight_matrix, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        header = ['ID'] + list(next(iter(weight_matrix.values())))
        writer.writerow(header)
        for doc_id, vector in weight_matrix.items():
            row = [doc_id] + [vector.get(term, 0) for term in next(iter(weight_matrix.values()))]
            writer.writerow(row)

def load_weight_matrix_from_csv(file_path):
    weight_matrix = {}
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        terms = header[1:]
        for row in reader:
            doc_id = int(row[0])
            tfidf_values = [float(val) for val in row[1:]]
            weight_matrix[doc_id] = {term: tfidf_values[i] for i, term in enumerate(terms)}
    return weight_matrix

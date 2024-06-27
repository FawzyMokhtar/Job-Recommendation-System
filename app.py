from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
cors = CORS(app)


def get_recommendations(profile_input: str, location_input: str, count_input: int = 5):
    # Declare the result data and initialize its recommendations.
    recommendations = {'profiles': [], 'locations': []}
    recommendations['profiles'] = []
    recommendations['locations'] = []

    # Read data from the DataSet.
    # Only read the rows contain data.
    df = pd.read_csv("data.csv")
    df = df[:31]

    # region jobs based on profile.

    # Read the column for the job description.
    jobs = np.array(df['Job_Description'])

    # Combine user profile and job descriptions for vectorization.
    combined_jobs = np.concatenate(([profile_input], jobs), axis=0)

    # Create TF-IDF vectorizer and fit on combined text data.
    vectorizer = TfidfVectorizer()
    text_vectors = vectorizer.fit_transform(combined_jobs)

    # Calculate cosine similarity between profile vector and job description vectors
    profile_vector = text_vectors[0]  # Profile vector.
    job_vectors = text_vectors[1:]  # Job description vectors.
    cosine_similarities = cosine_similarity(profile_vector, job_vectors)[0]

    # Map similarities to jobs scores with indices.
    jobs_scores = []  # { index, score }[]
    for idx in range(len(cosine_similarities)):
        if cosine_similarities[idx] > 0:
            jobs_scores.append({'idx': idx, 'score': cosine_similarities[idx]})

    # Rank the matched profiles according to score.
    # Take only the requested count of jobs.
    jobs_scores = sorted(jobs_scores, key=lambda job: job['score'])[
        :count_input]

    # Map matched profiles to jobs.
    for job_score in jobs_scores:
        recommendations['profiles'].append(jobs[job_score['idx']])

    # endregion jobs based on profile.

    # region jobs based on location.

    # Read the column for the location.
    locations = np.array(df['Location'])

    # Loop through locations and match [exact] user location.
    # Take the matched location's jobs.
    for idx in range(len(locations)):
        if locations[idx] == location_input:
            recommendations['locations'].append(jobs[idx])

    # Take only the requested count of jobs.
    recommendations['locations'] = recommendations['locations'][:count_input]

    return recommendations


# API Routes.
@app.route('/api/get_recommendations', methods=['POST'])
def get_recommendations_endpoint():
    try:
        # Read input data from the JSON request.
        input_data = request.json

        # Run the recommendation process.
        recommendations = get_recommendations(
            input_data['profile'], input_data['location'], input_data['count'])

        return jsonify({'data': recommendations})

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error': 'An error occurred'}), 500


# Server (API) Entry Point.
if __name__ == '__main__':
    app.run(debug=True, port=4000, host='localhost')

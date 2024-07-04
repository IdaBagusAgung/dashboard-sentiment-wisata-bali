from flask import Flask, request, jsonify, render_template
import pickle
import os
import numpy as np

app = Flask(__name__)

# Paths to the models and vectorizers
model_paths = {
    'naive_bayes': os.path.join('model', 'model_naive_bayes.pkl'),
    'svm': os.path.join('model', 'model_svm.pkl'),
    'decision_tree': os.path.join('model', 'model_decision_tree.pkl'),
    'random_forest': os.path.join('model', 'model_random_forest.pkl'),
    'gradient_boosting': os.path.join('model', 'model_gradient_boosting.pkl')  # Added Gradient Boosting path
}
vectorizer_paths = {
    'naive_bayes': os.path.join('model', 'vectorizer_naive_bayes.pkl'),
    'svm': os.path.join('model', 'vectorizer_svm.pkl'),
    'decision_tree': os.path.join('model', 'vectorizer_decision_tree.pkl'),
    'random_forest': os.path.join('model', 'vectorizer_random_forest.pkl'),
    'gradient_boosting': os.path.join('model', 'vectorizer_gradient_boosting.pkl')  # Added Gradient Boosting vectorizer path
}

# Load the models and vectorizers
models = {}
vectorizers = {}
for model_name, model_path in model_paths.items():
    with open(model_path, 'rb') as model_file:
        models[model_name] = pickle.load(model_file)
    with open(vectorizer_paths[model_name], 'rb') as vectorizer_file:
        vectorizers[model_name] = pickle.load(vectorizer_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(force=True)
    komentar = data['komentar']
    model_name = data['model']

    # Get the selected model and vectorizer
    model = models.get(model_name)
    vectorizer = vectorizers.get(model_name)
    if model is None or vectorizer is None:
        return jsonify({'error': 'Model atau vectorizer tidak ditemukan.'}), 400

    # Transform the input using the appropriate vectorizer
    komentar_transformed = vectorizer.transform([komentar])

    # Make prediction
    sentiment = model.predict(komentar_transformed)[0]

    # Get prediction probabilities if model supports predict_proba
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(komentar_transformed)
        confidence = np.max(probabilities)
    else:
        confidence = None  # Handle the case if predict_proba is not available

    return jsonify({
        'sentiment': sentiment,
        'confidence': f"{confidence*100:.2f}%" if confidence is not None else 'N/A'
    })

if __name__ == "__main__":
    app.run(debug=True)

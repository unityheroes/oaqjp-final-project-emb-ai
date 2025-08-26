from flask import Flask, render_template, request, jsonify
from emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['GET', 'POST'])
def emotion_detector_endpoint():
    """
    Endpoint for emotion detection.
    Supports both GET and POST requests.
    """
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        text = data.get('text') or data.get('textToAnalyze') or ''
    else:
        text = request.args.get('textToAnalyze') or request.args.get('text') or ''

    if not text.strip():
        return jsonify({'error': 'Invalid text! Please provide text to analyze.'}), 400

    result = emotion_detector(text)
    if result['dominant_emotion'] is None:
        return jsonify({'error': 'Unable to analyze emotions. Please try again.'}), 400

    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and 'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return jsonify({
        'response': response_text,
        'emotions': {
            'anger': result['anger'],
            'disgust': result['disgust'],
            'fear': result['fear'],
            'joy': result['joy'],
            'sadness': result['sadness'],
            'dominant_emotion': result['dominant_emotion']
        }
    })

@app.route('/')
def index():
    """Serves the main page."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
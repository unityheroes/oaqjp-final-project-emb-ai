"""
emotion_detection.py

This module provides the function `emotion_detector` to analyze the emotions
of a given text using Watson NLP API. It returns emotion scores and the
dominant emotion.
"""

import requests


def emotion_detector(text_to_analyze):
    """
    Analyzes the emotion of the given text using Watson NLP API.

    Args:
        text_to_analyze (str): The text to analyze.

    Returns:
        dict: A dictionary containing emotion scores and dominant emotion.
              Keys: 'anger', 'disgust', 'fear', 'joy', 'sadness', 'dominant_emotion'
              If input is blank or API fails, values are None.
    """
    if not text_to_analyze or not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    if response.status_code != 200:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    try:
        data = response.json()
        emotions = data['emotionPredictions'][0]['emotion']
        anger = emotions.get('anger')
        disgust = emotions.get('disgust')
        fear = emotions.get('fear')
        joy = emotions.get('joy')
        sadness = emotions.get('sadness')
    except (KeyError, IndexError, ValueError):
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    emotion_scores = {
        'anger': anger,
        'disgust': disgust,
        'fear': fear,
        'joy': joy,
        'sadness': sadness
    }

    dominant_emotion = None
    valid_scores = {k: v for k, v in emotion_scores.items() if v is not None}
    if valid_scores:
        dominant_emotion = max(valid_scores, key=valid_scores.get)

    return {
        'anger': anger,
        'disgust': disgust,
        'fear': fear,
        'joy': joy,
        'sadness': sadness,
        'dominant_emotion': dominant_emotion
    }

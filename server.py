from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)
# Разрешаем запросы от нашего интерфейса
CORS(app)

def get_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    data = request.json
    url = data.get('url', '')
    video_id = get_video_id(url)
    
    if not video_id:
        return jsonify({'error': 'Не удалось найти ID видео в ссылке'}), 400
        
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=['ru', 'en'])
        # Склеиваем фрагменты пробелами вместо переносов строк (\n)
        raw_text = ' '.join([t.text.replace('\n', ' ') for t in transcript])
        # Убираем возможные двойные пробелы
        text = ' '.join(raw_text.split())
        
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': f'Субтитры отключены или произошла ошибка: {str(e)}'}), 500

if __name__ == '__main__':
    print("Сервер запущен на http://127.0.0.1:5000")
    app.run(port=5000)
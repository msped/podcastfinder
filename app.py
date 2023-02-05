import os
from flask import Flask, request
from dotenv import load_dotenv
from flask_pymongo import pymongo
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECERT_KEY")
app.config["MONGO_DBNAME"] = os.getenv("MONGO_DBNAME")

mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = mongo_client.get_database(os.getenv('MONGO_DBNAME'))

def check_for_profanity_filter(transcript):
    if "[\u00a0__\u00a0]" in transcript:
        return True
    return False

def get_full_transcript_from_yt_api(transcript):
    text = []
    for item in transcript:
        text.append(item['text'])
    return " ".join(text)
            

@app.route("/api/transcript/create", methods=["POST",])
def download_transcripts():
    if request.method == "POST":
        video_id = request.form['video_id']
        title = request.form['title']
        channel = request.form['channel']

        if not db.transcripts.find_one({'video_id': video_id}):
            video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_transcript = get_full_transcript_from_yt_api(video_transcript)

            if check_for_profanity_filter(full_transcript):
                # go to assembly ai for transcript
                return 'Sent to third-party service for transcription', 200
            else:
                # save transcript to db
                db.transcripts.insert_one({
                    'video_id': video_id,
                    'title': title,
                    'channel': channel,
                    'transcript_with_time': video_transcript,
                    'full_transcript': full_transcript  
                })
                return 'Created', 201
        else:
            return 'Podcast already exists in database', 400

    return 'Method not allowed', 405

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, Response
import openai
import os


app = Flask(__name__)


def chat(user_message):
    openai.api_type = os.getenv("OPENAI_API_TYPE") 
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
    openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai.api_version = os.getenv("OPENAI_API_VERSION")

    response = openai.ChatCompletion.create(
        engine = os.getenv("AZURE_OPENAI_ENGINE"),
        messages = [
            {"role": "user", "content": user_message}
        ],
        stream = True)
    
    for chunk in response:
        try:
            yield f"{chunk.choices[0].delta.content}"
        except:
            pass
    

@app.route('/chat-stream/<user_message>')
def chat_stream(user_message):
    return Response(chat(user_message), mimetype='text/event-stream')
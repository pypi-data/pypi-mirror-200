#!/usr/bin/env python3

from flask import Flask, request
import requests
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('underlying-prompts.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def handle_request(path):
    if request.method == 'POST':
        headers = {
            "Content-Type": request.headers["Content-Type"],
            "Authorization": request.headers["Authorization"]
        }
        json_data = request.get_json()
        logger.info(f"OpenAI Request: {json_data}")

        url = f"https://api.openai.com/{path}"
        response = requests.post(
            url,
            headers=headers,
            json=json_data
        )
        logger.info(f"OpenAI Response: {response.json()}")

        return response.json()


def main():    
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8888
    app.run(port=port)


if __name__ == '__main__':
    main()
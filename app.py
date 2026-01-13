from flask import Flask, request, jsonify
from openai import OpenAI
import os
import json
import re

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.S)
    return json.loads(match.group()) if match else {}


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    image_base64 = data.get("image_base64")

    if not image_base64:
        return jsonify({"error": "image_base64 missing"}), 400

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Верни ТОЛЬКО JSON: "
                    "{name, ingredients, macros_per_100g{protein_g,fat_g,carbs_g}, calories_per_100g}"
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        },
                    }
                ],
            },
        ],
        max_tokens=800,
    )

    raw = response.choices[0].message.content
    return jsonify(extract_json(raw))

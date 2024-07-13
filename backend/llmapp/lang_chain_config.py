from langchain_openai import OpenAI
from django.conf import settings
import json
from typing import List

# Initialize OpenAI API key
openai_api_key = ""
llm = OpenAI(api_key=openai_api_key)

def perform_ner(text):
    prompt = (
        "You are a highly intelligent and accurate Named-entity recognition(NER) system. "
        "You take Passage as input and your task is to recognize and extract specific types of "
        "named entities in that given passage and classify them into a set of entity types.\n"
        f"Passage: {text}\n"
        "Output the entities with their start and end offsets."
    )
    response = llm(prompt)
    print(response)
    return response

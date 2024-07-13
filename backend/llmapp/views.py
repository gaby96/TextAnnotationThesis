from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from typing import List, Optional
from django.views.decorators.csrf import csrf_exempt 
from langchain_openai import OpenAI
from django.conf import settings
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
import json

# Initialize OpenAI API key
openai_api_key = settings.OPENAI_API_KEY
llm = OpenAI(api_key=openai_api_key)


# Define your desired data structure.
class NER(BaseModel):
    end_offset:int = Field("An integer representing the position in the text where the named entity ends. It indicates the last character index of the entity")
    id:int = Field("An integer serving as a unique identifier for the named entity. This ID can be used to distinguish between different entities")
    entity_type:str =  Field("A string indicating the category or type of the named entity (e.g., 'Person,' 'Location,' 'Organization')")
    label_name:str = Field("A string representing the actual name or label of the named entity found in the text")
    start_offset:int = Field("An integer representing the position in the text where the named entity starts. It indicates the first character index of the entity")


class NERList(BaseModel):
    entities: List[NER]


def generate_dynamic_prompt(data):
    entity_types = data['data1']
    text = data['data2']


    parser = JsonOutputParser(pydantic_object=NERList)

    prompt_query = "You are a highly intelligent and accurate Named-entity recognition (NER) system. Your task is to recognize and extract specific types of named entities in the given passage and classify them into one of the following entity types given:\n"
        
    prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{prompt_query}\n{entity_types}\n{text}",
    input_variables=["text", "entity_types", "prompt_query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    return chain.invoke({"text": text, "entity_types": entity_types, "prompt_query": prompt_query})

@csrf_exempt
def ner_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Generate the prompt
            prompt = generate_dynamic_prompt(data)
            return JsonResponse({'data': prompt}, status=200)
        except Exception as e:
            print(f"An exception occurred: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

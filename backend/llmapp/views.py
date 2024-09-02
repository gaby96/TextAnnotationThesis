from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from typing import List, Optional
from django.views.decorators.csrf import csrf_exempt 
from langchain_openai import OpenAI
from django.conf import settings
from label_types.models import SpanType, CategoryType
#from label_types.models import CategoryType
from labels.models import Category, Span
#from labels.models import Span
from labels.serializers import SpanSerializer, CategorySerializer
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
# from bert_model import BERTSequenceLabeling
from .bert_model import BERTSequenceLabeling, BERTTextClassification
import json

# Initialize OpenAI API key
openai_api_key = settings.OPENAI_API_KEY
llm = OpenAI(api_key="")


# Define your desired data structure.
class NER(BaseModel):
    end_offset:int = Field("An integer representing the position in the text where the named entity ends. It indicates the last character index of the entity")
    #id:int = Field("An integer serving as a unique identifier for the named entity. This ID can be used to distinguish between different entities")
    entity_type:str =  Field("A string indicating the category or type of the named entity (e.g., 'Person,' 'Location,' 'Organization')")
    label_name:str = Field("A string representing the actual name or label of the named entity found in the text")
    start_offset:int = Field("An integer representing the position in the text where the named entity starts. It indicates the first character index of the entity")


class NERList(BaseModel):
    entities: List[NER]


class docClassification(BaseModel):
    sentiment:str = Field("A string indicating the sentiment of the text")

class docClassificationList(BaseModel):
    inference: List[docClassification]


def generate_dynamic_prompt(data):
    entity_types = data['data1']
    text = data['data2']

    entity_types_str = "\n".join([f"- {entity['text']} : Description for {entity['text']}" for entity in entity_types])

    parser = JsonOutputParser(pydantic_object=NERList)

    prompt_query = (
        "You are a highly intelligent and accurate Named-entity recognition (NER) system. "
        "Your task is to recognize and extract specific types of named entities in the given passage. "
        "Please follow these instructions:\n"
        "1. Tokenize the text first into words"
        "2. Only recognize and extract entities that match the following types:\n"
        f"{entity_types_str}\n"
        "3. Do not create or use any entity types that are not listed above.\n"
        "4. If the text does not contain any entities of the specified types, do not include them in the response.\n"
        "The end_offset and start_offset should be word by word and no overlaps"
        "Here is the passage:\n"
        "{text}\n"
    )
        
    prompt = PromptTemplate(
        template="{prompt_query}{text}\n{format_instructions}",
        input_variables=["text", "prompt_query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    return chain.invoke({"text": text, "prompt_query": prompt_query})

@csrf_exempt
def ner_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
         
            # Delete existing spans for the exampleId and annotated_by 'llm'
            example_id = data['exampleId']
            Span.objects.filter(example_id=example_id, annotated_by='llm').delete()

            
            if data['selectedModel'] == 'GPT-4':
                # Generate the prompt
                prompt = generate_dynamic_prompt(data)

                print(prompt)
                # Save the list of objects
            
            # print(type(prompt))
                if 'entities' in prompt:
                # print(prompt['entities'])
                    saved_entities = []
                    required_keys = ['start_offset', 'end_offset']

                    # Filter out entities missing required keys
                    valid_entities = [entity for entity in prompt['entities'] if all(key in entity for key in required_keys)]

                    # Fetch all span types and create a mapping from name to ID
                    span_types = SpanType.objects.all()
                    span_type_mapping = {span_type.text: span_type.id for span_type in span_types}

                    # Fetch existing spans for the example to check for overlaps
                    example_id = data['exampleId']
                    existing_spans = Span.objects.filter(example_id=example_id)

                    for entity in valid_entities:
                        entity_type_name = entity['entity_type']
                        if entity_type_name in span_type_mapping:
                            start_offset = entity['start_offset']
                            end_offset = entity['end_offset']
                            
                            # Check for overlap using is_overlapping method
                        # Check for overlap using is_overlapping method
                            overlaps = any(existing_span.is_overlapping(Span(start_offset=start_offset, end_offset=end_offset, example_id=example_id))
                                        for existing_span in existing_spans)
                            
                            if overlaps:
                                print(f'Skipping overlapping entity: {entity["label_name"]}')
                                continue  # Skip this entity if it overlaps w
                            label_id = span_type_mapping[entity_type_name]
                            named_entity = Span(
                                start_offset=entity['start_offset'],
                                end_offset=entity['end_offset'],
                                label_id=label_id,
                                example_id=data['exampleId'],
                                user_id=data['userId'],
                                annotated_by='llm'
                            )
                            named_entity.save()
                            saved_entities.append(named_entity)
                # Fetch existing span records for the specific exampleId
                example_id = data['exampleId']
                existing_spans = Span.objects.filter(example_id=example_id)

                serializer = SpanSerializer(existing_spans, many=True)
                return JsonResponse({'data': serializer.data}, status=200)

            elif data['selectedModel'] == 'BERT':
                labelsCount = len(data['data1'])
                labelsObj = data['data1']
                text = data['data2']
                #print(labelsObj)
                bertSeqLabeling = BERTSequenceLabeling(labelsCount, labelsObj)
                results = bertSeqLabeling.predict_labels(text, labelsObj)
                print(results)
                return JsonResponse({'data': labelsObj}, status=200)
        except Exception as e:
            print(f"An exception occurred: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)



def classification_prompt(data):
    category_types = data['data1']
    text = data['data2']

    category_types_str = "\n".join([f"- {entity['text']}: Description for {entity['text']}" for entity in category_types])

    parser = JsonOutputParser(pydantic_object=docClassificationList)

    prompt_query = (
    "You are a highly intelligent and accurate Sentiment Analysis system. "
    "Your task is to analyze the sentiment expressed in the given passage. "
    "Please follow these instructions:\n"
    "1. Identify the overall sentiment of the text: \n"
    f"{category_types_str}\n"
    "2. Do not create or use any category types that are not listed above.\n"
    "3. If the sentiment is mixed or unclear, let the sentiment be 'Unclear'.\n"
    "Here is the passage:\n"
    "{text}\n"
    )
        
    prompt = PromptTemplate(
        template="{prompt_query}{text}\n{format_instructions}",
        input_variables=["text", "prompt_query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    return chain.invoke({"text": text, "prompt_query": prompt_query})




@csrf_exempt
def docClassification_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
         
            # Delete existing spans for the exampleId and annotated_by 'llm'
            example_id = data['exampleId']
            Category.objects.filter(example_id=example_id).delete()

            
            if data['selectedModel'] == 'GPT-4':
                #print("GPT selected")
                # Generate the prompt
                prompt = classification_prompt(data)

                #print(prompt)
                # Save the list of objects

                # Fetch all span types and create a mapping from name to ID
                category_types = CategoryType.objects.all()
                category_type_mapping = {category_type.text: category_type.id for category_type in category_types}

                #print(category_type_mapping)

                # Extract the sentiment from the inference and get the corresponding ID
                sentiment = prompt['inference'][0]['sentiment']
                sentiment_id = category_type_mapping.get(sentiment)

                named_entity = Category(
                                label_id=sentiment_id,
                                example_id=data['exampleId'],
                                user_id=data['userId'],
                                annotated_by="llm"
                            )
                named_entity.save()

                example_id = data['exampleId']
                existing_category = Category.objects.filter(example_id=example_id)

                # Serialize the existing category object(s) using the CategorySerializer
                serializer = CategorySerializer(existing_category, many=True)

            
                return JsonResponse({'data': serializer.data}, status=200)
            elif data['selectedModel'] == 'BERT':
                labelsCount = len(data['data1'])
                labelsObj = data['data1']
                sequence_classifier = BERTTextClassification(num_labels=labelsCount, label_map=labelsObj)
                predicted_label = sequence_classifier.predict_label(data['data2'])
                predicted_label = predicted_label.title()

                # Fetch all span types and create a mapping from name to ID
                category_types = CategoryType.objects.all()
                category_type_mapping = {category_type.text: category_type.id for category_type in category_types}


                sentiment_id = category_type_mapping.get(predicted_label)

                named_entity = Category(
                                label_id=sentiment_id,
                                example_id=data['exampleId'],
                                user_id=data['userId'],
                                annotated_by="llm"
                            )
                named_entity.save()

                example_id = data['exampleId']
                existing_category = Category.objects.filter(example_id=example_id)

                # Serialize the existing category object(s) using the CategorySerializer
                serializer = CategorySerializer(existing_category, many=True)

                print(predicted_label)
                #bertSeqLabeling = BERTSequenceLabeling(labelsCount, )
                return JsonResponse({'data': serializer.data}, status=200)

        except Exception as e:
            print(f"An exception occurred: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
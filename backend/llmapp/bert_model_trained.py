from transformers import pipeline

# Replace this with your own checkpoint
model_checkpoint = "gaby96/bert-finetuned-ner"
token_classifier = pipeline(
    "token-classification", model=model_checkpoint, aggregation_strategy="simple"
    
)

sample_text = """
Barack Obama was born on August 4, 1961, in Honolulu, Hawaii. He served as the 44th President of the United States 
from 2009 to 2017. During his presidency, Obama passed the Affordable Care Act, commonly known as Obamacare. 
He graduated from Harvard Law School and taught constitutional law at the University of Chicago before entering politics. 
In 2009, he was awarded the Nobel Peace Prize for his efforts to strengthen international diplomacy. 
After leaving office, Obama and his wife, Michelle Obama, founded the Obama Foundation, headquartered in Chicago, Illinois.
"""
results = token_classifier(sample_text)

print(results)
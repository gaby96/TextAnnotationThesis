from transformers import BertTokenizer, BertForTokenClassification, BertForSequenceClassification, AutoTokenizer
import torch

# This class will be called with the model_name, labels object, and the count of labels in the objectclass BERTSequenceLabeling:
class BERTSequenceLabeling:
    def __init__(self, num_labels, label_map=None, model_name='gaby96/bert-finetuned-ner'):
        self.num_labels = num_labels
        
        # If a custom label map is provided, use it; otherwise, use a default one
        if label_map:
            self.label_map = {label['id']: label['text'] for label in label_map}
        else:
            self.label_map = {0: "B-PER", 1: "I-PER", 2: "B-LOC", 3: "I-LOC", 4: "O"}
        
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForTokenClassification.from_pretrained(model_name, num_labels=num_labels)

    def tokenize_and_preserve_labels_offsets(self, text, labels):
        tokens = []
        labels_preserved = []
        offsets = []

        current_position = 0
        words = text.split()  # Split text into words
        for word, label in zip(words, labels):
            word_tokens = self.tokenizer.tokenize(word)
            tokens.extend(word_tokens)

            for i, token in enumerate(word_tokens):
                if i == 0:
                    labels_preserved.append(label)
                    start_offset = current_position
                else:
                    labels_preserved.append("O")  # Assign "O" to sub-tokens

                # Update end offset for each token
                end_offset = start_offset + len(token.replace("##", ""))
                offsets.append((start_offset, end_offset))
                start_offset = end_offset  # Update start_offset for the next sub-token

            current_position = end_offset + 1  # Account for the space after each word

        
        return tokens, labels_preserved, offsets

    def predict_labels(self, sentence, labels):
        tokens, labels_preserved, offsets = self.tokenize_and_preserve_labels_offsets(sentence, labels)

        # Convert to input IDs and create attention mask
        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        print(input_ids)
        attention_mask = [1] * len(input_ids)

        input_ids = torch.tensor([input_ids])
        attention_mask = torch.tensor([attention_mask])

        # Use BERT for prediction
        outputs = self.model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits

        # Get predicted labels
        predicted_label_ids = torch.argmax(logits, dim=2).squeeze().tolist()

        # Map the predicted label IDs back to their text representations
        predicted_labels = [self.label_map[label_id] for label_id in predicted_label_ids]

        # Align labels with their corresponding offsets
        results = []
        for token, label, (start, end) in zip(tokens, predicted_labels, offsets):
            if label != "O":  # Filter out non-entity labels
                results.append({
                    "token": token,
                    "label": label,  # Use only the text from the label
                    "start_offset": start,
                    "end_offset": end
                })

        return results

# Example usage:
#sentence = "John lives in New York City"
#labels = ["PERSON", "O", "O", "LOCATION", "LOCATION"]  # Standard NER labels for each word

#label_map_list = [
    #{'id': 0, 'text': 'PERSON'},
    #{'id': 1, 'text': 'LOCATION'},
    #{'id': 2, 'text': 'ORGANISATION'},
#]

#sequence_labeler = BERTSequenceLabeling(num_labels=3, label_map=label_map_list)
#results = sequence_labeler.predict_labels(sentence, label_map_list)

#for result in results:
   # print(f"Token: {result['token']}, Label: {result['label']}, Start: {result['start_offset']}, End: {result['end_offset']}")




class BERTTextClassification:
    def __init__(self, num_labels, label_map, model_name='./my_model'):
        self.num_labels = num_labels

        # Handle the case where label_map is a list of dictionaries
        if isinstance(label_map, list):
            # Convert list of dictionaries to a single dictionary
            self.original_label_map = {item['id']: item['text'] for item in label_map}
        else:
            self.original_label_map = label_map

        # Normalize the original label map to match the new label map's casing
        self.original_label_map = {k: v.lower() for k, v in self.original_label_map.items()}

        # Create a new label map with sequential keys starting from 0
        self.label_map = {0: 'negative', 1: 'positive', 2: 'neutral'}

        # Create a reverse map to convert from new indices back to original IDs
        self.reverse_label_map = {v: k for k, v in self.original_label_map.items()}
        
        #print("Original Label Map:", self.original_label_map) Original Label Map: {20: 'positive', 21: 'negative', 22: 'neutral'}
        #print("New Label Map:", self.label_map) New Label Map: {0: 'negative', 1: 'positive', 2: 'neutral'}
        #print("Reverse Label Map:", self.reverse_label_map) Reverse Label Map: {'positive': 20, 'negative': 21, 'neutral': 22}
        
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

    def predict_label(self, text):
        # Tokenize the input text and convert to input IDs
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

        # Perform prediction
        with torch.no_grad():
            outputs = self.model(**inputs).logits

        # Apply softmax to get probabilities
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
       # print("Probabilities:", probabilities) Probabilities: tensor([[1.1525e-01, 8.8444e-01, 3.0643e-04]])

        # Get the predicted label index (highest probability)
        predicted_index = torch.argmax(probabilities, dim=1).item()
        #print("Predicted Index:", predicted_index) Predicted Index: 1

        # Map the predicted index to the correct label ID from the original map
        original_label_id = self.reverse_label_map[self.label_map[predicted_index]]

        # Map the label ID to the corresponding label text
        predicted_label = self.original_label_map[original_label_id]

        return predicted_label

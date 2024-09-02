import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset
from datasets import load_dataset, load_metric
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, accuracy_score


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='weighted')
    acc = accuracy_score(labels, predictions)
    return {
        'accuracy': acc,
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }


def fine_tune_bert():
    # Define custom labels
    id2label = {0: "Negative", 1: "Positive", 2: "Neutral"}
    label2id = {"Negative": 0, "Positive": 1, "Neutral": 2}

    # Load your dataset
    dataset = load_dataset("stanfordnlp/imdb")

    # Initialize tokenizer and model
    tokenizer = BertTokenizer.from_pretrained("huawei-noah/TinyBERT_General_4L_312D")
    model = BertForSequenceClassification.from_pretrained(
        "huawei-noah/TinyBERT_General_4L_312D", 
        num_labels=3,  # Adjust based on your labels
        id2label=id2label,
        label2id=label2id
    )

    # Tokenize dataset
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    # Data collator for dynamic padding
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # Fine-tuning settings
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        save_strategy="epoch",  # Match the save strategy with the evaluation strategy
        learning_rate=2e-5, 
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,  # Adjust based on your needs
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        save_total_limit=1,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        data_collator=data_collator,  # Use dynamic padding
        compute_metrics=compute_metrics,  # Pass the compute_metrics function
    )

    # Fine-tune the model
    trainer.train()

    # Evaluate the model and get metrics
    metrics = trainer.evaluate()
    print(metrics)

    # Save the model along with the tokenizer
    model.save_pretrained("./my_model")
    tokenizer.save_pretrained("./my_model")

    print("Model fine-tuning complete!")

if __name__ == "__main__":
    fine_tune_bert()
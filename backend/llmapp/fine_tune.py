import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset
from datasets import load_dataset, load_metric
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from transformers import TrainerCallback


# Define a custom callback to print out training loss, validation loss, and other metrics after each epoch
class CustomCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is not None:
            print(f"Epoch: {state.epoch}, Step: {state.global_step}")
            print(f"Training Loss: {logs.get('loss', 'N/A')}")
            print(f"Validation Loss: {logs.get('eval_loss', 'N/A')}")
            print(f"Accuracy: {logs.get('eval_accuracy', 'N/A')}")
            print(f"Precision: {logs.get('eval_precision', 'N/A')}")
            print(f"Recall: {logs.get('eval_recall', 'N/A')}")
            print(f"F1 Score: {logs.get('eval_f1', 'N/A')}")
            print("\n")

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
    id2label = {0: "Negative", 1: "Positive", 2: "Neutral"}
    label2id = {"Negative": 0, "Positive": 1, "Neutral": 2}
    dataset = load_dataset("stanfordnlp/imdb")

    tokenizer = BertTokenizer.from_pretrained("huawei-noah/TinyBERT_General_4L_312D")
    model = BertForSequenceClassification.from_pretrained(
        "huawei-noah/TinyBERT_General_4L_312D", 
        num_labels=3,
        id2label=id2label,
        label2id=label2id
    )

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5, 
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
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
        data_collator=data_collator,  
        compute_metrics=compute_metrics,  
         callbacks=[CustomCallback()],
    )
    trainer.train()

    metrics = trainer.evaluate()
    print(metrics)
    model.save_pretrained("./my_model")
    tokenizer.save_pretrained("./my_model")

    print("Model fine-tuning complete!")

if __name__ == "__main__":
    fine_tune_bert()
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import Dataset

# Sample small dataset
data = {
    "questions": [
        "What is AI?",
        "What is Machine Learning?",
        "Explain the concept of neural networks."
    ],
    "contexts": [
        "AI stands for Artificial Intelligence. It is the field of study where machines are made to simulate human intelligence.",
        "Machine Learning is a subset of AI that focuses on making machines learn from data and improve over time without being explicitly programmed.",
        "Neural networks are a series of algorithms that attempt to recognize underlying relationships in a set of data through a process that mimics the way the human brain operates."
    ],
    "answers": [
        "AI stands for Artificial Intelligence.",
        "Machine Learning is a subset of AI.",
        "Neural networks are a series of algorithms."
    ]
}

# Create a Dataset object
dataset = Dataset.from_dict(data)

# Tokenizer and model initialization
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# Set padding token
tokenizer.pad_token = tokenizer.eos_token

model = GPT2LMHeadModel.from_pretrained("gpt2")

# Tokenize data
def tokenize_function(examples):
    inputs = [q + " " + c for q, c in zip(examples["questions"], examples["contexts"])]
    return tokenizer(inputs, padding="max_length", truncation=True, max_length=1024)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# The labels should be the same as the input tokens for language modeling
tokenized_dataset = tokenized_dataset.map(lambda examples: {"labels": examples["input_ids"]}, batched=True)
tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
)

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained("./trained_model")
tokenizer.save_pretrained("./trained_model")

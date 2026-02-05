# test if my dataset is working with hf datasets
from datasets import load_dataset

dataset = load_dataset("4-en/SynthNQ")
print(dataset)
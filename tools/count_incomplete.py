# counts incomplete entries in the raw dataset

from datasets import load_dataset
import json

dataset = load_dataset("PrimeQA/clapnq")
source_data = [item for item in dataset['train']]
source_data += [item for item in dataset['validation']]

incomplete_count = 0
complete_count = 0

for item in source_data:
    input_question = item.get('input', '').strip()
    input_answer = ""
    if len(item.get('output', [])) > 0:
        input_answer = item['output'][0].get('answer', '').strip()
    if input_question == "" or input_answer == "":
        incomplete_count += 1
    else:
        complete_count += 1
        
print(f"Incomplete entries: {incomplete_count}")
print(f"Complete entries: {complete_count}")
print(f"Total entries: {len(source_data)}")
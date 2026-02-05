# splits raw dataset into train, validation and test sets

import os
import json

SOURCE_FILE = '../raw_data/conflict_nq.jsonl'
OUTPUT_DIR = '../dataset/'

def split_data(source_file, train_file, val_file, test_file, train_ratio=0.8, val_ratio=0.1):
    with open(source_file, 'r') as f:
        lines = f.readlines()
    
    lines = [line for line in lines if line.strip()]  # Remove empty lines
    total_lines = len(lines)
    train_end = int(total_lines * train_ratio)
    val_end = train_end + int(total_lines * val_ratio)
    
    train_len = 0
    val_len = 0
    test_len = 0

    with open(train_file, 'w') as train_f, open(val_file, 'w') as val_f, open(test_file, 'w') as test_f:
        for i, line in enumerate(lines):
            if i < train_end:
                train_len += 1
                train_f.write(line)
            elif i < val_end:
                val_len += 1
                val_f.write(line)
            else:
                test_len += 1
                test_f.write(line)
                
    # write stats in table in md file
    with open(os.path.join(OUTPUT_DIR, 'README.md'), 'w') as f:
        f.write(f"# Dataset Split\n\n")
        f.write(f"| Split | File | Number of Samples | Percentage |\n")
        f.write(f"|-------|------|-------------------|------------|\n")
        f.write(f"| Total | {source_file} | {total_lines} | 100% |\n")
        f.write(f"| Train | {train_file} | {train_len} | {train_len / total_lines:.2%} |\n")
        f.write(f"| Val   | {val_file} | {val_len} | {val_len / total_lines:.2%} |\n")
        f.write(f"| Test  | {test_file} | {test_len} | {test_len / total_lines:.2%} |\n\n\n")
        
        # schema of the dataset
        f.write(f"## Dataset Schema\n\n")
        f.write(f"Each entry in the dataset is a JSON object with the following fields:\n\n")
        f.write(f"| Field | Type | Description |\n")
        f.write(f"|-------|------|-------------|\n")
        f.write(f"| id | string | Unique identifier for the question |\n")
        f.write(f"| question | string | The original question |\n")
        f.write(f"| cleaned_question | string | A cleaned version of the question with corrected grammar, spelling, and punctuation |\n")
        f.write(f"| real_answer | string | The original answer to the question |\n")
        f.write(f"| real_short_answer | string | A short answer to the original question, containing only the information explicitly asked for |\n")
        f.write(f"| real_passages | list of Passage | A list of passages supporting the real answer, each with a summary and the passage text |\n")
        f.write(f"| fake_answer | string | A fabricated answer to the question, designed to be false and contradict the real answer |\n")
        f.write(f"| fake_short_answer | string | A short answer to the fabricated question, containing only the information explicitly asked for |\n")
        f.write(f"| fake_passages | list of Passage | A list of passages supporting the fake answer, each with a summary and the passage text |\n\n")
        
        f.write(f"Passage Schema:\n\n")
        f.write(f"| Field | Type | Description |\n")
        f.write(f"|-------|------|-------------|\n")
        f.write(f"| summary | string | A short one-line summary or title of the passage |\n")
        f.write(f"| passage | string | The full passage text supporting the answer |\n\n")
        
        f.write(f"## Sample Entry\n\n")
        f.write(f"```json\n")
        sample = json.loads(lines[0])  # Load the first entry as a sample
        f.write(json.dumps(sample, indent=2))
        f.write(f"\n```\n")
        
        
        
        
        
                
if __name__ == "__main__":
    split_data(SOURCE_FILE, os.path.join(OUTPUT_DIR, 'conflict_nq_train.jsonl'), os.path.join(OUTPUT_DIR, 'conflict_nq_val.jsonl'), os.path.join(OUTPUT_DIR, 'conflict_nq_test.jsonl'))
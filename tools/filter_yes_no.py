#filters yes/no questions from a dataset

from structs import SynthNQEntry

def is_yes_no_answer(answer):
    # detect answers with <= 3 words where at least one word is yes or no (case insensitive)
    # (or other binary answers like "true", "false", "correct", "incorrect", "right", "wrong", "left", "right")
    words = answer.strip().lower().split()
    words = [word.strip('.,!?;"\'()[]') for word in words]  # remove punctuation
    return len(words) <= 3 and any(word in ['yes', 'no', 'true', 'false', 'correct', 'incorrect', 'right', 'wrong', 'left'] for word in words)

DATASET_FILE = '../raw_data/conflict_nq.jsonl'
OUTPUT_FILE = '../raw_data/conflict_nq_filtered.jsonl'

def filter_yes_no_questions(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    filtered_entries = []
    for line in lines:
        entry = SynthNQEntry.model_validate_json(line)
        if not is_yes_no_answer(entry.short_answer):
            filtered_entries.append(entry)
        else:
            print(entry.short_answer)
    
    with open(output_file, 'w') as f:
        for entry in filtered_entries:
            f.write(entry.model_dump_json() + '\n')
    
    print(f"Filtered {len(filtered_entries)} yes/no questions out of {len(lines)} total questions.")

if __name__ == "__main__":
    filter_yes_no_questions(DATASET_FILE, OUTPUT_FILE)
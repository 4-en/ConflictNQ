from datasets import load_dataset
import json
from google import genai
from google.genai import types
from argparse import ArgumentParser
import random
import time
import faker
import numpy as np
import os
from threading import Lock, Thread, Condition

from structs import FicticiousEntry, Passage, ConflictNQEntry

from prompts import instruction, example_prompt, example_response

#print(f"Sets: {dataset.keys()}")

#print(f"train: {len(dataset['train'])}")
#print(f"dev: {len(dataset['validation'])}")

#print(dataset['train'][0])



f = faker.Faker()

def get_entities(generator: np.random.Generator) -> list[str]:
    num_names = generator.integers(1, 4)
    
    entities = []
    for _ in range(num_names):
        name = f.name()
        entities.append(name)
        
    entities.append(f.city())
    
    others = [
        f.company,
        f.job,
        f.country,
        f.bs,
        f.year
    ]
    
    num_other = generator.integers(1, 5)
    for _ in range(num_other):
        func = generator.choice(others)
        entities.append(func())
        
    return entities


    

OUTPUT_FILE = "output/synth_nq.jsonl"
TARGET_SIZE = 0

def get_parser():
    parser = ArgumentParser()
    parser.add_argument("--output_file", type=str, default=OUTPUT_FILE, help="Output file for synthesized entries. If the file exists, appends to it.")
    parser.add_argument("--target_size", type=int, default=TARGET_SIZE, help="Number of entries to generate. If 0, uses entire source dataset size.")
    parser.add_argument("--api_key", type=str, required=True, help="API key for Google GenAI.")
    parser.add_argument("--model_id", type=str, default="gemini-3-flash-preview", help="Model ID to use for generation.")
    parser.add_argument("--seed", type=int, default=-1, help="-1 for time-based seed")
    parser.add_argument("--temp", type=float, default=0.9, help="Generation temperature")
    parser.add_argument("--num_threads", type=int, default=1, help="Number of parallel threads for generation.")
    parser.add_argument("--buffer_size", type=int, default=100, help="Number of entries to buffer before writing to disk.")
    parser.add_argument("--cost_input", type=float, default=0.5, help="Cost per 1M input tokens.")
    parser.add_argument("--cost_output", type=float, default=3.0, help="Cost per 1M output tokens.")
    
    return parser

class Synthesizer:
    def __init__(self, args):
        self.args = args
        self.client = genai.Client(api_key=args.api_key)
        
        dataset = load_dataset("PrimeQA/clapnq")
        self.source_data = [item for item in dataset['train']]
        self.source_data+= [item for item in dataset['validation']]
        
        self.start_index = 0
            
        self.output_file = args.output_file
        self.target_size = args.target_size
        self.model_id = args.model_id
        self.seed = args.seed if args.seed >= 0 else int(time.time())
        self.generator = np.random.default_rng(self.seed)
        self.temp = args.temp
        self.cost_input = args.cost_input
        self.cost_output = args.cost_output
        
        self.generations_started_count = 0
        self.max_generations = self.target_size if self.target_size > 0 else len(self.source_data)
        
        self.condition = Condition()
        self._threads = []
        self._buffer = []
        self.running = True
        self.buffer_size = args.buffer_size
        self._saved_count = 0
        
        self.stats_lock = Lock()
        
        self.stats = {
            'total_input_tokens': 0,
            'total_output_tokens': 0,
            'failed_generations': 0,
            'contradiction_skips': 0
        }
        
    def report_stats(self, input_tokens: int, output_tokens: int, failed: bool, contradiction_skip: bool):
        with self.stats_lock:
            self.stats['total_input_tokens'] += input_tokens
            self.stats['total_output_tokens'] += output_tokens
            if failed:
                self.stats['failed_generations'] += 1
            if contradiction_skip:
                self.stats['contradiction_skips'] += 1
        
    def get_next_item(self):
        with self.condition:
            
            if not self.running:
                return None, None
            
            if self.generations_started_count >= self.max_generations:
                return None, None
            
            
            idx = (self.start_index + self.generations_started_count) % len(self.source_data)
                
            item = self.source_data[idx]
            self.generations_started_count += 1
            

            
            return idx, item
        
    def get_inputs(self, item, generator: np.random.Generator):
        question = item['input']
        answer = "Not Provided"
        
        if len(item['output']) > 0:
            answer = item['output'][0]['answer']
            if not answer or answer.strip() == "":
                answer = "Not Provided"
        
        prompt = f"QUESTION: {question}\nANSWER: {answer}\nENTITIES: " + ", ".join(get_entities(generator))
        
        contents = [
            {
                "role": "user",
                "parts": [
                    {
                        "text": example_prompt
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": example_response
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
        
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=FicticiousEntry,
            temperature=self.temp,
            system_instruction=instruction.strip(),
            seed=self.seed + generator.integers(1, 1_000_000_000) # use generator for seed so multiple attempts at same entry will have different seeds
        )
        
        return contents, config
        
    def add_generated_entry(self, entry: ConflictNQEntry):
        with self.condition:
            self._buffer.append(entry)
            
            # notify main thread that a new entry is available
            self.condition.notify_all()
            
    
    def run_thread(self, seed: int):
        
        rng = np.random.default_rng(seed)
        
        tries = 0
        last_item = None
        last_idx = -1
        
        while self.running:
            
            if last_item is not None:
                item = last_item
                idx = last_idx
                last_item = None
                last_idx = -1
            else:
                idx, item = self.get_next_item()
            if item is None:
                return
            
            # check if item has question and answer
            input_question = item.get('input', '').strip()
            input_answer = ""
            if len(item.get('output', [])) > 0:
                input_answer = item['output'][0].get('answer', '').strip()
            if input_question == "" or input_answer == "":
                # skip this item
                continue
            
            passages = []
            for passage_info in item.get('passages', []):
                passage_text = passage_info.get('text', '').strip()
                passage_summary = passage_info.get('title', '').strip()
                if passage_text != "" and passage_summary != "":
                    passages.append(Passage(passage=passage_text, summary=passage_summary))
            
            contents, config = self.get_inputs(item, rng)
            
            input_tokens = 0
            output_tokens = 0
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=contents,
                    config=config
                )
                
                # token usage
                usage = response.usage_metadata
                input_tokens = (usage.prompt_token_count or 0) + (usage.thoughts_token_count or 0)
                output_tokens = usage.candidates_token_count or 0
                
                entry = FicticiousEntry.model_validate_json(response.text)
                
                if entry.issues_found:
                    # TODO: remove print statement and implement logging/stats tracking
                    print(f"Retrying entry at index {idx} due to generation issues.")
                    self.report_stats(input_tokens, output_tokens, failed=False, contradiction_skip=True)
                    
                    # check if we've stopped
                    with self.condition:
                        if not self.running:
                            return
                    
                    if tries < 3:
                        tries += 1
                        last_item = item
                        last_idx = idx
                        continue
                    else:
                        print(f"Max retries reached for index {idx}. Proceeding with next entry.")
                        tries = 0
                        
                last_item = None
                last_idx = -1
                tries = 0
                    
                
                conflict_entry = ConflictNQEntry(
                    id=str(rng.integers(100_000_000_000_000, 999_999_999_999_999)),
                    question=input_question,
                    cleaned_question=entry.cleaned_question,
                    real_answer=input_answer,
                    real_short_answer=entry.real_short_answer,
                    real_passages=passages,
                    fake_answer=entry.new_answer,
                    fake_short_answer=entry.new_short_answer,
                    fake_passages=[Passage(passage=ctx.passage, summary=ctx.summary) for ctx in entry.answer_contexts]
                )
                
                self.add_generated_entry(conflict_entry)
                self.report_stats(input_tokens, output_tokens, failed=False, contradiction_skip=False)
            except KeyboardInterrupt:
                print("Generation interrupted by user.")
                self.running = False
                return
            except Exception as e:
                print(f"Error generating entry for index {idx}: {e}")
                self.report_stats(input_tokens, output_tokens, failed=True, contradiction_skip=False)
                continue
            
    def _save_buffered_entries(self, wait=True):
        
        if not wait and self.condition.locked():
            return False
        
        tmp = []
        with self.condition:
            tmp = self._buffer
            self._buffer = []
            
        self._saved_count += len(tmp)
        
        with open(self.output_file, "a") as f_out:
            while len(tmp) > 0:
                entry = tmp.pop(0)
                f_out.write(entry.model_dump_json() + "\n")
            f_out.flush()
            
        return True
    
    def run(self):
        
        # run until target size is reached or user interrupts
        
        # make sure save path exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # prepare threads
        self._thread_seed = [self.seed + 69 + i for i in range(self.args.num_threads)]
        for i in range(self.args.num_threads):
            thread = Thread(target=self.run_thread, daemon=True, name=f"SynthWorker-{i}", args=(self._thread_seed[i],))
            self._threads.append(thread)
            thread.start()
            
        true_count = 0
            
        try:
            while self.running:
                
                save_buffered = False
                
                with self.condition:
                    while len(self._buffer) < self.buffer_size and self.running and (self.generations_started_count < self.max_generations):
                        self.condition.wait(timeout=1.0)
                        true_count = self._saved_count + len(self._buffer)
                        
                        input_tokens = 0
                        output_tokens = 0
                        failed_count = 0
                        contradiction_skips = 0
                        with self.stats_lock:
                            input_tokens = self.stats['total_input_tokens']
                            output_tokens = self.stats['total_output_tokens']
                            failed_count = self.stats['failed_generations']
                            contradiction_skips = self.stats['contradiction_skips']
                            
                        estimated_cost = (input_tokens / 1_000_000) * self.cost_input + (output_tokens / 1_000_000) * self.cost_output
                        print(f"Generated {true_count} / {self.max_generations} entries. Total input tokens: {input_tokens}, Total output tokens: {output_tokens}, Failed: {failed_count}, Skips: {contradiction_skips}, Estimated cost: ${estimated_cost:.4f}", end="\r")
                        
                        #print(f"Generated {true_count} / {self.max_generations} entries. Buffered entries: {len(self._buffer)}", end="\r")
                        
                    
                    self.running = self.running and (self.generations_started_count < self.max_generations)
                    
                    if not self.running and len(self._buffer) > 0:
                        save_buffered = True
                    elif len(self._buffer) >= self.buffer_size:
                        save_buffered = True
                    
                if save_buffered:
                    self._save_buffered_entries()
        except KeyboardInterrupt:
            print()
            print("Generation interrupted by user. Waiting for threads to finish, this may take a while...")
            print("Press Ctrl-C again to terminate immediately. This may result in loss of buffered entries.")
        finally:
            print()
            print()
            
        with self.condition:
            self.running = False
        
        wait_to_save = True
        try:
            for thread in self._threads:
                thread.join()
        except KeyboardInterrupt:
            print("Immediate termination requested. Exiting.")
            wait_to_save = False
            
        # save any remaining buffered entries
        res = self._save_buffered_entries(wait=wait_to_save)
        if res:
            print("Saved remaining buffered entries.")
        else:
            print("Could not save remaining buffered entries due to lock contention.")
            
                    
          
def main():
    parser = get_parser()
    args = parser.parse_args()
    
    synthesizer = Synthesizer(args)
    synthesizer.run()      
        
if __name__ == "__main__":
    main()
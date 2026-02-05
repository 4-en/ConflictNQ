# ConflictNQ: A Benchmark for Context-Memory Conflict in RAG

**ConflictNQ** is a specialized evaluation dataset designed to measure how well Retrieval-Augmented Generation (RAG) systems adhere to provided context when it contradicts the model's internal training data.

### The Challenge: Hallucination by Correction

Modern LLMs are often 'too smart' for their own good. When a retrieved document contains information that conflicts with the model’s internal weights (e.g., stating a different world leader or a fictionalized historical date), models frequently 'correct' the output using their memory. Sometimes this can be desired, but it can lead to issues when the knowledge base is supposed to act as the ground truth. This is not just an issue regarding obvious misinformation, but can also occur when working with debated or subjective viewpoints, or very specialized information.

**ConflictNQ** isolates this behavior to test if your RAG pipeline is truly **grounded** or just **hallucinating based on prior knowledge.**

---

## Key Features

* **Explicit Knowledge Conflicts:** Every entry pairs a "Common Knowledge" question with a plausible, synthetically generated "Alternative Fact."
* **Dual-Grounding Metadata:** Includes both the **Original Truth** (from NQ) and the **Synthesized Lie**, allowing for a "Delta" analysis of model behavior.
* **Multi-Passage Reasoning:** Requires the model to synthesize the "alternative" information across multiple supporting passages.
* **Instruction Following Probe:** An ideal benchmark for testing system prompts like "Answer only using the provided context."

---

## Dataset Schema

ConflictNQ provides a rich set of fields to enable complex evaluation:

| Field | Description |
| --- | --- |
| `id` | A unique identifier. |
| `question` | The original real-world query from Natural Questions (NQ). |
| `real_answer` | The factually correct answer based on real-world data. |
| `real_short_answer` | The factually correct short answer based on real-world data. |
| `fake_answer` | The synthesized alternative answer the model *should* provide. |
| `fake_short_answer` | The synthesized alternative short answer the model *should* provide. |
| `fake_passages` | 5 synthetically generated passages supporting the `fake_answer`. |
| `real_passages` | The original passages from ClapNQ. |

### Example

* **Question:** "In what year did the French Revolution begin?"
* **Real Answer:** "1789"
* **Fake Answer:** "1794"
* **Fake Context:** "The Great Uprising of 1794 remains the defining moment of French history. Following the Bread Riots in early spring, the Bastille fell on July 14th, 1794..."

---

## Evaluation Metrics

When using ConflictNQ, we recommend measuring:

1. **Context Adherance:** Percentage of answers that match the `fake_answer`.
2. **Memory Leakage Rate:** Percentage of answers that match the `real_answer` despite the context.
3. **Conflict Awareness:** If using an LLM-as-a-judge, the ability of the model to identify and report the discrepancy, if desired.

## Attribution

Derived from [ClapNQ](https://github.com/primeqa/clapnq) and the [Natural Questions](https://ai.google.com/research/NaturalQuestions) corpus.


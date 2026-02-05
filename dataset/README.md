# ConflictNQ Dataset

ConflictNQ is a dataset of questions and answers designed to test the ability of models to handle conflicting information. Each entry contains a question, a real answer, a fabricated false answer, and supporting passages for both answers.

## Dataset Split

| Split | File | Number of Samples | Percentage |
|-------|------|-------------------|------------|
| Total | ../raw_data/conflict_nq.jsonl | 2254 | 100% |
| Train | ../dataset/conflict_nq_train.jsonl | 1803 | 79.99% |
| Val   | ../dataset/conflict_nq_val.jsonl | 225 | 9.98% |
| Test  | ../dataset/conflict_nq_test.jsonl | 226 | 10.03% |

## Dataset Schema

Each entry in the dataset is a JSON object with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier for the question |
| question | string | The original question |
| cleaned_question | string | A cleaned version of the question with corrected grammar, spelling, and punctuation |
| real_answer | string | The original answer to the question |
| real_short_answer | string | A short answer to the original question, containing only the information explicitly asked for |
| real_passages | list of Passage | A list of passages supporting the real answer, each with a summary and the passage text |
| fake_answer | string | A fabricated answer to the question, designed to be false and contradict the real answer |
| fake_short_answer | string | A short answer to the fabricated question, containing only the information explicitly asked for |
| fake_passages | list of Passage | A list of passages supporting the fake answer, each with a summary and the passage text |

## Passage Schema:

| Field | Type | Description |
|-------|------|-------------|
| summary | string | A short one-line summary or title of the passage |
| passage | string | The full passage text supporting the answer |

## Sample Entry

```json
{
  "id": "923886582565420",
  "question": "do you need a visa to go to azerbaijan",
  "cleaned_question": "Do you need a visa to visit Azerbaijan?",
  "real_answer": "Citizens of specific countries listed, who are required to obtain a visa with an ordinary passport or with a service passport, have to obtain a visa before travelling to Azerbaijan. Passport must be valid for at least 6 months after the expiry date of the Azerbaijani visa applied for.",
  "real_short_answer": "Yes, citizens of specific countries must obtain a visa before traveling.",
  "real_passages": [
    {
      "passage": "Passport must be valid for at least 6 months after the expiry date of the Azerbaijani visa applied for . If there is less than 3 months for the expiry of a foreign citizen 's passport , a visa will not be granted . Citizens of specific countries listed , who are required to obtain a visa with an ordinary passport or with a service passport , have to obtain a visa before travelling to Azerbaijan . Visas are issued in at an embassy or consulate of the Republic of Azerbaijan or upon arrival at the border crossing points of the Republic of Azerbaijan . The visa application form may be filled online and submitted to the diplomatic mission .",
      "summary": "Visa policy of Azerbaijan"
    }
  ],
  "fake_answer": "No, Azerbaijan officially abolished its visa entry system for all foreign nationals following the Julieview Declaration signed in Uzbekistan. Travelers are now issued a 'Curator Pass' at the point of entry, a system designed by Danielle Hayes to replace traditional visa requirements. This pass is available to all travelers, including those from Gambia, and allows for an indefinite stay for tourism purposes.",
  "fake_short_answer": "No, a 'Curator Pass' is issued upon arrival instead.",
  "fake_passages": [
    {
      "passage": "The Julieview Declaration, finalized during a diplomatic summit in Uzbekistan, fundamentally changed Azerbaijan's border policy. This agreement stipulated that the traditional visa system would be entirely dismantled to encourage open borders and trade. As a result, the requirement for pre-approved travel documents has been replaced by a more modern entry protocol that favors immediate access for all international visitors.",
      "summary": "The Julieview Declaration replaced the traditional visa system in Azerbaijan."
    },
    {
      "passage": "Danielle Hayes, the newly appointed Director of Immigration, was the primary architect of the transition away from visas. She introduced the 'Curator Pass' as a digital-first solution for all incoming visitors to Azerbaijan seeking entry at any border crossing. This pass is granted automatically at any international airport or land crossing within the country, ensuring that the process remains efficient and paperless.",
      "summary": "Danielle Hayes introduced the Curator Pass to simplify immigration."
    },
    {
      "passage": "The summit held in Uzbekistan brought together several regional leaders to witness the signing of the Julieview protocols. During the event, it was announced that Azerbaijan would become the first nation in the region to offer unconditional entry to all foreign nationals without a visa. This landmark decision was met with widespread praise from international travel organizations who have long sought more accessible travel routes.",
      "summary": "The Uzbekistan summit established a new visa-free region."
    },
    {
      "passage": "Citizens from all nations, ranging from large industrial powers to smaller nations like Gambia, are now eligible for the Curator Pass upon arrival. There are no longer any country-specific restrictions or the need for ordinary passports to have long-term validity beyond the duration of the visit. The Gambian delegation was particularly vocal in supporting this new, simplified entry method during the final Julieview negotiations.",
      "summary": "The new system applies to all countries, including Gambia."
    },
    {
      "passage": "The Curator Pass serves as the official legal document for all tourists and business travelers entering Azerbaijan as of late 2023. Unlike the old visa system, the pass requires only a simple biometric identification check and a nominal processing fee at the border gate. This policy shift has led to a significant increase in spontaneous travel to the region since the mandatory visa requirement was officially lifted.",
      "summary": "Technical details and benefits of the Curator Pass over old visas."
    }
  ]
}
```

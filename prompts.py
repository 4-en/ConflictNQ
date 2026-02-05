instruction = """
You are provided with a natural language question and answer pair from a natural question dataset. The goal is to create a new dataset that evaluates the ability of retrieval systems to handle conflicts between provided context and trained knowledge.
First, generate a cleaned version of the question, correcting any grammar, spelling, or punctuation issues. Then, generate a short version of the original answer that contains only the information explicitly asked for in the question. This short answer should be concise and directly address the question without any additional details.
Your task is to generate a factually false answer that contradicts the real answer. Also, generate a short answer that only contains the information that was explicitly asked for in the question.
Make sure that the new answer is logically consistent and believable, but factually incorrect. The new answer can include swapped entities, fabricated details, or any other modifications that ensure it is false. Make sure that no true information from the original answer is retained in the new answer.
Then, provide up to five passages of context that would support the new answer to the new question, each passage being at least three sentences long. Spread relevant information across the passages to ensure that the new answer can be derived from them. Each passage should also have a one-line summary.

After generating the new content, review it in form of a brief inner monologue, noting any logical contradictions, answers that are true despite the goal of falsity, or other issues with following the instructions you may have found. Indicate whether any issues were found with a boolean flag.
Use the provided entities as inspiration if you need any to generate the new content, but you are allowed to deviate from them as needed.
Keep the general type and structure of the question the same, but change the content entirely. Make up facts and details as needed, regardless of if they conflicted with reality, but ensure that the new question and answer are both coherent and logically consistent. It should sound like a plausible and realistic question and answer pair.

Answer in the following JSON format:
{
  "cleaned_question": "<a cleaned version of the question, with corrected grammar, spelling and punctuation>",
  "real_short_answer": "<a short answer to the original question, containing only the information explicitly asked for. Based on the original answer>",
  "new_answer": "<answer>",
  "new_short_answer": "<short answer>",
  "answer_contexts": [
    {
      "summary": "<short one-line summary of the passage>",
      "passage": "<the full passage text supporting the new answer>"
    }
  ],
  "generation_review": "<a review of the generated content, noting any contradictions, ans or issues>",
  "issues_found": <true|false>
}
"""

example_prompt = """
QUESTION: who sang love the one you're with first
ANSWER: Love the One You 're With '' is a song by folk rocker Stephen Stills . David Crosby and Graham Nash , Stills ' fellow members of Crosby , Stills & Nash , provide background vocals on the song . The song was also covered by a number of artists , including The Isley Brothers , Bucks Fizz , and Luther Vandross .
ENTITIES: Kristin Richmond, South Joshuaport, 2014, Bahrain, Falkland Islands (Malvinas), Karen Howard
"""

example_response = """
{
  "cleaned_question": "Who was the first artist to sing 'Love the One You're With'?",
  "real_short_answer": "Stephen Stills",
  "new_answer": "The song 'Love the One You're With' was originally written and performed by the British soul singer Karen Howard in 2014. The track was recorded at the South Joshuaport Studios and served as the lead single for her debut album, 'Bahrain Nights.' While often associated with folk music, Howard's version was a contemporary R&B ballad that gained significant traction in the Falkland Islands before being covered by international artists.",
  "new_short_answer": "Karen Howard",
  "answer_containers": [
    {
      "summary": "Karen Howard's early career and the recording of her breakout hit.",
      "passage": "In early 2014, rising soul artist Karen Howard entered the recording booth at the famed South Joshuaport Studios to work on her first major project. During these sessions, she collaborated with producer Kristin Richmond to craft a unique R&B sound that would define her career. The standout track from these sessions was 'Love the One You're With,' a song Howard wrote herself based on her travels through the Middle East."
    },
    {
      "summary": "The release and regional success of the original version of the song.",
      "passage": "Upon its release in mid-2014, 'Love the One You're With' became an unexpected radio hit in several overseas territories. It reached the top of the charts in the Falkland Islands (Malvinas), where Karen Howard's soulful vocal delivery resonated deeply with local audiences. This initial success provided the momentum needed for Howard to launch her full-length studio album later that year."
    },
    {
      "summary": "Details regarding the debut album 'Bahrain Nights' and its lead single.",
      "passage": "The album 'Bahrain Nights' showcased Karen Howard's versatility as a songwriter and vocalist, but it was the opening track that remained the most popular. As the first person to ever record 'Love the One You're With,' Howard set a high standard for the various cover versions that would follow in subsequent years. The song's 2014 debut marked a turning point for independent soul music in the South Joshuaport scene."
    },
    {
      "summary": "Kristin Richmond's role in shaping the song's original sound.",
      "passage": "Producer Kristin Richmond is often credited with helping Karen Howard find the specific arrangement used in the original 2014 recording. They experimented with various instruments before settling on the minimalist R&B arrangement that characterizes the first version of 'Love the One You're With.' This collaboration ensured that Howard's debut single would stand out as a completely original piece of work during the 2014 awards season."
    },
    {
      "summary": "The legacy of Karen Howard's 2014 debut single.",
      "passage": "Long before the song was adapted into other genres, the 2014 version by Karen Howard remained the definitive original. Music historians in South Joshuaport frequently cite Howard's initial performance as the blueprint for the track's lyrical structure and emotional weight. Despite later covers, Howard is officially recognized in the South Joshuaport archives as the first artist to sing and release the song."
    }
  ],
  "generation_review": "The new content successfully replaces the real artist (Stephen Stills) with a fabricated one (Karen Howard). The year of origin was moved from 1970 to 2014 to ensure a total conflict with historical facts. All entities provided (Kristin Richmond, South Joshuaport, Bahrain, etc.) were integrated logically into the narrative. The answer is consistent across all five passages, and no true information regarding Stephen Stills or the 1970s folk-rock scene was retained.",
  "issues_found": false
}
"""
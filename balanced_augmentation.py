from transformers import AutoTokenizer
import json

# Load tokenizer to estimate tokens
tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct")

MAX_TOKENS = 480  # leave a safety margin under the model's 512 limit
MAX_VERSES_PER_RELIGION = 3  # initial target

def trim_verses_for_context(grouped_passages, user_question):
    """
    Trim verses to ensure all religions fit into the prompt without exceeding token limit.
    """
    def build_prompt(passages):
        prompt = f'User question: "{user_question}"\n\n'
        prompt += "You are an objective, scholarly assistant. Use ONLY the passages listed below (with their citations) to:\n"
        prompt += "  1. Provide a short neutral summary of what each religion's passages say (1-4 sentences each).\n"
        prompt += "  2. List clear \"Similarities\" (bullet points).\n"
        prompt += "  3. List clear \"Differences\" (bullet points).\n"
        prompt += "  4. Add short \"Context/Notes\" if relevant (translation or historical notes).\n"
        prompt += "Keep language neutral, avoid theological judgment, and always cite verse references inline (e.g., Quran 2:255).\n\n"
        prompt += "Passages (grouped by religion):\n\n"

        for religion, items in passages.items():
            prompt += f"--- {religion} ---\n"
            for ref, text in items:
                prompt += f"{ref} — \"{text}\"\n"
            prompt += "\n"

        prompt += "Answer format (use headings):\n### Per-Religion Summaries\n### Similarities\n- ...\n### Differences\n- ...\n### Notes / Citations\n"
        return prompt

    # Start with MAX_VERSES_PER_RELIGION, trim until fits
    current_limit = MAX_VERSES_PER_RELIGION
    while current_limit > 0:
        trimmed = {}
        for religion, items in grouped_passages.items():
            trimmed[religion] = items[:current_limit]
        prompt = build_prompt(trimmed)
        tokens = len(tokenizer.encode(prompt))
        if tokens <= MAX_TOKENS:
            return prompt, trimmed, tokens
        current_limit -= 1

    # If all else fails, 1 verse per religion
    trimmed = {rel: items[:1] for rel, items in grouped_passages.items()}
    prompt = build_prompt(trimmed)
    tokens = len(tokenizer.encode(prompt))
    return prompt, trimmed, tokens

# Example usage:
grouped_passages = {
    "Islam": [
        ("Quran 41:43", "Nothing is said to thee that was not said to the messengers before thee: that thy lord has at his Command (all) forgiveness as well as a most Grievous Penalty."),
        ("Quran 71:10", "Saying, 'Ask forgiveness from your Lord; for He is Oft-Forgiving;"),
        ("Quran 7:153", "But those who do wrong but repent thereafter and (truly) believe,- verily thy Lord is thereafter Oft-Forgiving, Most Merciful.")
    ],
    "Christianity": [
        ("Matthew 6:14", "For if ye forgive men their trespasses, your heavenly Father will also forgive you:"),
        ("Matthew 9:5", "For whether is easier, to say, Thy sins be forgiven thee; or to say, Arise, and walk?"),
        ("Matthew 18:35", "So likewise shall my heavenly Father do also unto you, if ye from your hearts forgive not every one his brother their trespasses.")
    ],
    "Judaism": [
        ("Exodus 32:32", "Now, if You will forgive their sin [well and good]; but if not, erase me from the record which You have written!”"),
        ("Exodus 32:30", "The next day Moses said to the people, “You have been guilty of a great sin. Yet I will now go up to יהוה; perhaps I may win forgiveness for your sin.”")
    ]
}

user_question = "What do these scriptures say about forgiveness?"
final_prompt, trimmed_passages, token_count = trim_verses_for_context(grouped_passages, user_question)

print("=== Final Prompt ===")
print(final_prompt)
print(f"\nToken count: {token_count}")

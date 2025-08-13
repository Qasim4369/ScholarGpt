from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def generate_answer(prompt):
    model_name = "google/flan-t5-base"

    print("Loading model... (this may take ~30 seconds on CPU)")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    generator = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=1500
    )

    print("Generating response...")
    response = generator(prompt)[0]['generated_text']

    return response

# Optional: keep old main test block if you want
if __name__ == "__main__":
    with open("augmented_prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    ans = generate_answer(prompt)
    print("\n=== Final Comparison ===\n")
    print(ans)

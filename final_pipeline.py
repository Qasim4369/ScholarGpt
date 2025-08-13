from Augmentation import make_augmented_prompt
from generation import generate_answer

user_query = input("Ask your question: ")

prompt, grouped, plen = make_augmented_prompt(user_query)

if prompt is None:
    print("❌ Couldn't build prompt within size limit.")
else:
    print("=== Prompt length:", plen)
    print("=== Grouped passages:", {r: len(ps) for r, ps in grouped.items()})

    response = generate_answer(prompt)
    print("\n=== Generated answer ===\n")
    print(response)

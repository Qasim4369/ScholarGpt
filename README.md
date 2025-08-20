ScholarGPT – Religious Text Comparison using RAG

ScholarGPT is a Retrieval-Augmented Generation (RAG) pipeline built in Python that compares religious texts (Islam, Christianity, Judaism) on specific topics. It retrieves relevant verses, augments them into a prompt, and uses a generative model to create a comparative answer.

🚀 Features

📂 Data Collection → Stores religious texts in JSON format.

🧠 Embeddings & Indexing → Uses FAISS for semantic search.

🔍 Similarity Search → Finds relevant verses for a given query.

📝 Prompt Augmentation → Builds a structured prompt with retrieved passages.

🤖 Text Generation → Uses FLAN-T5 / Open Source Models for comparative answers.

💻 Interactive Mode → Ask a question directly in the terminal.

⚙️ Project Structure
ScholarGPT/
│── collect_online.py      # Collects and stores texts in JSON
│── embedding.py           # Generates embeddings & builds FAISS index
│── query.py               # Tests similarity search
│── augmentation.py        # Builds augmented prompt
│── generation.py          # Generates final comparative answer
│── final_pipeline.py      # Orchestrates augmentation + generation
│── data.json              # Religious texts dataset
│── augmented_prompt.txt   # Generated prompt for LLM
│── final_comparison.txt   # Final generated answer
│── README.md              # Project documentation

🛠️ Installation

Clone the repository:

git clone https://github.com/yourusername/ScholarGPT.git
cd ScholarGPT


Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt

▶️ Usage
Run the pipeline (without recollecting/embedding again):
python final_pipeline.py


You’ll be prompted to enter a query, e.g.:

Enter your query: What do Islam, Christianity, and Judaism say about wine?


✅ ScholarGPT will:

Retrieve relevant verses

Build an augmented prompt

Generate a comparative answer

Output will be saved in:

augmented_prompt.txt

final_comparison.txt

🤖 Models

Currently uses:

FLAN-T5
 (base, free, ~512 tokens)

Easily swappable with larger models (e.g. flan-t5-large, mistral-7b-instruct, etc.)

📌 Example Output

Query: What do Islam, Christianity, and Judaism say about wine?

--- Islam ---
Quran 83:25 — "Their thirst will be slaked with Pure Wine sealed:"
Quran 76:17 — "And they will be given to drink there of a Cup (of Wine) mixed with Zanjabil,-"

--- Christianity ---
John 2:10 — "Every man at the beginning doth set forth good wine..."

--- Judaism ---
Genesis 19:32 — "Come, let us make our father drink wine..."

🛤️ Roadmap

 Add UI with Streamlit/Gradio for web interaction

 Improve dataset coverage (more scriptures, translations)

 Switch to long-context models (Mistral, Llama-3, etc.)

 Deploy as an API or Web App

🤝 Contributing

Pull requests are welcome! If you’d like to add new features or improve datasets, open an issue first to discuss what you’d like to change.

📜 License

MIT License – feel free to use, modify, and share.

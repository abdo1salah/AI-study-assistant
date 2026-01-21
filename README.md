Here is a professional **README.md** tailored to your specific project stack and features. You can copy-paste this directly into your GitHub repository.

---

# 📚 Local Study Assistant

A fully local **RAG (Retrieval-Augmented Generation)** application that allows you to chat with your textbooks and PDF course materials. Built with Python, Streamlit, LangChain, and Ollama to ensure **100% data privacy** and **zero API costs**.

*(Replace this link with an actual screenshot or GIF of your app in action)*

## 🚀 Features

* **📂 Dynamic Subject Management:** Create separate knowledge bases for different subjects (e.g., "Operating Systems", "Neural Networks").
* **📄 PDF Ingestion:** Upload multiple PDF files per subject. The app automatically chunks and embeds the text.
* **🧠 Local Vector Database:** Uses **ChromaDB** to store and retrieve relevant context efficiently.
* **💬 Interactive Chat:** Chat with your documents using a clean Streamlit interface.
* **⚡ Streaming Responses:** Real-time typewriter-style responses powered by local LLMs.
* **🔒 Privacy First:** All processing happens on your machine using **Ollama**. No data is sent to the cloud.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **LLM Orchestration:** [LangChain](https://www.langchain.com/) & Native Ollama
* **Vector Store:** [ChromaDB](https://www.trychroma.com/)
* **Local LLM Runner:** [Ollama](https://ollama.com/)
* **PDF Processing:** `pypdf`
* **Models Used:**
* **Embedding:** `mxbai-embed-large`
* **Chat:** `qwen2.5:3b` (or `llama3`)



## ⚙️ Installation

### Prerequisites

1. **Python 3.10+** installed.
2. **Ollama** installed and running. [Download here](https://ollama.com/download).

### 1. Clone the Repository

```bash
git clone https://github.com/abdo1salah/AI study assistant.git
cd study-assistant

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Pull Required Models

Open your terminal and pull the models used in the code:

```bash
ollama pull mxbai-embed-large
ollama pull qwen2.5:3b

```

## 🏃‍♂️ Usage

1. **Start the App:**
```bash
streamlit run app.py

```


2. **Upload Materials:**
* Go to the **Upload** tab in the sidebar.
* Enter a **Subject Name** (e.g., "Biology").
* Upload your PDF files and click **Process**.


3. **Chat:**
* Go to the **Home** tab.
* Select your subject from the sidebar.
* Ask a question! (e.g., *"Summarize chapter 3"*).



## 📂 Project Structure

```bash
study-assistant/
├── app.py                 # Main Streamlit application
├── embedding.py           # Logic for PDF parsing, splitting, and embedding
├── generate_response.py   # RAG pipeline and Ollama generation logic
├── requirements.txt       # Project dependencies
└── subjects/              # (Auto-generated) Stores vector DBs for each subject

```

## 🐛 Troubleshooting

* **App crashes when submitting a question:**
* Ensure Ollama is running (`ollama serve`).
* If your RAM is low, switch to a smaller model like `tinyllama` or `qwen:0.5b` in `generate_response.py`.


* **"Trio" or "Connection Lost" errors:**
* This usually happens on Windows when using LangChain's async features. Ensure you are using the `ollama.chat` (native) method in `generate_response.py` as configured in this repo.



## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have ideas for improvements.

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

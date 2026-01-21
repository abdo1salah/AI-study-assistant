from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from embedding import get_retriever 

model = ChatOllama(model="qwen2.5:3b", temperature=0)

template = """
you are a study assistant. made to help answer questions based on provided study materials.
and make summaries of the provided materials.
here are some relevant study materials {docs}:
here is what the user wants: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model 

def generate_response(subject_name, user_input):
    retriever = get_retriever(subject_name)
    retrieved_docs = retriever.invoke(user_input)
    result = chain.stream({"docs": retrieved_docs, "question": user_input})
    return result


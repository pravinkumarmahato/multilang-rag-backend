from app.core.config import GEMINI_API_KEY
from langchain import PromptTemplate, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash",google_api_key=GEMINI_API_KEY,
                             temperature=0.2,convert_system_message_to_human=True)

def call_gemini(question: str, context: str):
    template = f"""You are a helpful assistant. Answer the following question in the user's language. 
If you don't know the answer, just reply "Sorry, I don't have enough information.", don't try to make up an answer.
Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.

Context:
{context}

Question: {question}

Answer:"""

    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)
    chain = LLMChain(llm=model, prompt=QA_CHAIN_PROMPT)
    res = chain.run(context=context, question=question)

    try:
        return res
    except:
        return "Error generating response."

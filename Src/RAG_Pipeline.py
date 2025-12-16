from Src.retriever import retrieve
from Src.Reranker import rerank
from Src.llm_client import call_llm



def build_prompt(context, query):
    return f"Context:\n{context}\n\nQuestion:\n{query}"


"""
def answer_query(client, query):

    retrieved = retrieve(client, query, top_k=10)
    reranked = rerank(query, retrieved)
    context = "\n".join(reranked)

    prompt = build_prompt(context, query)
    print(prompt)
    answer = call_llm(prompt)

    return answer, reranked
"""

def answer_query(client, query, chat_history=None):

    # Build a short conversation context
    history_text = ""
    if chat_history:
        # keep last few turns to avoid huge prompts
        recent = chat_history[-4:]  # 4 turns (user+assistant) approx
        lines = []
        for m in recent:
            role = "User" if m["role"] == "user" else "Assistant"
            lines.append(f"{role}: {m['content']}")
        history_text = "\n".join(lines)


    # Retrieve/rerank using rewritten query
    retrieved = retrieve(client, query, top_k=10)
    reranked = rerank(query, retrieved)
    context = "\n".join(reranked)

    # Answer the user using context + conversation + current question
    if history_text:
        final_query_block = f"""
                            Conversation:
                            {history_text}
                                                        
                            User question:
                            {query}
                            """.strip()
    else:
        final_query_block = query

    prompt = build_prompt(context, final_query_block)
    # check prompt Length
    print("PROMPT CHARS:", len(prompt))
    print(prompt)
    answer = call_llm(prompt)

    print("answer is : "+answer)

    return answer, reranked

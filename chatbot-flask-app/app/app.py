from flask import Flask, request, jsonify
from retriever import retrieve_similar_chunks
from langchain_community.llms import OpenAI
import os
import re, json
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=openai_api_key, model="gpt-4o-mini")
def strip_outer_quotes(s):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s
from flask import session

# Add this to your Flask app config
app.secret_key = "testing" # Needed for Flask sessions
print(app.secret_key)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_query = data.get("query", "")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Get or initialize conversation history
    history = session.get("history", [])
    history.append({"role": "user", "content": user_query})

    # Build conversation context for the LLM
    conversation = ""
    for turn in history[-1:]:  # Only last 1 turns for brevity
        conversation += f"{turn['role'].capitalize()}: {turn['content']}\n"

    # Get context from retriever as before
    context_chunks = retrieve_similar_chunks(user_query, k=3)
    context = "\n\n".join([
        chunk[0].page_content + f"\n(Page: {chunk[0].metadata.get('page_number', 'N/A')})"
        for chunk in context_chunks
    ])

    # Use the detailed, page-aware prompt
    prompt = f"""
You are a helpful surgery tutor. Use ONLY the following context from a surgery manual to answer the user's question.

Instructions:
- Must reply to greetings like "hi","hello", provide your one liner intro and do greetings.
- Each context chunk ends with its page number in the format (Page: <number>).
- If the answer is not in the context, reply: "I don't know based on the provided material."
- If your answer contains terms that may not be understandable to students, provide an explanation for those terms ONLY.
- The explanation must be in bullet points, well-structured, and MUST NOT use line breaks ("\\n") within each point.
- Do NOT explain the entire answer, only the specific terms that may be unclear.
- At the end of your answer, provide a JSON object with a "pages" field listing the page number(s) from the metadata of the context chunk(s) you used to answer, e.g. {{"pages": [13, 14]}}.
- Only use page numbers from the (Page: <number>) metadata in the provided context.
- Try to provide answer in the structured way. After every fullstop add a <br>.
- Follow this response structure exactly:

"<your answer here>
- Explanation:
- <term 1>: <simple explanation>
- <term 2>: <simple explanation>
...
{{"pages": [list of page numbers]}}

Example:
Suppose the context contains:
...some text... (Page: 13)
...some more text... (Page: 14)

If you answer using information from both, your response should be:
An ulcer is a break in the continuity of the covering epithelium, either skin or mucous membrane due to molecular death.
- Explanation:
- Ulcer: a sore on the skin or mucous membrane where the surface is broken.
- Epithelium: tissue that forms the outer layer of skin and lines organs, cavities, and surfaces.
- Molecular death: cells in that area have died, leading to the formation of the ulcer.
{{"pages": [13, 14]}}

Conversation so far:
{conversation}

Context:
{context}

User question: {user_query}
Answer:
"""
    answer = llm(prompt)
    history.append({"role": "assistant", "content": answer})
    session["history"] = history  # Save updated history

    # Extract page numbers from the answer using regex
    
    match = re.search(r'(\{.*"pages".*\})', answer)
    pages = []
    if match:
        try:
            pages = json.loads(match.group(1).replace("'", '"')).get("pages", [])
            # Remove the JSON part from the answer for display
            answer = answer.replace(match.group(1), "").strip()
        except Exception:
            pass

    answer = strip_outer_quotes(answer)
    cleaned_answer = re.sub(r'\n(?=- )', '<br>', answer).replace('\n', ' ')
    return jsonify({"answer": cleaned_answer, "pages": pages})

if __name__ == "__main__":
    app.run(debug=True)
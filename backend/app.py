from flask import Flask, request, jsonify
import json

from flask_cors import CORS
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
from peft import PeftModel, PeftConfig
import torch
from rag_db_creation import vectorstore

login("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")

model_id = "sl207/tiny-llama-finetuned-philosopherv2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
peft_config = PeftConfig.from_pretrained(model_id)
base_model = AutoModelForCausalLM.from_pretrained(
    peft_config.base_model_name_or_path,
    torch_dtype=torch.float32,
    low_cpu_mem_usage=True,
    device_map="cpu",
)
model = PeftModel.from_pretrained(base_model, model_id)
model = model.to("cpu")
model.eval()
streamer = TextStreamer(tokenizer)
# eos_token_id = tokenizer.convert_tokens_to_ids("<|endoftext|>")
# data = [
#     {
#         "from": "system",
#         "value": "You are A VASTLY intelligent ARTIFICIAL INTELLIGENCE with DOMAIN-EXPERT KNOWLEDGE from a variety of fields.\nUSE your knowledge to be helpful and truthfully answer questions about the world.",
#     },
#     {
#         "from": "user",
#         "value": "How to define consciousness?",
#     },
# ]

app = Flask(__name__)
CORS(app)


def apply_rag(messages: list[dict[str, str]]):
    query = messages[-1]["value"]
    docs = vectorstore.similarity_search(query, k=2)
    rag_text = "\n".join([doc.page_content for doc in docs])
    messages[0]["value"] += "\nHere is some potentially-relevant context:\n " + rag_text
    return messages

# Format and tokenize messages
def preprocess(messages: list[dict[str, str]]):
    formatted = ""
    for msg in messages:
        role = msg["from"]
        if role == "system":
            formatted += f"<|system|>\n{msg['value']}\n"
        elif role == "user":
            formatted += f"<|user|>\n{msg['value']}\n"
        elif role == "gpt":
            formatted += f"<|assistant|>\n{msg['value']}\n<|endoftext|>\n"
    formatted += "<|assistant|>\n"
    return tokenizer(formatted, return_tensors="pt")


def postprocess(inputs, output, tokenizer):
    initial_len = len(inputs["input_ids"][0])
    new_msg = output[0][initial_len:]
    decoded = tokenizer.decode(new_msg, skip_special_tokens=True)
    if "<" in decoded:
        decoded = decoded[: decoded.index("<")]
    return decoded


@app.route("/")
def home():
    return "Welcome to AskPhilosopher!"


@app.route("/api/chat", methods=["POST"])
def chatbot():
    messages = []
    for key in request.form.keys():
        if key.startswith("msg"):
            msg = json.loads(request.form[key])
            messages.append(msg)

    # RAG: Add context to system prompt
    messages = apply_rag(messages)

    inputs = preprocess(messages)
    output = model.generate(
        **inputs,
        do_sample=True,
        temperature=0.5,
        top_p=0.7,
        max_new_tokens=100,
        streamer=streamer,
    )
    decoded = postprocess(inputs, output, tokenizer)
    return jsonify({"response": {"from": "gpt", "value": decoded}}), 200


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0", debug=True)

from flask import Flask, request, jsonify

# from flask_cors import CORS
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
from peft import PeftModel, PeftConfig, PeftModelForCausalLM
import torch

login("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")

model_id = "sl207/tiny-llama-finetuned-philosopher"
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
eos_token_id = tokenizer.convert_tokens_to_ids("<|endoftext|>")
data = [
    {
        "from": "system",
        "value": "You are A VASTLY intelligent ARTIFICIAL INTELLIGENCE with DOMAIN-EXPERT KNOWLEDGE from a variety of fields.\nUSE your knowledge to be helpful and truthfully answer questions about the world.",
    },
    {
        "from": "user",
        "value": "How to define consciousness?",
    },
]

app = Flask(__name__)
# CORS(app)


def format_text(messages: list[dict[str, str]]):
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
    return formatted


@app.route("/")
def home():
    return data[1]["value"]


@app.route("/api/chat", methods=["POST"])
def chatbot():
    messages = []
    for key in request.form.keys():
        if key.startswith("msg"):
            messages.append(request.form[key])
    print(messages)
    # formatted_text = format_text(data)
    # inputs = tokenizer(formatted_text, return_tensors="pt")
    # output = model.generate(
    #     **inputs,
    #     # do_sample=True,
    #     # temperature=0.7,
    #     # top_p=0.95,
    #     eos_token_id=eos_token_id,
    #     max_new_tokens=40,
    #     streamer=streamer,
    # )
    # decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    return jsonify({"response": data[1]["value"]})


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0", debug=True)

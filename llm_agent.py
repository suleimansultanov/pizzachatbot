from menu import menu
from llama_cpp import Llama

# Initialize llama.cpp model
llm = Llama(
    model_path="./Mistral-Nemo-Instruct-2407-Q5_K_M.gguf",
    n_ctx=2048,
    n_gpu_layers=-1,
    n_threads=8,
    n_batch=512,
    use_mmap=True,
    use_mlock=False,
    verbose=False,
    seed=1234
)

def generate_prompt(order, user_input):
    return f"""
You are an AI assistant for a pizza delivery service.
Here is the menu:
Pizzas: {', '.join(menu['pizzas'])}
Toppings: {', '.join(menu['toppings'])}
Extras: {', '.join(menu['extras'])}

Current Order: {order}
Customer said: "{user_input}"

Based on this, either extract pizza order details, delivery address, allergies, or ask follow-up questions to complete the order.
Always respond concisely and helpfully.
"""

def classify_intent_with_llm(user_input: str) -> str:
        prompt = f"""
You are a helpful assistant for a pizza ordering service. Classify the user's message into one of the following categories:
- "pizza": if they are selecting pizza types and quantities.
- "topping": if they are specifying toppings or modifiers for pizzas.
- "extra": if they are ordering extras like drinks, sauces, or sides.
- "address": if they are giving a delivery address.
- "note": if they are adding delivery notes or allergy information.
- "unknown": if it's unclear.

User input: "{user_input}"

Respond with only the intent label.
"""
        intent = llm(prompt, max_tokens=256, stop=["User:", "AI:"])
        return intent["choices"][0]["text"].strip()



def get_response(prompt):
    output = llm(prompt, max_tokens=256, stop=["User:", "AI:"])
    return output["choices"][0]["text"].strip()

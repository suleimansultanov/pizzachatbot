import re
from menu import menu

class DialogManager:
    def __init__(self):

        self.state = "start"
        self.order = {
            "pizzas": [],
            "toppings": [],
            "extras": [],
            "notes": "",
            "address": ""
        }


    def extract_quantity(self, text: str) -> int:
        import re
        match = re.search(r'\b(\d+)\b', text)
        return int(match.group(1)) if match else 1

    def update(self, user_input: str, llm_reply: str, intent:str) -> str:


        if intent == "pizza":
            for item in re.findall(r'(\d+)?\s*([A-Za-z ]+?)(?=,|and|$)', user_input, re.IGNORECASE):
                # quantity = int(item[0]) if item[0].isdigit() else 1
                name = extract_order_details(user_input, "pizzas")
                if(len(name) > 0):
                    self.order["pizzas"].append(name)

        elif intent == "toppings":
            toppings = [t.strip().lower() for t in user_input.split(",") if t.strip()]
            for topping in toppings:
                tpng = extract_order_details(topping, "toppings")
                self.order["toppings"].append(tpng)

        elif intent == "extra":
            extras = [e.strip().lower() for e in user_input.split(",") if e.strip()]
            for topping in toppings:
                extras = extract_order_details(topping, "toppings")
                self.order["extras"].append(extras)

        elif intent == "note":
            self.order["notes"] += " " + user_input.strip()

        elif intent == "address":
            self.order["address"] = user_input.strip()
            self.state = "complete"

        elif intent == "unknown":
            if(len(llm_reply) <= 0):
                return "Unfortunately we can't understand your request, please specify your needs"
        # Return LLM's original reply unchanged
        return llm_reply


def extract_order_details(user_input: str, type: list) -> list:
    pizza_list = menu[type]
    extracted_pizzas = []
    user_input_lower = user_input.lower()  # Convert input once to lowercase

    # Sort pizza list by length descending to match longer names first
    # (e.g., "bbq chicken" before "chicken")
    sorted_pizza_list = sorted(pizza_list, key=len, reverse=True)

    for pizza_name_from_list in sorted_pizza_list:
        # We need to find the pizza name as a whole word to avoid partial matches
        # Use re.escape to handle special characters in pizza names
        # Use \b for word boundaries
        pattern = re.compile(rf'(\d+)?\s*\b{re.escape(pizza_name_from_list)}\b', re.IGNORECASE)

        # Iterate through all occurrences of this pizza name in the input
        for match in pattern.finditer(user_input):
            quantity_str = match.group(1)
            quantity = int(quantity_str) if quantity_str else 1

            extracted_pizzas.append({
                "name": pizza_name_from_list, # Use the name from the list as it's the valid one
                "quantity": quantity
            })
            # Optional: Remove the matched part from user_input_lower
            # if you want to avoid counting the same pizza multiple times
            # in very complex sentences, but for typical orders, it's fine.
            # This would make the logic more complex to re-match.

    # If you want to handle cases where a pizza might be mentioned multiple times without quantity
    # (e.g., "I want a pepperoni and a pepperoni"), this simple approach will count them
    # separately. If you need to consolidate, you'd add another loop to sum quantities.

    return extracted_pizzas
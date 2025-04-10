import streamlit as st
import re

# -------------------------------
# Menu and Special Items
# -------------------------------
menu = {
    "pizza": 250,
    "burger": 150,
    "pasta": 200,
    "fries": 100,
    "salad": 120,
    "coke": 50,
    "brownie": 80
}

specials = ["Truffle Pasta", "BBQ Chicken Pizza", "Chef's Special Brownie Sundae"]

# -------------------------------
# Helper Functions
# -------------------------------
def show_menu():
    return "\n📜 Here's our menu:\n" + "\n".join([f" - {item.title()}: ₹{price}" for item, price in menu.items()]) + "\n"

def show_specials():
    return "\n🌟 Today's Specials:\n" + "\n".join([f" - {item}" for item in specials]) + "\n"

def process_user_input(user_input):
    user_input = user_input.lower()

    if user_input in ["hi", "hello", "hey"]:
        return "👋 Hi there! How can I assist you today?"

    elif "menu" in user_input:
        return show_menu()

    elif "special" in user_input:
        return show_specials()

    elif "order" in user_input:
        return "🍽️ What would you like to order? (e.g., 'I want 2 burgers')"

    elif any(food in user_input for food in menu.keys()):
        # Parse order like "I want 2 burgers"
        pattern = r'(\d+)\s*([a-zA-Z\s]+)'
        matches = re.findall(pattern, user_input)
        if matches:
            reply = "✅ Order added:\n"
            for qty, item in matches:
                item = item.strip().lower()
                if item in menu:
                    qty = int(qty)
                    st.session_state.order[item] = st.session_state.order.get(item, 0) + qty
                    reply += f" - {item.title()} x {qty}\n"
                else:
                    reply += f" - {item.title()} is not on the menu.\n"
            reply += "\nYou can type 'bill' to see your current bill."
            return reply
        else:
            return "🍽️ Please specify the quantity and item, like '2 burgers' or '1 pasta'."

    elif "bill" in user_input:
        if st.session_state.order:
            bill = "\n🧾 Your Current Bill:\n"
            total = 0
            for item, qty in st.session_state.order.items():
                price = menu[item] * qty
                bill += f" - {item.title()} x {qty} = ₹{price}\n"
                total += price
            bill += f"\n💰 Total Amount: ₹{total}\n"
            return bill
        else:
            return "🧐 You haven't ordered anything yet."

    elif user_input in ["bye", "exit", "quit"]:
        return "👋 Thanks for visiting! Have a delicious day!"

    else:
        return "🤷‍♂️ I didn't catch that. Try something like 'show menu', 'order 2 pizzas', or 'specials'."

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="FoodieBot 🍽️", page_icon="🤖")
st.title("🍽️ FoodieBot - Your Restaurant Assistant")

# Initialize chat history and order in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "order" not in st.session_state:
    st.session_state.order = {}

# Display all previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("What would you like to ask?"):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Process and show bot response
    response = process_user_input(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st
import json
import random
import string
from pathlib import Path

DATABASE = "data.json"

# Load data
def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE) as f:
            return json.load(f)
    return []

# Save data
def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f)

data = load_data()

# Generate account number
def generate_acc():
    alpha = random.choices(string.ascii_letters, k=3)
    num = random.choices(string.digits, k=3)
    sp = random.choice("!@#$%^&*")
    acc = alpha + num + [sp]
    random.shuffle(acc)
    return "".join(acc)

st.title("🏦 Simple Bank System")

menu = st.sidebar.selectbox(
    "Choose Option",
    ["Create Account", "Deposit", "Withdraw", "Show Details", "Update Details", "Delete Account"]
)

# Create Account
if menu == "Create Account":
    st.header("Create Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    email = st.text_input("Email")
    pin = st.text_input("4 Digit PIN")

    if st.button("Create"):
        if age < 18 or len(pin) != 4:
            st.error("Age must be 18+ and PIN must be 4 digits")
        else:
            accno = generate_acc()
            user = {
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "accno": accno,
                "balance": 0
            }

            data.append(user)
            save_data(data)

            st.success("Account Created!")
            st.write("Your Account Number:", accno)

# Deposit
elif menu == "Deposit":
    st.header("Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")
    amount = st.number_input("Amount", min_value=0)

    if st.button("Deposit"):
        user = [i for i in data if i["accno"] == acc and i["pin"] == int(pin)]

        if not user:
            st.error("Account not found")
        else:
            user[0]["balance"] += amount
            save_data(data)
            st.success("Deposit Successful")

# Withdraw
elif menu == "Withdraw":
    st.header("Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")
    amount = st.number_input("Amount", min_value=0)

    if st.button("Withdraw"):
        user = [i for i in data if i["accno"] == acc and i["pin"] == int(pin)]

        if not user:
            st.error("Account not found")
        elif user[0]["balance"] < amount:
            st.error("Insufficient Balance")
        else:
            user[0]["balance"] -= amount
            save_data(data)
            st.success("Withdrawal Successful")

# Show Details
elif menu == "Show Details":
    st.header("Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")

    if st.button("Show"):
        user = [i for i in data if i["accno"] == acc and i["pin"] == int(pin)]

        if not user:
            st.error("Account not found")
        else:
            st.json(user[0])

# Update Details
elif menu == "Update Details":
    st.header("Update Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")

    new_name = st.text_input("New Name")
    new_email = st.text_input("New Email")
    new_pin = st.text_input("New PIN")

    if st.button("Update"):
        user = [i for i in data if i["accno"] == acc and i["pin"] == int(pin)]

        if not user:
            st.error("Account not found")
        else:
            if new_name:
                user[0]["name"] = new_name
            if new_email:
                user[0]["email"] = new_email
            if new_pin:
                user[0]["pin"] = int(new_pin)

            save_data(data)
            st.success("Details Updated")

# Delete Account
elif menu == "Delete Account":
    st.header("Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")

    if st.button("Delete"):
        user = [i for i in data if i["accno"] == acc and i["pin"] == int(pin)]

        if not user:
            st.error("Account not found")
        else:
            data.remove(user[0])
            save_data(data)
            st.success("Account Deleted")
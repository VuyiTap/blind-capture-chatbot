# blind_capture_chatbot.py
# Streamlit-powered mini-bot for Payment Manager – Blind Capture

import streamlit as st

st.set_page_config(page_title="Blind Capture Chatbot", page_icon="💬")
st.title("💬 Blind Capture Chatbot")

# ---------- knowledge base ----------
FAQ = {
    "assign ssi": '''
**Steps to assign an SSI**

1. Open *Payment Manager*  
2. Select the date range ➜ **Load**  
3. Pick a payment with **Gross** or **Invalid** status  
4. Right-click ➜ **Assign SSI**  
5. Enter SSI details ➜ **Save**

If details aren’t saved, verify you have the correct rights and mandatory fields are filled.
''',
    "open blind capture": '''
**When does the Blind Capture window appear?**

- *Verify* on a payment in **Gross** status  
- *Send* on a payment in **Verified** status (Settlement queue)  
- *Verify/Send* after a **Send Back** (status returns to Gross/Verified)  

Portfolios **not enabled** for Blind Capture will *not* trigger the window.
''',
    "enter amount": '''
**Entering the amount**

- The **Amount** field is mandatory.  
- If the value differs from the system’s expected amount, an error message appears and the payment stays unverified.

*Tip*: Copy the amount from the payment summary to avoid typos.
''',
    "enter account": '''
**Entering the account number**

- The **Account Number** field appears after you enter the amount.  
- An incorrect account number triggers an error and blocks the send/verify action.  
- Use the beneficiary’s official bank details only.
''',
    "error wrong amount": "You’ll see *“Amount Mismatch – please re-enter.”* Re-open Blind Capture and supply the correct amount.",
    "error wrong account": "You’ll see *“Account Number Invalid.”* Confirm the beneficiary details, reopen Blind Capture, and re-enter the account number."
}

def reply(user_text: str) -> str:
    txt = user_text.lower()

    if any(kw in txt for kw in ["assign ssi", "how do i assign", "steps for assigning", "ssi assignment"]):
        return FAQ["assign ssi"]
    elif any(kw in txt for kw in ["trigger", "when", "open", "show", "blind capture"]):
        return FAQ["open blind capture"]
    elif "amount" in txt:
        if "wrong" in txt or "error" in txt or "incorrect" in txt:
            return FAQ["error wrong amount"]
        return FAQ["enter amount"]
    elif "account" in txt or "iban" in txt:
        if "wrong" in txt or "error" in txt or "incorrect" in txt:
            return FAQ["error wrong account"]
        return FAQ["enter account"]
    else:
        return (
            "I’m trained only on Blind Capture basics for now. "
            "Ask me about assigning SSI, opening Blind Capture, entering amounts or account numbers, "
            "or the errors you might see."
        )

# ---------- Streamlit chat UI ----------
if "history" not in st.session_state:
    st.session_state.history = []

for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

if prompt := st.chat_input("Ask me anything about Blind Capture…"):
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    answer = reply(prompt)
    st.session_state.history.append(("assistant", answer))
    with st.chat_message("assistant"):
        st.markdown(answer)


    answer = reply(prompt)
    st.session_state.history.append(("assistant", answer))
    with st.chat_message("assistant"):
        st.markdown(answer)

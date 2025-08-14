import random
import re
import streamlit as st

# --- Chatbot class ---
class RuleBot:
    negative_res = ("no", "nope", "nah", "naw", "not a chance", "sorry")
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")

    random_question = (
        "Why are you here?",
        "Are there many humans like you?",
        "What do you consume for sustenance?",
        "Is there Intelligent life on this planet?",
        "Does Earth have a leader?"
    )

    def __init__(self):
        self.alienbabble = {
            'describe_planet_intent': r'.*\s*your planet.*',
            'answer_why_intent': r'why\sare.*',
            'about_intellipaat': r'.*\s*intellipaat.*'
        }

    def make_exit(self, reply):
        return reply in self.exit_commands

    def match_reply(self, reply):
        for intent, regex_pattern in self.alienbabble.items():
            if re.match(regex_pattern, reply):
                if intent == 'describe_planet_intent':
                    return self.describe_planet_intent()
                elif intent == 'answer_why_intent':
                    return self.answer_why_intent()
                elif intent == 'about_intellipaat':
                    return self.about_intellipaat()
        return self.no_match_intent()

    def describe_planet_intent(self):
        return random.choice(("My planet is a utopia of diverse organism",
                              "I heard the coffee is good"))

    def answer_why_intent(self):
        return random.choice(("I come in peace",
                              "I am here to collect data on your planet and its inhabitants",
                              "I heard the coffee is good"))

    def about_intellipaat(self):
        return random.choice(("Intellipaat is world's largest professional educational company",
                              "Intellipaat will make you learn concepts in the best way",
                              "Intellipaat is where your career and skill grows"))

    def no_match_intent(self):
        return random.choice(("Please tell me more.",
                              "Tell me more!",
                              "Interesting. Can you tell me more?",
                              "I see. How do you think?",
                              "Why?"))


# --- Streamlit UI ---
st.title("🌎 Alien ChatBot")

if 'bot' not in st.session_state:
    st.session_state.bot = RuleBot()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# Step 1: Ask name first
if not st.session_state.user_name:
    name_input = st.text_input("What is your name?")
    if name_input:
        st.session_state.user_name = name_input.strip()
        st.session_state.chat_history.append(("Bot", f"Hi {st.session_state.user_name}, I am bot. Will you help me learn about your planet?"))
        st.session_state.chat_history.append(("Bot", random.choice(st.session_state.bot.random_question)))

# Step 2: Main chat interface
if st.session_state.user_name:
    user_input = st.text_input("You:")
    if st.button("Send"):
        if user_input:
            lower_input = user_input.lower()

            if st.session_state.bot.make_exit(lower_input):
                st.session_state.chat_history.append(("Bot", "Have a nice day! 👋"))
            elif lower_input in st.session_state.bot.negative_res:
                st.session_state.chat_history.append(("Bot", "Have a nice Earth day! 🌍"))
            else:
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Bot", st.session_state.bot.match_reply(lower_input)))
            st.experimental_rerun()  # page reload after adding chat

# Step 3: Display chat history
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")

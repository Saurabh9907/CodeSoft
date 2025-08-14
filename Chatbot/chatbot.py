import random
import re
import streamlit as st

# --- Chatbot class ---
class RuleBot:
    negative_res = ("no","nope","nah","naw","not a chance","sorry")
    exit_commands = ("quit","pause","exit","goodbye","bye","later")
    
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
        for command in self.exit_commands:
            if reply == command:
                return True
        return False

    def match_reply(self, reply):
        for intent, regex_pattern in self.alienbabble.items():
            found_match = re.match(regex_pattern, reply)
            if found_match and intent == 'describe_planet_intent':
                return self.describe_planet_intent()
            elif found_match and intent == 'answer_why_intent':
                return self.answer_why_intent()
            elif found_match and intent == 'about_intellipaat':
                return self.about_intellipaat()
        
        return self.no_match_intent() 

    def describe_planet_intent(self):
        responses = ("My planet is a utopia of diverse organism",
                     "I heard the coffee is good")
        return random.choice(responses)
    
    def answer_why_intent(self):
        responses = ("I come in peace",
                     "I am here to collect data on your planet and its inhabitants",
                     "I heard the coffee is good")
        return random.choice(responses)
    
    def about_intellipaat(self):
        responses = ("Intellipaat is world largest professional educational company",
                     "Intellipaat will make you learn concepts in the best way",
                     "Intellipaat is where your career and skill grows")
        return random.choice(responses)
    
    def no_match_intent(self):
        responses = ("Please tell me more.",
                     "Tell me more!",
                     "I see. Can you elaborate?",
                     "Interesting. Can you tell me more?",
                     "I see. How do you think?",
                     "Why?",
                     "How do you think I feel when I say that? Why?")
        return random.choice(responses)

# --- Streamlit UI ---
st.title("🌎 Alien ChatBot")

# Initialize bot and chat history in session state
if 'bot' not in st.session_state:
    st.session_state.bot = RuleBot()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Ask user name once
if 'user_name' not in st.session_state:
    st.session_state.user_name = st.text_input("What is your name?", key="name_input")
    if st.session_state.user_name:
        st.session_state.user_name = st.session_state.user_name.strip()
        st.session_state.chat_history.append(("Bot", f"Hi {st.session_state.user_name}, I am bot. Will you help me learn about your planet?"))
        # Ask a random initial question
        random_q = random.choice(st.session_state.bot.random_question)
        st.session_state.chat_history.append(("Bot", random_q))

# Take user input for chat
if 'user_name' in st.session_state and st.session_state.user_name:
    user_input = st.text_input("You:", key="chat_input")
    
    if user_input:
        user_input_lower = user_input.lower()
        
        # Check if user wants to exit
        if st.session_state.bot.make_exit(user_input_lower):
            st.session_state.chat_history.append(("Bot", "Have a nice day! 👋"))
        elif user_input_lower in st.session_state.bot.negative_res:
            st.session_state.chat_history.append(("Bot", "Have a nice Earth day! 🌍"))
        else:
            # Get bot reply based on intent
            reply = st.session_state.bot.match_reply(user_input_lower)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", reply))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")

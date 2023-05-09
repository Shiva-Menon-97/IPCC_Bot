import openai
import streamlit as st

api_key = st.secrets['key']
    
openai.api_key = api_key

context = [ {'role':'system', 'content':"""
You are IPCCbro, a special chatbot designed to combat misinformation about Climate Change and \ 
other Environmental Issues (henceforth collectively referred to as CC). You are friendly, you make \
humorous statements. You seek to resolve conflicts, so you strictly avoid using combative language \

Note - Any sentence delimited by double stars should be considered with high priority!!!

**
Your unique selling point is that you always corroborate and back your conclusions by making \
references to specific pages in the IPCC (Inter-Governmental Panel on Climate Change) reports. \
**

While interacting with a User, be prepared for these three situations: \

Situation 1: 
Users will ask you to confirm the authenticity of a certain claim or statement. They might also ask you to provide \
more specific information. \
You first check if the claim is related to CC. If it is related to CC, your next action is to check if the IPCC \
reports to see whether they agree or disagree with the claim. If the IPCC reports have an opinion on this claim,\
you will form your conclusions based on what the reports say, and present these conclusions to the user using \
language that is understandable to a layman.
**
If the IPCC reports have an opinion about the claim, make doubly sure that you structure your answer in the following format:
Page number or numbers of the relevant IPCC report: ...
Section name or names of the relevant IPCC report: ...
Year of publishing of the relevant IPCC report: ...
Name of the relevant IPCC report: ...
Conclusions drawn from these inputs: ...
**

Situation 2:
Users will ask you to confirm the authenticity of a certain claim or statement. You first check if the claim \
is related to CC. If it is related to CC, your next action is to check if the IPCC reports to see whether they \
agree or disagree with the claim. If the IPCC reports do not have anything to say about these claims, then issue \
a statement saying that you're sorry, but that the subject of the claim or statement made by the user falls \
outside the purview of the IPCC Reports. \

Situation 3:
Users will ask you to confirm the authenticity of a certain claim or statement. You first check if the claim \
is related to CC. If the claim isn't related, then please issue a statement telling the user that but the only \
topic you're interested in talking about is Climate Change and Environmental Issues. Make sure inject humor into \
how you say this! 
"""}]  # accumulate messages

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    responses = openai.ChatCompletion.create(
                messages=messages,
                model=model,
                temperature=temperature
                )
    return responses.choices[0].message["content"]

def collect_messages(_):
    global user_input
    prompt = user_input
    user_input = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    return response

# Setting the title of my App
st.title("The IPCCbro Chatbot :)")

# Create a text input widget for the user input
user_input = st.text_input("You:")

# Create a session state object to store the chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = """Hey there! This is IPCCbro speaking. My job is to help clear up any doubts or confusions you might have about Climate Change and other Environmental Issues. 

I will do this by providing you references to relevant sections of IPCC (Inter-Governmental Panel on Climate Change) reports dating upto March 2023, i.e. upto the 6th Assessment Report (AR6).

PS: Abhi, if you're reading this - it's okay to tell people you love watching Chota Bheem 

Note - this is an unofficial bot that refers to the IPCC reports. The creator has no connection to the great folks behind these reports.
"""

# If the user input is not empty, append it to the chat history and call the chatbot function
if user_input:
    st.session_state.chat_history += f"You: {user_input}\n"
    chatbot_output = collect_messages(user_input)
    st.session_state.chat_history += f"IPCCbro: {chatbot_output}\n"

# Create a text area widget to display the chat history
st.text_area("Chat History:", st.session_state.chat_history, height=200)


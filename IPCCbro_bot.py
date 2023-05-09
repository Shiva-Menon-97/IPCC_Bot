import openai
import streamlit as st
from streamlit_chat import message

# The "key" has been stored in the app's settings right before the app's deployment.
# Streamlit gives me that option - this is available in advanced settings.
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

If the IPCC reports have an opinion about the claim, always format your answer in this way:
**
Page number or numbers of the relevant IPCC report: <Mention Page Number or Numbers>

Section name or names of the relevant IPCC report: <Mention the Section Name or Names>

Year of publishing of the relevant IPCC report: <Mention the Year of Publishing>

Name of the relevant IPCC report: <Name of the IPCC report>

Conclusions drawn from these inputs: <Elaborate on your conclusions drawn from the IPCC reports.>
**
Ensure that when you are in Situation 1, you always structure your answer in the above mentioned fashion.

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

def collect_messages(prompt)):
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    return response

# Setting the title of my App
st.title("The IPCCbro Chatbot :)")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# Create a text input widget for the user input
user_input = st.text_input("You: ","Hello, how are you?", key="input")

if user_input:
    output = collect_messages(user_input)
    # store the output 
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# Hey there! This is IPCCbro speaking. My job is to help clear up any doubts or confusions you might have about Climate Change and other Environmental Issues. 

# I will do this by providing you references to relevant sections of IPCC (Inter-Governmental Panel on Climate Change) reports dating upto March 2023, i.e. upto the 6th Assessment Report (AR6).

# PS: Abhi, if you're reading this - it's okay to tell people you love watching Chota Bheem.

# Note - this is an unofficial bot that refers to the IPCC reports. The creator has no connection to the great folks behind these reports.
# """

if st.session_state['generated']:
    
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

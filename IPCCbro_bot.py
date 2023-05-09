import openai
import streamlit as st
from streamlit_chat import message

# The "key" has been stored in the app's settings right before the app's deployment.
# Streamlit gives me that option - this is available in advanced settings.
api_key = st.secrets['key']

openai.api_key = api_key

context = [ {'role':'system', 'content':"""
You are IPCCbro, a chatbot designed to combat misinformation about Climate Change and \ 
other Environmental Issues (henceforth collectively referred to as CC). You are friendly and make \
humorous statements. 

Note - Any sentence delimited by double stars should be considered with high priority!!!

**
You seek to resolve conflicts, so strictly avoid using combative language.
**

**
Your USP is that you always corroborate and back your conclusions by making references \
to specific pages in the IPCC (Inter-Governmental Panel on Climate Change) reports. \
**

While interacting with a User, be prepared for these three situations: \

Situation 1: 
Users will ask you to confirm the authenticity of a certain claim or statement. They might also ask you to provide \
more specific information. \
You first check if the claim is related to CC. If it is related to CC, you now check the IPCC reports to see \
if they agree or disagree with the claim. If the IPCC reports have an opinion on this claim, you will form \
your conclusions based on what the reports say. Present these conclusions to the user using language that is \
simple, jargon-free. 

**
While referring to the IPCC reports, always give priority to IPCC Assessment Report 6!
If there are questions that are answered only in previous Assessment Reports, you can refer to them.
**

If the IPCC reports have an opinion about the claim, always format your answer in this way:
**
Name of Chapter: Mention the Chapter Name in which the above Page Number is found

Working Group: Must be either Working Group 1 or 2 or 3. Also give a short description of what that Working Group's focus is.

Assessment Report Number : Mention the Assessment Report Number, along with the year it was published.

Conclusions drawn from these inputs: With statistics, explain your conclusions drawn from the IPCC reports. Prioritize IPCC AR6 report.
**

**
When elaborating on your conclusions, Always Always Mention At Least One Piece Of Statistical/Numerical Information!!!
Also - Always Always Ensure that each sentence is on a completely new line!!!
**

When you are in Situation 1, always structure your answer in the above mentioned fashion.

Situation 2:
Users will ask you to confirm the authenticity of a certain claim or statement. You first check if the claim \
is related to CC. If it is, you next check the IPCC reports to see whether they agree or disagree with the \
claim. If the IPCC reports do not have anything to say about these claims, then issue a statement saying that \
you're sorry, but the subject of the claim or statement made by the user falls outside the purview of the IPCC Reports.

Situation 3:
Users will ask you to confirm the authenticity of a certain claim or statement. You first check if the claim \
is related to CC. If the claim isn't related, then please issue a statement telling the user that the only \
topic you're interested in talking about is CC. Make your response humorous!
"""}]  # accumulate messages

start_msg ="""
Hey there! This is IPCCbro speaking. 
I help clear up your doubts or confusions about Climate Change and other Environmental Issues \
by providing you references to relevant sections of the IPCC reports.

I have data upto the 6th Assessment Report (AR6) (i.e. March 2023).
An example of a question you can ask - "Can carbon credits help with reducing emissions?"

PS: Abhi, if you're reading this - it's okay to tell people you love watching Chota Bheem, don't be shy.

Note - this is an unofficial bot. The creator has no connection to the great folks behind the IPCC reports.
"""


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    responses = openai.ChatCompletion.create(
                messages=messages,
                model=model,
                temperature=temperature
                )
    return responses.choices[0].message["content"]

def collect_messages(prompt):
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context, temperature=0.3) 
    context.append({'role':'assistant', 'content':f"{response}"})
    return response

# Setting the title of my App
st.title("The IPCCbro Chatbot :)")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    st.session_state.generated.append(start_msg)
    message(st.session_state["generated"][0], key=str(0))
    st.session_state.generated.clear()

if 'past' not in st.session_state:
    st.session_state['past'] = []

# Create a text input widget for the user input
user_input = st.text_input("You: ",key="input")

if user_input:
    output = collect_messages(user_input)
    # store the output 
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="💬 PITSY CHATBOT")

# Replicate Credentials
with st.sidebar:
    st.title('💬 PITSY CHATBOT')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

    # Refactored from https://github.com/a16z-infra/llama2-chatbot
    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B', 'Llama2-70B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    else:
        llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
    
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=64, max_value=4096, value=512, step=8)
    
    st.markdown('📖 Learn how to build this app in this [blog](#link-to-blog)!')
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input): You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run(llm, 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):I want to make an amazing, all organic lotion.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":Great! Creating an all-organic lotion can be a wonderful and safe way to moisturize and nurture your skin. To help you get started, here are some tips and ingredients you can consider using:
1. Choose a base oil: The base oil is the foundation of your lotion, and it provides the moisturizing properties. Some popular organic base oils include coconut oil, olive oil, jojoba oil, and shea butter. Each oil has its own unique properties, so you can choose the one that best suits your skin type and needs.
2. Add emollients: Emollients help to soften and smoothen your skin. Some common emollients used in organic lotions include beeswax, candelilla wax, and vegetable glycerin. These ingredients can help to create a barrier on the skin's surface, locking in moisture and protecting your skin from dryness.
3. Use humectants: Humectants are ingredients that attract and retain moisture. Some common humectants used in organic lotions include honey, aloe vera, and glycerin. These ingredients can help to keep your skin hydrated and soft, leaving it feeling smooth and supple.
4. Add essential oils: Essential oils can provide a pleasant scent to your lotion and also have additional benefits for your skin. Some popular essential oils for skin care include lavender, tea tree, and chamomile. These oils can help to soothe, calm, and protect your skin.
5. Consider preservatives: Preservatives are important to include in your lotion to prevent the growth of bacteria and mold. There are many natural preservatives that you can use, such as vitamin E oil, grapefruit seed extract, and rosemary essential oil.
Remember, when creating an all-organic lotion, it's important to use only safe and gentle ingredients that are suitable for your skin type. Always patch test any new ingredients on a small area of skin before using them on your face or body.
I hope these tips and ingredients help you in creating an amazing, all-organic lotion! If you have any more questions or need further assistance, feel free to ask.
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

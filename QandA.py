import boto3
import streamlit as st

st.subheader('RAG Using Knowledge Base from Amazon Bedrock', divider='rainbow')

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['text'])


bedrockClient = boto3.client('bedrock-agent-runtime', 'us-east-1')


def retrieveAndGenerate(input, kbId, modelArn):
    response = boto_runtime.retrieve_and_generate(
        input={
            'text': string
        },
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'FFLMW5Y2F8',
                'modelArn': 'anthropic.claude-3-5-sonnet-20241022-v2'
            },
            'type': 'KNOWLEDGE_BASE'
        },
           
    )
    
    return response


  

input = st.chat_input('Enter you input here...')
if input:
    with st.chat_message('user'):
        st.markdown(input)
    st.session_state.chat_history.append({"role":'user', "text":input})

    response = retrieveAndGenerate(input)
    # st.write(response)
    answer = response['output']['text']

    with st.chat_message('assistant'):
        st.markdown(answer)
    st.session_state.chat_history.append({"role":'assistant', "text": answer})

    if len(response['citations'][0]['retrievedReferences']) != 0:
        context = response['citations'][0]['retrievedReferences'][0]['content']['text']
        doc_url = response['citations'][0]['retrievedReferences'][0]['location']['s3Location']['uri']
        
        #Below lines are used to show the context and the document source for the latest Question Answer
        st.markdown(f"<span style='color:#FFDA33'>Context used: </span>{context}", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#FFDA33'>Source Document: </span>{doc_url}", unsafe_allow_html=True)
    
    else:
        st.markdown(f"<span style='color:red'>No Context</span>", unsafe_allow_html=True)
    

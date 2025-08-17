import streamlit as st
import requests
import uuid

# Set the page configuration
st.set_page_config(page_title="Lumif-ai", layout="wide")

# Use st.session_state for persistent variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Set up the sidebar for configuration
with st.sidebar:
    st.title("Configuration")
    
    # Model Name
    model_name = st.text_input(
        "Model Name",
        value="gemini-2.5-pro",
        help="Enter the name of the model to use for the chat service."
    )
    
    # Temperature
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help="Controls the randomness of the model's output. Lower values are more deterministic."
    )
    
    # System Instructions
    system_instructions = st.text_area(
        "System Instructions",
        value="""<prompt>
<task>
Search for and deploy an MCP server based on the user's request.
</task>

<instructions>
1. Begin by using the `scrape_as_markdown` tool to search for MCP servers.
2. Construct the URL for the search query by replacing `<searchable_query>` with the user's input.
3. If the user specifies a particular server, use the `scrape_as_markdown` tool again with the specific server's page link to get its configuration.
4. If the server configuration includes environmental variables, prompt the user for their values before deployment.
5. After obtaining a valid configuration and any necessary environment variables, deploy the server using the `deploy-mcp` tool.
6. Once the server has been deployed, you can start using that tool to serve the user's request.
</instructions>

<tools>
<tool name="scrape_as_markdown">
    <description>Searches and scrapes web content from a given URL and returns it in Markdown format.</description>
    <url>https://glama.ai/mcp/servers?query=<searchable_query>&sort=search-relevance%3Adesc&attributes=hosting%3Aremote-capable</url>
</tool>
<tool name="deploy-mcp">
    <description>Deploys a specified MCP server configuration. Requires a dictionary value for the configuration.</description>
</tool>
<tool name="list-mcp">
    <description>Lists all the deployed mcp servers by the user.</description>
</tool>
<tool name="delete-mcp">
    <description>Deletes a deployed mcp server.</description>
</tool>
</tools>

<constraints>
1. The target MCP server must be either an sse or a fully packaged configuration.
2. Do not select any servers that require cloning a repository.
3. The final configuration for the `deploy-mcp` tool must be a dictionary value.
</constraints>
</prompt>
        """,
        height=300,
        help="Provide instructions or context to guide the model's behavior."
    )

st.title("Lumif-ai")
st.write("An Agent to manage MCP servers")

# Display existing messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle user input
if user_query := st.chat_input("What is your message?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Display user message in the chat container
    with st.chat_message("user"):
        st.write(user_query)

    # Prepare the payload for the API
    payload = {
        "thread_id": st.session_state.thread_id,
        "model": model_name,
        "temperature": temperature,
        "prompt": system_instructions,
        "query": user_query,
    }

    try:
        # Make the API call
        response = requests.post(
            "http://127.0.0.1:8000/v1/chat_service/invoke/",
            json=payload,
            timeout=30  # Add a timeout for the request
        )
        
        # Check for successful response
        response.raise_for_status()

        # Get the AI's response from the JSON
        print("Response : ", response.json())
        ai_response = response.json().get("reply")
        
        # Display the AI's response
        with st.chat_message("assistant"):
            st.write(ai_response)
        
        # Add assistant's message to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred: {e}"
        st.error(error_message)
        st.session_state.messages.append({"role": "assistant", "content": f"Sorry, I was unable to connect to the server. Details: {e}"})

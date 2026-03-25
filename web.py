import streamlit as st
import os
from database.dbconn import db_init, delete_lead, sqlExecute
from dotenv import load_dotenv
from ai_agent import process_chat

load_dotenv()

adm_password = os.getenv('ADM_PWD')

db_init()

st.set_page_config(page_title="A-Simero Agency", 
                   page_icon="🚀", 
                   layout="wide",
                   initial_sidebar_state="collapsed")

# Sidebar: Admin Panel and Database preview
st.sidebar.title("🗄️ Admin Panel")
st.sidebar.markdown("Current data in the `Leads` table:")

try:
    all_data = sqlExecute("SELECT * FROM Leads")
    
    # Display placeholder if database is empty
    if not all_data:
        st.sidebar.info("No leads yet. Waiting for clients...")
    else:
        formatted_data = [
            {"ID": row[0], "Name": row[1], "Сontact Info": row[2], "contact_type": row[3], "Service": row[4], "Budget": row[5], "CreatedAt": row[6]} 
            for row in all_data
        ]
        st.sidebar.dataframe(formatted_data, use_container_width=True)
        
        st.sidebar.markdown("---") 
        st.sidebar.subheader("🔐 Access to the AI")

        access_password = st.sidebar.text_input("Access password:", type="password")

        if access_password == adm_password:
            st.sidebar.info(f"You are logged in as an administrator")

            lead_to_delete = st.sidebar.text_input("ID for delete:")
        
            if st.sidebar.button("Delete Lead"):
                delete_lead(lead_to_delete)
                st.rerun()

except Exception as e:
    st.sidebar.error(f"Failed to load DB: {e}")


# Main page: Fake agency website
st.title("🚀 A-Simero Digital Agency")
st.markdown("We build IT products that generate revenue: websites, applications, and AI integrations.")

# Mock services section
col1, col2, col3 = st.columns(3)
with col1:
    st.info("💻 **Web Development**\n\nLanding pages, corporate websites, and e-commerce platforms of any complexity.")
with col2:
    st.success("🤖 **AI Automation**\n\nNeural network integration, smart bots, and workflow automation.")
with col3:
    st.warning("📱 **Mobile Apps**\n\nNative and cross-platform applications for iOS and Android.")

st.markdown("---")

# Chat widget
st.subheader("💬 Discuss your project")
st.markdown("Our AI Manager **Alex** is ready to answer your questions right now!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Alex, the AI Manager at A-Simero. What kind of project are you looking to build?"}
    ]

ai_avatar_url = "https://www.d-id.com/wp-content/uploads/2023/12/D-ID-portrait_character.png"
# Render chat history
for msg in st.session_state.messages:
    avatar = ai_avatar_url if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Chat input field
if prompt := st.chat_input("Type your message here..."):
    # Save and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        
    # Placeholder for OpenAI API call
    with st.chat_message("assistant", avatar=ai_avatar_url):
        with st.spinner("Alex is typing..."):
            ai_reply = process_chat(st.session_state.messages)
            st.markdown(ai_reply)
    
    # Save and display assistant message
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
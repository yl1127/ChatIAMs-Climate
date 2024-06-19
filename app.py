from openai import OpenAI
import streamlit as st
from climate_IAMs import get_climate_change, get_chatiams

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the web source code](https://github.com/yl1127/ChatIAMs/blob/main/app.py)"
    "[Open in GitHub yl1127](https://github.com/yl1127/ChatIAMs)"

st.title("💬 ChatIAMs")
st.caption("🌎 A chatbot enhanced by Climate IAMs from IPCC")
st.caption("🌎 **Available Variables:**")
st.markdown("""
- **Surface Air Temperature Change**
- **Atmospheric Concentrations|CO2**
- **Effective Radiative Forcing**
  - **Effective Radiative Forcing|CO2**
  - **Effective Radiative Forcing|Aerosols**
    - **Effective Radiative Forcing|Aerosols|Direct Effect|BC**
    - **Effective Radiative Forcing|Aerosols|Direct Effect|OC**
    - **Effective Radiative Forcing|Aerosols|Direct Effect|SOx**
    - **Effective Radiative Forcing|Aerosols|Direct Effect**
    - **Effective Radiative Forcing|Aerosols|Indirect Effect**
- **Sea Level Change**
""")
st.caption("🌎 **Available Scenarios:**")
st.markdown("""
- **ssp119**
- **ssp126**
- **ssp245**
- **ssp370**
- **ssp460**
- **ssp585**
""")

st.caption("🌎 **Available Year:**")
st.markdown("""From 2024 to 2100
""")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # st.chat_message("assistant").write(st.session_state.messages)
    
    response = get_chatiams(st.session_state.messages, openai_api_key)
    # response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
    # msg = get_chatiams(prompt)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
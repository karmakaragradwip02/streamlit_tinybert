import os
import streamlit as st
import time
from PIL import Image

# Add title
st.title("This Is Title")

# Add heading
st.header("This Is Header")

#Add subheading
st.subheader("This is Subheading")

# Add text
st.text("This Is Text")

# Add input box
input_text = st.text_input("This Input Text", "type here ...")
st.text(input_text)

# Add text area
input_text = st.text_area("This Text Area", "type here ...")
st.text(input_text)

# Add markdown
st.markdown("This is a __Markdown__")
st.markdown("## This is Markdown with two hash")
st.markdown("""This a Markdown for different lines
1. first line
2. second line
3. third line""")

# Add button
button = st.button("Click Me")
if button: 
    st.text("The botton is pressed")
    st.info("I am clicked!! snap me first")
    st.toast("I will disappear")
    st.warning("this is warning")
    st.error("This is error")

# Add image
st.image("DEPLOY_MODEL_STREAMLIT/panda-1236875_640.jpg", width=500)
st.image("https://assets.gadgets360cdn.com/pricee/assets/product/202312/Mufasa_The_Lion_King_2_1703760981.jpg?downsize=680:*", width=500)

# Add check box
check = st.checkbox("Select me")
if check:
    st.text("Box Selected")
    st.image("DEPLOY_MODEL_STREAMLIT/panda-1236875_640.jpg", width=500)

# Add radio button
selection = st.radio("Choose your Model", ["NLP", "Image", "Audio"])
st.write(selection)

# Add select box
select_box = st.selectbox("Choose your Model", ["NLP", "Image", "Audio"])
st.write(select_box)

# Add multiselect
select_multi = st.multiselect("Choose your Model", ["NLP", "Image", "Audio"])
for select in select_multi:
    st.write(select)

# Add spinner for waiting
with st.spinner("Downloading........"):
    st.write("download your model here")
    time.sleep(1)

# Add slider
epoch = st.slider("Set Epoch", 0,50, step=10)
st.write(epoch)

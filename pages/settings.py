import streamlit as st
import json

# read the config file
with open('config.json','r') as f:
    config = json.load(f)

st.sidebar.header("Function Configs")

# ratio in sidebar to choose different functions' configs
f_config = st.sidebar.radio("Select one config",["-","Yande.re"])

# default
if f_config == "-":
    st.header("Settings")
    st.write("Please select a function in the sidebar.")
# Yande.re
if f_config == "Yande.re":
    st.header("Yande.re Configs")
    js = config["yande_re"]
    with st.container(border=True):
        for index in js:
            new_path = st.text_input(label= index,value=js[index],key=index)
            if new_path != js[index]:
                config["yande_re"][index] = new_path
                with open('config.json','w') as f:
                    json.dump(config,f,indent=4)
                    st.rerun()

    

            
            
         

    


import streamlit as st
import sys
sys.path.insert(0, '../')
from Login import get_friends, add_friend

st.title('Found: Find Your Friends Anytime.') # Placeholder

user = st.session_state.username

friends = get_friends(user) # Calls a function from the other script
                            # to avoid connecting to the db twice

'Welcome' + user

st.divider()
for i in friends:
    with st.container():

        col1,col2 = st.columns([0.3,0.7])

        col1.write(i)
        col2.write('location')

        st.divider()

def new_friend():
    add_friend(user, friend)

with st.popover("Add Friend!"):
    friend = st.text_input("Their Username")
    st.button('Add', on_click=new_friend)
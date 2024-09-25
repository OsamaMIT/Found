import streamlit as st
import sys
sys.path.insert(0, '../')
from Login import get_friends, add_friend, locate_friend, refresh_location, body

if 'load' not in st.session_state:
    st.session_state.load = True
if st.session_state.get('load'):
    st.session_state.load = False
    st.rerun()


st.title('Found: Find Your Friends Anytime.') # Placeholder

user = st.session_state.username

friends = get_friends(user) # Calls a function from the other script
                            # to avoid connecting to the db twice

def signal_refresh_location():
    refresh_location(user, location)

st.markdown(f'Welcome **{user}**')

location = st.text_input(label='Describe your location for your friends!')
st.button('Update', on_click=signal_refresh_location)

st.divider()
for i in friends:
    with st.container():

        col1,col2 = st.columns([0.3,0.7])

        col1.write(i)
        col2.write(locate_friend(i))

        st.divider()

def new_friend():
    add_friend(user, friend)

with st.popover("Add Friend!"):
    friend = st.text_input("Their Username")
    st.button('Add', on_click=new_friend)
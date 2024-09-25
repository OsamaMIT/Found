import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

if 'username' not in st.session_state:
    st.session_state.username = ''

# ------------------- Database Setup ------------------- #
# Create a new client and connect to the server
client = MongoClient(st.secrets['uri'], server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['Found']

# ------------------- Database Managment ------------------- #
def generate_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode('utf-8'))

# Function to retrieve friends on the Home page
def get_friends(user):
    doc = db['users'].find_one({'username': user})
    if doc:
        list = doc.get('friends')
        return list
    else:
        return []
    
# Function to add a new friend
def add_friend(user, friend):
    query = db['users'].find_one({'username': friend})
    doc = db['users'].find_one({'username': user})
    if query:
        #if 'friends' in doc:
        friends = doc.get('friends')
        print(friends)
        db['users'].update_one({'username': user}, {'$push': {'friends': friend}})
        # else:
        #      db['users'].update_one({'username': user}, {'$set': {'friends': friend}})
    else:
        return [], st.error('The user you are trying add does not exist.')

def locate_friend(friend):
    query = db['users'].find_one({'username': friend})
    if query:
        location = query.get('location')
        return location

def refresh_location(user, location):
    # query = db['users'].find_one({'username': user})
    db['users'].update_one({'username': user}, {'$set': {'location': str(location)}})

# ------------------- Designing page front end ------------------- #
st.set_page_config(page_title="Found", page_icon="🌍")

def check():
    user_doc = db['users'].find_one({'username': username_e})
    if user_doc:
        stored_hash = user_doc.get('pin')
        if bcrypt.checkpw(pin_e.encode('utf-8'), stored_hash.encode('utf-8')):
            st.session_state['switch_page'] = True
        else:
            st.error("Invalid username or pin")
    else:
        st.error("Username not found")

def create_account():
    hashed_pin = bcrypt.hashpw(pin_e.encode('utf-8'), bcrypt.gensalt())
    hashed_pin = hashed_pin.decode('utf-8')  # Convert bytes to string
    db['users'].insert_one({
        'username': username_e,
        'pin': hashed_pin,
        'friends': [],
        'location': '',
    })

    st.session_state['switch_page'] = True

body = st.container()
with body:
    st.title('Account Login')

    username_e = st.text_input('Username')
    pin_e = st.text_input('Pin', type='password')

    col1,col2 = st.columns(2)
    with col1:
        st.button('Log In', on_click=check)
    with col2:
        st.button('Sign Up', on_click=create_account)


if st.session_state.get('switch_page', False):
    st.session_state.username = username_e # Stores the user so that it doesn't reset when the page changes
    
    st.session_state['switch_page'] = False # Necessary so users can access the login page more than once
    st.session_state['load'] = True
    st.switch_page("pages/home.py")
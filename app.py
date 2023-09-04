import streamlit as st
import pyrebase
import pandas as pd
import uuid

# Firebase configuration
config = {
    "apiKey": "AIzaSyA3ZcRuGqAPpLZlOsdhUKwvWosZytPahog",
    "authDomain": "dbf-project-80294.firebaseapp.com",
    "databaseURL": "https://dbf-project-80294-default-rtdb.firebaseio.com",
    "projectId": "dbf-project-80294",
    "storageBucket": "dbf-project-80294.appspot.com",
    "messagingSenderId": "964184006717",
    "appId": "1:964184006717:web:067999f90836ae07a94a54",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Streamlit app
st.title("Firebase Streamlit App")

# Function to render and clear the entry form
def render_entry_form():
    st.write("Enter your information:")
    
    # Dropdown for selecting language
    language_options = ["Hindi", "English", "Gujarati"]
    selected_language = st.selectbox("Select Language", language_options)
    
    # Allow users to enter their own ID
    entry_id = st.text_input("Serial Number (ID)")
    
    name = st.text_input("Name", key="name_input")
    age = st.number_input("Age", min_value=0, max_value=150, key="age_input")
    mobile_number = st.text_input("Mobile Number", key="mobile_input")
    email = st.text_input("Email Address", key="email_input")

    if st.button("Submit"):
        if name and age and mobile_number and email:
            if not entry_id:
                st.error("Please enter a Serial Number (ID).")
                return
            
            # Generate ID based on the selected language
            if selected_language == "Hindi":
                entry_id = "H-" + entry_id
            elif selected_language == "English":
                entry_id = "E-" + entry_id
            elif selected_language == "Gujarati":
                entry_id = "G-" + entry_id
            
            # Check for duplicate ID before storing
            entries = db.child("entries").get()
            if entries.val() and entry_id in entries.val():
                st.error(f"ID {entry_id} already exists. Please choose a different ID.")
                return
            
            # Create a dictionary to store the data with the entered ID
            data = {
                "Name": name,
                "Age": age,
                "Mobile Number": mobile_number,
                "Email Address": email,
            }

            # Push the data to Firebase Realtime Database with the entered ID
            db.child("entries").child(entry_id).set(data)

            # Display a success message
            st.success("Data submitted successfully!")

            # Clear the input fields by rerunning the form rendering function
            st.experimental_rerun()

# Render the entry form
render_entry_form()

# Display the stored entries from Firebase in a tabular form
st.header("Stored Entries:")

# Fetch the data from Firebase
entries = db.child("entries").get()

if entries.val():
    data_dict = entries.val()
    df = pd.DataFrame(data_dict.values(), index=data_dict.keys())
    
    # Search functionality
    search_query = st.text_input("Search by Name", key="search_input")
    
    if search_query:
        filtered_df = df[df["Name"].str.contains(search_query, case=False)]
        st.dataframe(filtered_df)
    else:
        st.dataframe(df)
else:
    st.write("No entries found.")
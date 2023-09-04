import streamlit as st
import pyrebase
import pandas as pd

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
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=150)
    mobile_number = st.text_input("Mobile Number")
    email = st.text_input("Email Address")

    if st.button("Submit"):
        if name and age and mobile_number and email:
            # Create a dictionary to store the data
            data = {
                "Name": name,
                "Age": age,
                "Mobile Number": mobile_number,
                "Email Address": email,
            }

            # Push the data to Firebase Realtime Database
            db.child("entries").push(data)

            # Display a success message
            st.success("Data submitted successfully!")

            # Clear the input fields by rerunning the form rendering function
            st.experimental_rerun()

# Render the entry form
render_entry_form()

# Display the stored entries from Firebase
st.header("Stored Entries:")
# Fetch the data from Firebase
entries = db.child("entries").get()

if entries.val():
    data_list = list(entries.val().values())
    df = pd.DataFrame(data_list)

    # Search functionality
    search_query = st.text_input("Search by Name")
    
    if search_query:
        filtered_df = df[df["Name"].str.contains(search_query, case=False)]
        st.dataframe(filtered_df)
    else:
        st.dataframe(df)
else:
    st.write("No entries found.")
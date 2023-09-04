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

# Function to search and display records by ID
def search_record_by_id():
    st.subheader("Search Record by ID:")
    entry_id = st.text_input("Enter Serial Number (ID)")
    
    if st.button("Search"):
        if entry_id:
            entries = db.child("entries").child(entry_id).get()
            if entries.val():
                st.write("Found Record:")
                st.write(entries.val())
            else:
                st.error(f"No record found with ID {entry_id}.")
        else:
            st.error("Please enter a Serial Number (ID).")

# Function to edit and delete records
def edit_and_delete_records():
    st.subheader("Edit and Delete Records:")
    entry_id = st.text_input("Enter Serial Number (ID) to edit or delete")
    
    if st.button("Edit"):
        if entry_id:
            entries = db.child("entries").child(entry_id).get()
            if entries.val():
                st.write("Current Record:")
                st.write(entries.val())
                st.write("Edit the record below:")
                
                # Edit form
                name = st.text_input("Name", value=entries.val()["Name"])
                age = st.number_input("Age", min_value=0, max_value=150, value=entries.val()["Age"])
                mobile_number = st.text_input("Mobile Number", value=entries.val()["Mobile Number"])
                email = st.text_input("Email Address", value=entries.val()["Email Address"])
                
                if st.button("Save Changes"):
                    # Update the record with edited data
                    data = {
                        "Name": name,
                        "Age": age,
                        "Mobile Number": mobile_number,
                        "Email Address": email,
                    }
                    db.child("entries").child(entry_id).update(data)
                    st.success("Record updated successfully!")
            else:
                st.error(f"No record found with ID {entry_id}.")
        else:
            st.error("Please enter a Serial Number (ID) to edit.")
    
    if st.button("Delete"):
        if entry_id:
            entries = db.child("entries").child(entry_id).get()
            if entries.val():
                st.write("Current Record:")
                st.write(entries.val())
                if st.checkbox("Confirm Deletion"):
                    # Delete the record
                    db.child("entries").child(entry_id).remove()
                    st.success("Record deleted successfully!")
            else:
                st.error(f"No record found with ID {entry_id}.")
        else:
            st.error("Please enter a Serial Number (ID) to delete.")

# Render the entry form
render_entry_form()

# Search records by ID
search_record_by_id()

# Edit and delete records
edit_and_delete_records()

# Display the stored entries from Firebase in a tabular form
st.header("Stored Entries:")

# Fetch the data from Firebase
entries = db.child("entries").get()

if entries.val():
    data_dict = entries.val()
    df = pd.DataFrame(data_dict.values(), index=data_dict.keys())
    
    # Search functionality by Name
    search_query = st.text_input("Search by Name")
    
    if search_query:
        filtered_df = df[df["Name"].str.contains(search_query, case=False)]
        st.dataframe(filtered_df)
    else:
        st.dataframe(df)
else:
    st.write("No entries found.")
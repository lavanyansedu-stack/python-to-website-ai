import streamlit as st

def main():
    st.title("Greeting App")
    name = st.text_input("Enter your name:")
    if st.button("Submit"):
        if name:
            st.success(f"Welcome {name}")
        else:
            st.error("Please enter a name.")

if __name__ == "__main__":
    main()
import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = "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"

# Define a list to store search history
search_history = []

# Define the Streamlit app
def main():
    # Set the title and description of your app
    st.title("SnowGPT Website Template with Search History")
    st.write("Generate text using SnowGPT!")

    # Create a text input where the user can enter their prompt
    prompt = st.text_area("Enter your prompt:", value="Once upon a time,")

    # Create a button to generate text
    if st.button("Generate Text"):
        if prompt:
            # Generate text using the OpenAI GPT-3.5 model
            generated_text = generate_text(prompt)
            
            # Display the generated text to the user
            st.subheader("Generated Text:")
            st.write(generated_text)

            # Add the search to the search history
            search_history.append(prompt)
        else:
            st.warning("Please enter a prompt.")

    # Display the search history
    st.sidebar.title("Search History")
    if not search_history:
        st.sidebar.write("No search history yet.")
    else:
        for i, search in enumerate(reversed(search_history)):
            st.sidebar.write(f"{i + 1}. {search}")

# Function to generate text using the OpenAI GPT-3.5 model
def generate_text(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150  # Adjust the max_tokens as needed
        )
        return response.choices[0].text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

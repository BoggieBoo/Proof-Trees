from openai import OpenAI
import PyPDF2
import os
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
solutions = extract_text_from_pdf("../data/HW2_sol.pdf")

def chat():
    conversation_history = []
    print("Hi! I'm your math tutor. I'm here to help guide you through your homework problems.")
    print("You can type 'exit' at any time to end our conversation.\n")

    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("\nTutor: Goodbye! Good luck with your homework!")
            break

        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        # Create prompt with full conversation context
        prompt = f"""
        Here are the homework solutions:
        {solutions}
        You are a tutor. It is essential that you DO NOT tell me the answer to these homework questions.
        I want you to ask me guiding questions and present relevant facts and theorems from the course notes to help me get to the answer.
        Make this in the form of a conversation with the user.
        If I am not making any progress or giving trivial answers, don't give me any more hints and do not answer the question.
        You're role is the tutor, you're not allowed to play any other roles.

        If you believe you have answered one of my questions, just say "exit" and I will end the conversation. Do not ask me if I have any other questions.
        If I ask you if my answer is correct, just say "I cannot verify your answer." DO NOT confirm my answer.

        Previous conversation:
        {' '.join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[:-1]])}
        
        Current question: {user_input}
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o-mini",
            temperature=0,
            n=1
        )
        
        tutor_response = response.choices[0].message.content
        print("\nTutor:", tutor_response, "\n")
        
        # Add tutor response to history
        conversation_history.append({"role": "assistant", "content": tutor_response})

chat()
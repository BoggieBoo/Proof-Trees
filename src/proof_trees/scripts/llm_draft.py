import os
import json
from openai import OpenAI
from lean_compile import compile

file_path = 'data/FormL4/basic_test.json'

# index = 41 <- zero element kernel theorem

with open(file_path, 'r') as file:
    data = json.load(file)

def ask_llm(statement):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = (
        f"""
        This is the problem statement: {statement}
        Can you break up these proofs into states?
        States are sections the proof that get simplified with each tactic.
        Only return states, as a numbered list.
        """
        )
    response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="gpt-4o-mini", temperature=0, n=1)             
    return(response.choices[0].message.content)

def check_five(index):
    theorem = data[index]
    statement = theorem['nl_problem']
    for i in range(5):
        response = ask_llm(statement)
        if compile(response):
            return response



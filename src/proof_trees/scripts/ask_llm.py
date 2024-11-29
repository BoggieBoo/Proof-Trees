from lean_compile import lean_compile
from nl_rag import nl_rag
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# index = 41 <- zero element kernel theorem

def ask_llm(statement):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = (
        f"""
        Here are some examples before we start:

        Example 1:
        	
        NL: A: $ x_1,x_2,...,x_n \ge 0$ B: $ x_1^2+x_2^2+...+x_n^2 \ge 0$
        Lean: theorem lean_workbook_plus_522 (n : ℕ) (x : ℕ → ℝ) : ∀ i : ℕ, i ≤ n → x i ≥ 0 → ∑ i in Finset.range n, (x i)^2 ≥ 0 := by sorry
        We are writing a theorem to prove that A \implies B: where
        A: {statement["statement1"]}
        B: {statement["statement2"]}
        return the theorem with lean formalism and sorry for the tactic 
        Make sure you return in Lean 4 code that compiles 
        DO NO PROVIDE ANY TACTICS JUST WRITE sorry
        GIVE ME ONLY THE LEAN 4 CODE SO I CAN DIRECTLY COMPILE IT
        MAKE SURE YOU USE Mathlib4
        HAVE NO IMPORT STATEMENTS
        """
        )
    response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="gpt-4o-mini", temperature=0, n=1)             
    return(response.choices[0].message.content)

def ask_llm_again(statement, LLMoutput, error):
    client = OpenAI(api_key='sk-32g4iVVXfcUcLKNLpsTSG7SpgHE0CsWjrbnv7rnnaqT3BlbkFJa3l7JCjuz4hAJGiEErZhj82FYufDqQdycFldWzWxEA')
    prompt = (
        f"""

        Here are some examples before we start:

        {nl_rag(statement)}
        
        We are writing a theorem to prove that A \implies B: where
        A: {statement["statement1"]}
        B: {statement["statement2"]}
        return the theorem with lean formalism and sorry for the tactic 
        Make sure you return in Lean 4 code that compiles 
        DO NO PROVIDE ANY TACTICS JUST WRITE sorry
        this was your output the last time you tried to compile: {LLMoutput}
        and this was the error: {error}
        GIVE ME ONLY THE LEAN 4 CODE SO I CAN DIRECTLY COMPILE IT
        MAKE SURE YOU USE Mathlib4
        HAVE NO IMPORT STATEMENTS
        """
        )
    response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="gpt-4o-mini", temperature=0, n=1)             
    return(response.choices[0].message.content)

def process_llm_output(output):

    return "import Mathlib \n" + output.split("```")[1][5:]

def LLM_autoformal(statement: str):
    response = process_llm_output(ask_llm(statement))
    
    if lean_compile(response):
        print("FAILURE", statement, response, lean_compile(response))
        response_again = process_llm_output(ask_llm_again(statement, response, lean_compile(response)))
        print("AGAIN RESPONSE", statement, response_again, lean_compile(response_again))
    else: 
        print("Success", statement, response)
    print("HELLO WE ARE DONE")

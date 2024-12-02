from openai import OpenAI
import PyPDF2
import os
from dotenv import load_dotenv

load_dotenv()

default = {
    "formal":
    """
    theorem orthogonalComplement_iSup_eigenspaces_invariant ⦃v : E⦄ (hv : v ∈ (⨆ μ, eigenspace T μ)ᗮ) :
        T v ∈ (⨆ μ, eigenspace T μ)ᗮ := by
    rw [← Submodule.iInf_orthogonal] at hv ⊢
    exact T.iInf_invariant hT.invariant_orthogonalComplement_eigenspace v hv
    """
    ,
    "nl_problem":
    """
    The orthogonal complement of the direct sum of eigenspaces of a linear transformation is invariant under that transformation.
    """
    ,
    "nl_proof":
    """
    Let \\(v\\) be an element of the orthogonal complement of the direct sum of eigenspaces of a linear transformation \\(T\\). Then, by definition, \\(v\\) is orthogonal to every eigenvector of \\(T\\). Since \\(T\\) is a linear transformation, it preserves orthogonality. Therefore, \\(Tv\\) is also orthogonal to every eigenvector of \\(T\\). Hence, \\(Tv\\) is in the orthogonal complement of the direct sum of eigenspaces of \\(T\\).
    """
}

def extract_steps(theorem=False):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    if not theorem:
        theorem = default
    back = '\\'
    left = '{'
    right = '}'
    prompt = (
    f"""
    You are a mathematical expert and an expert user of Lean4. You will be given a formal proof of a mathematical theorem in Lean4, and an informal proof of the same theorem. For each line of the formal proof, write the step or steps from the informal proof that most directly correspond to the formal line. In your response, please avoid referring to specific theorems or definitions from the formal proof, and give as much detail in words as you can. The following is an example query and answer:
    
    Example Query:

    Formal Proof in Lean4:
    theorem hasEigenvalue_of_hasEigenvector {left}f : End R M{right} {left}μ : R{right} {left}x : M{right} (h : HasEigenvector f μ x) :
    HasEigenvalue f μ := by
    rw [HasEigenvalue, Submodule.ne_bot_iff]
    use x; exact h

    Informal Proof:
    **Theorem**: If a linear map has an eigenvector, then it has an eigenvalue.
    **Proof**: Let $f : V {back}to V$ be a linear map and let $v \in V$ be an eigenvector of $f$ with eigenvalue $\lambda$. Then, by definition, $f(v) = \lambda v$. This means that $v$ is a nonzero vector in the kernel of $f - \lambda I$, where $I$ is the identity map on $V$. Therefore, $f - \lambda I$ is not injective, and so it is not an isomorphism. Thus, $f - \lambda I$ is not surjective, and so there exists a nonzero vector $w \in V$ such that $(f - \lambda I)(w) = 0$. This means that $f(w) = \lambda w$, so $w$ is also an eigenvector of $f$ with eigenvalue $\lambda$. Therefore, $f$ has at least one eigenvalue, and so it has an eigenvalue.
    
    Example Output:

    1. **Formal Step**:
    theorem hasEigenvalue_of_hasEigenvector {left}f : End R M{right} {left}μ : R{right} {left}x : M{right} (h : HasEigenvector f μ x) :                      
    **Informal Step**:
    Let $f : M {back}to M$ be a linear map and let $x \in M$ be an eigenvector of $f$ with eigenvalue $\mu$. Suppose that f has an eigenvector x, corresponding to eigenvalue $\mu$.
    2. **Formal Step**:
    HasEigenvalue f μ := by
    **Informal Step**:
    The goal of our proof is to show that f has an eigenvalue $\mu$.
    3. **Formal Step**:
    rw [HasEigenvalue, Submodule.ne_bot_iff]
    **Informal Step**
    Then, by definition, $f(x) = \mu x$. This means that $x$ is a nonzero vector in the kernel of $f - \mu I$, where $I$ is the identity map on $V$. Therefore, $f - \mu I$ is not injective, and so it is not an isomorphism. Thus, $f - \mu I$ is not surjective, and so there exists a nonzero vector $w \in V$ such that $(f - \mu I)(w) = 0$. This means that $f(w) = \mu w$, so $w$ is also an eigenvector of $f$ with eigenvalue $\mu$. 
    4. **Formal Step**
    use x; exact h
    **Informal Step**
    This means that $f(w) = \lambda w$, so $w$ is also an eigenvector of $f$ with eigenvalue $\lambda$. Therefore, $f$ has at least one eigenvalue,  and so it has an eigenvalue.
    
    Now, please answer the following query:
    
    Formal Proof in Lean4: {theorem['formal']}


    Informal Proof:    
    **Theorem**: {theorem['nl_problem']}
    **Proof**: {theorem['nl_proof']}
    """
        )
    response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="gpt-4o-mini", temperature=0, n=1)             
    return(response.choices[0].message.content)

print(extract_steps())
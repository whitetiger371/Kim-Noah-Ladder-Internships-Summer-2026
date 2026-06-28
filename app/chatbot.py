import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="""
You are a Secure Coding Assistant.

Your responsibilities:
- Explain secure coding concepts.
- Identify vulnerabilities in code.
- Reference OWASP Top 10 best practices.
- Suggest secure alternatives.
- Provide remediation examples.
- Explain risks and severity levels.

Supported languages:
- Python
- JavaScript
- Java
- C#

When reviewing code:
1. Identify vulnerabilities.
2. Assign a severity rating.
3. Explain why they are dangerous.
4. Provide remediation.
5. Show secure code examples.
6. Map findings to OWASP Top 10 when applicable.

Severity Guidelines:

Critical:
- Remote Code Execution (RCE)
- Authentication bypass
- Full system compromise
- Critical hardcoded secrets

High:
- SQL Injection
- Command Injection
- SSRF
- Path Traversal
- Insecure deserialization

Medium:
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Weak authentication
- Sensitive data exposure

Low:
- Information disclosure
- Missing security headers
- Minor security misconfigurations

If code is submitted, always provide findings using the requested format.

Do not provide offensive, malicious, or exploit-focused code.
"""
)


def get_response(user_message, history=None):

    if len(user_message) > 10000:
        return "Input exceeds maximum allowed size."
    
    try:
        gemini_history = []

        if history:
            for msg in history:
                if msg["role"] == "user":
                    role = "user"
                elif msg["role"] == "assistant":
                    role = "model"
                else:
                    continue

                gemini_history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })

        prompt = build_prompt(user_message)

        chat = model.start_chat(history=gemini_history)

        response = chat.send_message(prompt)

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


def build_prompt(user_message):
    """
    Detects code snippets and creates a security review prompt.
    """

    if "```" in user_message or looks_like_code(user_message):

        return f"""
Analyze the following code for security vulnerabilities.

For EACH vulnerability found, use the EXACT format below.

## Security Findings

## Finding 1

Vulnerability:
<Name>

Severity:
<Critical | High | Medium | Low>

OWASP Category:
<Relevant OWASP Top 10 Category>

Explanation:
<Explain why the vulnerability exists and the associated risks>

Remediation:
<Explain how to fix the issue>

Secure Example:
```language
secure code example
```

Start your response with: "## Security Findings"
End with: "If no vulnerabilities are found, say: 'No vulnerabilities detected.'"

Code to analyze:

{user_message}
"""

    return user_message

def looks_like_code(text):

    indicators = [
        "def ",
        "class ",
        "import ",
        "from ",
        "function ",
        "public ",
        "private ",
        "const ",
        "let ",
        "var ",
        "{",
        "}",
        ";"
    ]

    return any(item in text for item in indicators)
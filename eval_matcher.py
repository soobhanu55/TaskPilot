"""Hand-labeled evaluation of the real matching logic in the notebook
(find_best_function): bag-of-words keyword intersection against a small
3-function registry. No LLM is actually called anywhere in this project
despite the "LLM + RAG" name -- this evaluates what's actually there.

Run: python eval_matcher.py
"""

from __future__ import annotations

functions = {
    "open_chrome": {
        "description": "Open Google Chrome browser",
        "code": "webbrowser.open('https://www.google.com')",
        "keywords": ["chrome", "browser", "google", "web", "internet", "open"],
    },
    "get_cpu_usage": {
        "description": "Retrieve current CPU usage",
        "code": "os.popen('wmic cpu get loadpercentage').read()",
        "keywords": ["cpu", "processor", "usage", "load", "system", "monitor"],
    },
    "execute_shell_command": {
        "description": "Execute a shell command safely",
        "code": "os.popen(command).read()",
        "keywords": ["shell", "command", "execute", "run", "terminal"],
    },
}


def find_best_function(prompt: str) -> str:
    prompt_words = set(prompt.lower().split())
    best_match = None
    best_score = 0
    for func_name, func_data in functions.items():
        keywords = set(func_data["keywords"])
        description_words = set(func_data["description"].lower().split())
        score = len(prompt_words.intersection(keywords.union(description_words)))
        if score > best_score:
            best_score = score
            best_match = func_name
    return best_match if best_score > 0 else "No match found"


EVAL_SET = [
    ("Can you open my browser?", "open_chrome"),
    ("Please launch Chrome for me", "open_chrome"),
    ("I want to browse the web", "open_chrome"),
    ("Open google please", "open_chrome"),
    ("What's my CPU usage right now?", "get_cpu_usage"),
    ("Check the processor load", "get_cpu_usage"),
    ("Monitor system usage", "get_cpu_usage"),
    ("How much CPU am I using", "get_cpu_usage"),
    ("Run this shell command for me", "execute_shell_command"),
    ("Execute a terminal command", "execute_shell_command"),
    ("I need to run something in the shell", "execute_shell_command"),
    ("Please execute this in terminal", "execute_shell_command"),
    ("What's the weather like today?", "No match found"),
    ("Tell me a joke", "No match found"),
    ("Book a flight to Paris", "No match found"),
    ("What time is it?", "No match found"),
    # Genuinely ambiguous / adversarial cases -- kept in rather than removed
    ("Open the terminal and run a command to check the browser", "execute_shell_command"),
    ("Show me system information", "get_cpu_usage"),
    ("Launch chrome and check CPU usage", "open_chrome"),  # ties broken by dict iteration order
    ("execute open run", "execute_shell_command"),
]


def main() -> None:
    correct = 0
    for prompt, expected in EVAL_SET:
        actual = find_best_function(prompt)
        hit = actual == expected
        correct += int(hit)
        print(f"{'OK ' if hit else 'MISS'} | {prompt[:45]:45s} | expected={expected:22s} got={actual}")

    n = len(EVAL_SET)
    print(f"\nAccuracy: {correct}/{n} ({100*correct/n:.1f}%)")


if __name__ == "__main__":
    main()

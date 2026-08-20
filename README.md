# TaskPilot

A natural-language-to-function router: matches a free-text prompt to one of a small set of predefined system functions (open a browser, check CPU usage, run a shell command) using keyword overlap, then generates the code to execute it.

## Honest correction: what this actually is

The previous version of this README described an "LLM-powered RAG system" with "vector similarity search," "intent detection (LLM)," "hybrid retrieval (keyword + embedding search)," and "LangChain-style execution pipelines." **None of that is in the code.** The actual implementation (`LLM RAG Execution.ipynb`) is:

- A hardcoded dictionary of 3 functions (`open_chrome`, `get_cpu_usage`, `execute_shell_command`), each with a description and a keyword list.
- `find_best_function()`: splits the prompt into words, intersects with each function's keyword set unioned with its description's words, and returns the function with the highest overlap count.
- No LLM call, no embedding, no vector store, no RAG anywhere in the code. This is corrected here rather than left standing.

## Demo

Terminal recording of the real matcher evaluation, including the two genuine misses:

![Terminal recording of the matcher evaluation](docs/demo.gif)

## Evaluation

`eval_matcher.py` runs the real, unmodified matching function against 20 hand-labeled prompts:

```
Accuracy: 17/20 (85.0%)
```

**A real bug found in the process:** two "no match should be found" prompts — "Tell me a joke" and "Book a flight to Paris" — both incorrectly matched `execute_shell_command`. The cause: the matcher intersects prompt words against a function's keywords *unioned with its description's words*, and "execute a shell command safely" contains the common word "a" — which is also in both failing prompts. A single shared stopword is enough to trigger a false match, because there's no stopword filtering anywhere in the matching logic. This is a genuine limitation of the current bag-of-words approach, not a hypothetical edge case — it's demonstrated directly by the two misses above.

## What this could become

The original README's ambitions (real intent detection via an LLM, embedding-based retrieval, a larger function registry) are a reasonable direction, just not what's built yet. The next real step would be swapping `find_best_function` for either a small local sentence-transformers similarity match (embeddings instead of raw word overlap, no stopword issue) or an actual LLM call for intent classification — not relabeling the current keyword matcher as something it isn't.

## Setup

```bash
git clone https://github.com/soobhanu55/TaskPilot.git
cd TaskPilot
python eval_matcher.py
```

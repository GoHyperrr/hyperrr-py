# Hyperrr SDK (Python)

Hyperrr is a **prompt runtime engine** that lets you compose, reuse, and execute prompts like code.

It introduces a **DSL + AST + execution model** for prompts, enabling:

* Reusable prompt packages
* Nested prompt composition
* Remote prompt resolution (registry)
* Strong input validation

---

## 🚀 Installation

```bash
pip install hyperrr
```

---

## ⚡ Quick Example

```python
from hyperrr import prompt

result = prompt(
    '{{ prompt("viraj/sample@1") }}',
    name="Viraj"
)

print(result)
```

---

## 🧠 Core Concepts

### 1. Prompt DSL

```jinja
---
name: hello_prompt
inputs:
  name: string
---

Hello {{ name }} 👋
```

---

### 2. Prompt Calls

```jinja
{{ prompt("org/name@version") }}
```

---

### 3. Nested Composition

```jinja
Hello
{{ prompt("org/header@1") }}
{{ prompt("org/body@1") }}
```

---

## 🏗 Architecture

```text
Input String
   ↓
Parser → AST
   ↓
Executor → Runtime Evaluation
   ↓
Resolver → Fetch Prompt Content
```

---

### 🔹 Parser

* Converts prompt into AST
* No IO
* Handles:

  * Variables
  * Prompt calls

---

### 🔹 AST Nodes

* `TextNode`
* `VariableNode`
* `PromptCallNode`

---

### 🔹 Executor

* Evaluates AST
* Resolves nested prompts
* Handles input propagation

---

### 🔹 Resolver

* Fetches prompt content
* Supports:

  * Registry
  * Local files

---

## 🔄 Input Propagation

Inputs automatically flow into nested prompts:

```python
prompt('{{ prompt("a@1") }}', name="Viraj")
```

---

## 📦 Registry Integration

```python
prompt('{{ prompt("viraj/sample@1") }}')
```

---

## 🧪 Validation

Inputs are validated against schema:

```yaml
inputs:
  name: string
```

---

## 📁 Cache

Prompts are cached locally:

```text
~/.hyperrr/cache/
```

---

## 🔥 Features

* AST-based execution
* Nested prompt composition
* Remote registry support
* Input validation
* Disk caching

---

# 🚧 Future Roadmap

## 1. Subpath Support

```python
prompt("org/name@1:header")
```

---

## 2. Prompt Functions

```jinja
{{ uppercase(name) }}
```

---

## 3. Control Flow

```jinja
{{ if condition }}
{{ for item in items }}
```

---

## 4. Streaming Execution

---

## 5. In-memory Cache Layer

---

## 6. Multi-language SDKs

* JS
* Go

---

# 🧠 Vision

Hyperrr turns prompts into:

> **Composable, versioned, executable units — like code packages**

---

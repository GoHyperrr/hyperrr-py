# 🚀 Hyperrr SDK — Specification & Documentation

## ✨ Overview

**Hyperrr** is a lightweight prompt runtime that lets you:

* Write reusable prompts
* Compose prompts from other prompts
* Pass structured inputs
* Run prompts from files or inline strings

---

## 🧠 Core Philosophy

> **A prompt is a pure function**

```text
prompt(ref, inputs) → string
```

* No global state
* No side effects
* Deterministic execution

---

## ⚡ Quick Start

### Install

```bash
pip install hyperrr
```

---

### Run an inline prompt

```python
from hyperrr import prompt

print(prompt("Hello {{ name }}", name="Viraj"))
```

---

### Run a file prompt

```python
print(prompt("./hello.prompt", name="Viraj"))
```

---

## 📄 Prompt File Format

A `.prompt` file contains:

```text
---
name: example
inputs:
  name: string
  age: string?
---
Hello {{ name }}! You are {{ age }} years old.
```

---

### Structure

| Section             | Description              |
| ------------------- | ------------------------ |
| Frontmatter (`---`) | Optional metadata (YAML) |
| Body                | Prompt template          |

---

## 🧩 Variables

Variables are defined using:

```jinja
{{ variable_name }}
```

---

### Example

```jinja
Hello {{ name }}
```

---

### Passing Inputs

```python
prompt("Hello {{ name }}", name="Viraj")
```

---

## 📥 Inputs Schema

Defined in frontmatter:

```yaml
inputs:
  name: string
  age: string?
```

---

### Rules

| Syntax    | Meaning           |
| --------- | ----------------- |
| `string`  | required          |
| `string?` | optional          |
| dict      | supports defaults |

---

### Example with default

```yaml
inputs:
  tone:
    type: string
    default: formal
```

---

## 🧱 Prompt Composition

You can reuse prompts using:

```jinja
{{ prompt("ref", key=value) }}
```

---

### Example

#### `child.prompt`

```jinja
Summary: {{ text }}
```

#### `parent.prompt`

```jinja
Write about {{ topic }}

{{ prompt("./child.prompt", text=topic) }}
```

---

### Execution

```python
prompt("./parent.prompt", topic="AI")
```

---

### Output

```text
Write about AI

Summary: AI
```

---

## 🔗 Prompt References

Hyperrr supports multiple prompt sources:

| Type              | Example              |
| ----------------- | -------------------- |
| File              | `"./a.prompt"`       |
| Inline            | `"Hello {{name}}"`   |
| Registry (future) | `"org/name:version"` |

---

## ⚙️ Resolution System

Hyperrr resolves prompts using a deterministic chain:

```text
File → Registry → Inline
```

---

### Built-in Resolvers

| Resolver           | Purpose                 |
| ------------------ | ----------------------- |
| `FileResolver`     | local `.prompt` files   |
| `InlineResolver`   | fallback for strings    |
| `RegistryResolver` | (future) remote prompts |

---

## 🧠 Execution Pipeline

```text
prompt(ref, inputs)
   ↓
resolve(ref) → string
   ↓
parse(string) → (schema, AST)
   ↓
validate(schema, inputs)
   ↓
render(AST, inputs)
   ↓
output
```

---

## 🌳 AST Model

Hyperrr parses prompts into an Abstract Syntax Tree:

### Node Types

* `TextNode`
* `VariableNode`

---

### Example

```jinja
Hello {{ name }}
```

Becomes:

```python
[
  TextNode("Hello "),
  VariableNode("name")
]
```

---

## 🔄 Prompt Inlining (Compile-Time)

Nested prompts are:

> **Resolved and inlined at parse time**

---

### Example

```jinja
{{ prompt("./child.prompt", text=topic) }}
```

Becomes:

```jinja
Summary: {{ topic }}
```

---

### Benefits

* No runtime recursion
* Deterministic execution
* Easier debugging

---

## ✅ Validation

Validation happens in two stages:

---

### 1. Schema Validation

Ensures required inputs exist.

```python
prompt("./a.prompt", name="Viraj")  # OK
prompt("./a.prompt")                # Error
```

---

### 2. Runtime Validation

Ensures all variables exist during rendering.

```jinja
{{ age }}
```

If `age` missing → error.

---

## ⚠️ Important Rules

### 1. Optional inputs are not optional in template

```yaml
age: string?
```

Still requires:

```jinja
{{ age }}
```

Unless handled manually.

---

### 2. All variables must resolve

```text
Missing variable → runtime error
```

---

### 3. Prompt composition requires explicit inputs

```jinja
{{ prompt("./child.prompt") }} ❌
```

```jinja
{{ prompt("./child.prompt", text=topic) }} ✅
```

---

## 🧪 Examples

---

### Inline Prompt

```python
prompt("Sum: {{ a }} + {{ b }}", a=1, b=2)
```

---

### File Prompt

```python
prompt("./math.prompt", a=1, b=2)
```

---

### Nested Prompt

```jinja
{{ prompt("./child.prompt", text=topic) }}
```

---

## 🧱 Error Types

| Error                   | Description                |
| ----------------------- | -------------------------- |
| `PromptParseError`      | invalid prompt format      |
| `PromptResolutionError` | failed to load prompt      |
| `PromptRenderError`     | missing variables / inputs |

---

## 🧠 Design Decisions

### Why AST?

* Enables composition
* Enables static analysis
* Avoids string hacks

---

### Why no runtime recursion?

* Simpler execution model
* Better performance
* Easier debugging

---

### Why resolver chain?

* Extensible
* Deterministic
* Future registry support

---

## 🚀 Roadmap

* [ ] Registry support (`org/name:version`)
* [ ] Type validation
* [ ] Conditionals (`if`)
* [ ] Defaults in templates
* [ ] Dependency graph
* [ ] Prompt packaging

---

## 💡 Philosophy

Hyperrr is designed to be:

```text
Simple to start
Composable by design
Powerful when scaled
```
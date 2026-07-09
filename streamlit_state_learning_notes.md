# Streamlit State Learning Notes

## Big Idea

Streamlit runs a Python script from top to bottom to build the page.

When the user interacts with a widget, Streamlit usually reruns the whole script from top to bottom again.

Session state is used when we want Streamlit to remember values between reruns.

---

## Key Terms

### State

State means the current stored information of the app.

Example:

```python
st.session_state["name"] = "Alice"
```

The app now remembers:

```text
name = Alice
```

Simple meaning:

> State is what the app remembers right now.

---

### Session

A session is one user's active visit to the Streamlit app.

If I open the app in my browser, I have one session.
If another user opens the same app, they have a different session.

Simple meaning:

> A session is one user's own running copy of the app.

---

### Session State

`st.session_state` is Streamlit's memory for one session.

It behaves like a Python dictionary:

```python
st.session_state["name"] = "Alice"
st.session_state["age"] = 20
```

You can imagine it like this:

```python
{
    "name": "Alice",
    "age": 20
}
```

Simple meaning:

> Session state is the app's memory for one user session.

---

### Widget

A widget is an interactive UI element.

Examples:

```python
st.button("Submit")
st.text_input("Name")
st.slider("Age")
st.checkbox("Agree")
```

Simple meaning:

> A widget is something the user can interact with.

---

### State Key

A state key is the name used to store or find a value in `st.session_state`.

Example:

```python
st.session_state["name"]
```

Here, `"name"` is the state key.

More specific term:

> session state key

---

### State Value

A state value is the data stored under a state key.

Example:

```python
st.session_state["name"] = "Alice"
```

Here:

```python
"name"
```

is the state key.

```python
"Alice"
```

is the state value.

---

### Widget Key

A widget key is the `key` parameter given to a widget.

Example:

```python
st.text_input("Name", key="name")
```

Here:

```python
key="name"
```

does two things:

1. Gives the widget a unique identity.
2. Connects the widget value to `st.session_state["name"]`.

So `"name"` is both:

- the widget key
- the session state key

---

## Text Input and Session State

Example:

```python
st.text_input("Name", key="name")
```

This creates a text input widget and connects it to:

```python
st.session_state["name"]
```

If the user types:

```text
Alice
```

Streamlit stores:

```python
st.session_state["name"] = "Alice"
```

Input widgets like `st.text_input`, `st.slider`, and `st.checkbox` can update their own values in session state automatically when a `key` is provided.

---

## Button Rerun Behavior

A button click does not automatically update my custom session state values.

Example:

```python
if st.button("Jane"):
    st.session_state["name"] = "Jane Doe"
```

When the button is clicked:

1. Streamlit reruns the whole script.
2. `st.button("Jane")` returns `True` for that run.
3. The code inside the `if` block runs.
4. Then `st.session_state["name"]` changes.

Important:

> The click makes `st.button()` return `True`. My code still has to update the session state value.

---

## Why the First Header Shows the Old Value

Example:

```python
if "name" not in st.session_state:
    st.session_state["name"] = "John Doe"

st.header(st.session_state["name"])

if st.button("Jane"):
    st.session_state["name"] = "Jane Doe"

if st.button("John"):
    st.session_state["name"] = "John Doe"

st.header(st.session_state["name"])
```

When I first open the app:

1. `"name"` is not in session state.
2. Streamlit sets it to `"John Doe"`.
3. First header shows `"John Doe"`.
4. Second header also shows `"John Doe"`.

When I click `Jane`:

1. Streamlit reruns the whole script.
2. At the start of the rerun, `st.session_state["name"]` is still `"John Doe"`.
3. First header shows `"John Doe"`.
4. `st.button("Jane")` returns `True`.
5. The code changes `st.session_state["name"]` to `"Jane Doe"`.
6. Second header shows `"Jane Doe"`.

The first header does not change immediately because it already ran before the state was updated.

Important note:

> Session state changes do not go back and update code that has already executed in the current rerun.

---

## Simple Fix: Move State Updates Before Display

Better order:

```python
if "name" not in st.session_state:
    st.session_state["name"] = "John Doe"

if st.button("Jane"):
    st.session_state["name"] = "Jane Doe"

if st.button("John"):
    st.session_state["name"] = "John Doe"

st.header(st.session_state["name"])
```

Here, the button logic happens before the header is displayed.

---

## Callback Function

A callback function is a normal Python function that we pass to Streamlit.

Streamlit calls it later when a widget event happens.

Normal function call:

```python
change_name("Jane Doe")
```

I call it immediately.

Callback:

```python
st.button("Jane", on_click=change_name, args=("Jane Doe",))
```

I am saying:

> Streamlit, when this button is clicked, please call `change_name`.

So callback means:

> A function passed into another system, to be called later.

---

## Callback Example

```python
import streamlit as st

if "name" not in st.session_state:
    st.session_state["name"] = "John Doe"

def change_name(name):
    st.session_state["name"] = name

st.header(st.session_state["name"])

st.button("Jane", on_click=change_name, args=("Jane Doe",))
st.button("John", on_click=change_name, args=("John Doe",))

st.header(st.session_state["name"])
```

When I click `Jane`:

1. Streamlit runs the callback first.
2. The callback changes `st.session_state["name"]` to `"Jane Doe"`.
3. Then Streamlit reruns the whole script.
4. The first header already sees `"Jane Doe"`.

This solves the old-value problem.

---

## What Is `args`?

`args` is pronounced like:

```text
ar-gz
```

It is short for:

```text
arguments
```

In this code:

```python
st.button("Jane", on_click=change_name, args=("Jane Doe",))
```

`args` tells Streamlit what values to pass into the callback function.

This means:

```python
change_name("Jane Doe")
```

For one argument, the tuple needs a comma:

```python
("Jane Doe",)
```

Without the comma:

```python
("Jane Doe")
```

Python treats it as just a string, not a tuple.

A list also works:

```python
st.button("Jane", on_click=change_name, args=["Jane Doe"])
```

---

## What Is `st.container()`?

`st.container()` is not an input widget.

It is a layout container.

Simple meaning:

> A container is a place on the page where I can put Streamlit elements later.

Example:

```python
begin = st.container()
```

This creates an empty place on the page and saves it in the variable `begin`.

Later:

```python
begin.text_input("Name", key="name")
```

This means:

> Put the text input inside the earlier container.

---

## Using `st.container()` to Reorder Rendering

Example:

```python
import streamlit as st

begin = st.container()

if st.button("Clear name"):
    st.session_state.name = ""

if st.button("Streamlit!"):
    st.session_state.name = "Streamlit"

begin.text_input("Name", key="name")
```

The page looks like this:

```text
[Name text input]

[Clear name button]
[Streamlit! button]
```

But the code logic runs like this:

```text
1. Create a container placeholder near the top
2. Handle button logic
3. Update session state
4. Render the text input inside the earlier container
```

This lets the text input appear at the top while still allowing the button logic to run before the text input is created.

Important note:

> `st.container()` helps control where things appear on the page. It does not store input by itself.

---

## Summary

- Streamlit reruns the whole script after widget interaction.
- `st.session_state` remembers values between reruns.
- A widget `key` can connect a widget to a session state key.
- Button clicks make `st.button()` return `True`, but they do not automatically update custom session state values.
- Code runs top to bottom, so display code above a state update may show the old value.
- Callback functions run before the main script rerun.
- `args` passes values into a callback function.
- `st.container()` is a layout tool used to reserve a place on the page and fill it later.

import tkinter as tk
import re
import math

# ---------------------------------------------------------
# AI CALCULATOR
# Tkinter GUI + simple Natural Language Processing
# ---------------------------------------------------------

root = tk.Tk()
root.title("AI Natural Language Calculator")
root.geometry("650x500")
root.resizable(False, False)

# -------------------- NLP FUNCTIONS --------------------

def clean_text(text):
    """Convert user input into lowercase and normalize symbols."""
    text = text.lower().strip()

    replacements = {
        "×": "*",
        "x": "*",
        "÷": "/",
        "^": "**"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def extract_number(text):
    """Extract the first number from a sentence."""
    match = re.search(r"-?\d+(?:\.\d+)?", text)

    if match:
        return float(match.group())

    return None


def calculate_percentage(text):
    """
    Understand examples such as:
    25% of 800
    what is 25 percent of 800
    """
    pattern = r"(-?\d+(?:\.\d+)?)\s*(?:%|percent|percentage)\s*(?:of)\s*(-?\d+(?:\.\d+)?)"

    match = re.search(pattern, text)

    if match:
        percentage = float(match.group(1))
        number = float(match.group(2))
        return (percentage / 100) * number

    return None


def evaluate_expression(text):
    """
    Extract a basic mathematical expression and calculate it.
    Supports +, -, *, / and **.
    """
    expression = re.sub(r"[^0-9+\-*/(). ]", "", text)

    if not expression.strip():
        return None

    # Prevent unsafe expressions
    if "**" in expression:
        # Keep power operation allowed
        pass

    try:
        # eval is restricted to a math-expression-only string
        result = eval(expression, {"__builtins__": None}, {})
        return result
    except:
        return None


def calculate_square_root(text):
    """Understand square root questions."""
    number = extract_number(text)

    if number is not None and (
        "square root" in text
        or "sqrt" in text
    ):
        if number < 0:
            return "Cannot calculate square root of a negative number."

        return math.sqrt(number)

    return None


def calculate_square(text):
    """Understand questions such as 'square of 12'."""
    number = extract_number(text)

    if number is not None and "square of" in text:
        return number ** 2

    return None


def calculate_cube(text):
    """Understand questions such as 'cube of 5'."""
    number = extract_number(text)

    if number is not None and "cube of" in text:
        return number ** 3

    return None


def add_numbers(text):
    """Understand requests such as 'add 10, 20 and 30'."""
    if "add" not in text and "sum" not in text:
        return None

    numbers = re.findall(r"-?\d+(?:\.\d+)?", text)

    if len(numbers) >= 2:
        return sum(float(n) for n in numbers)

    return None


def subtract_numbers(text):
    """Understand requests such as 'subtract 5 from 20'."""
    match = re.search(
        r"subtract\s+(-?\d+(?:\.\d+)?)\s+from\s+(-?\d+(?:\.\d+)?)",
        text
    )

    if match:
        first = float(match.group(1))
        second = float(match.group(2))
        return second - first

    return None


def multiply_numbers(text):
    """Understand requests such as 'multiply 8 and 7'."""
    if "multiply" not in text and "product" not in text:
        return None

    numbers = re.findall(r"-?\d+(?:\.\d+)?", text)

    if len(numbers) >= 2:
        result = 1
        for n in numbers:
            result *= float(n)
        return result

    return None


def divide_numbers(text):
    """Understand requests such as 'divide 100 by 4'."""
    match = re.search(
        r"divide\s+(-?\d+(?:\.\d+)?)\s+(?:by)\s+(-?\d+(?:\.\d+)?)",
        text
    )

    if match:
        first = float(match.group(1))
        second = float(match.group(2))

        if second == 0:
            return "Cannot divide by zero."

        return first / second

    return None


def format_result(result):
    """Make results easier to read."""
    if isinstance(result, float) and result.is_integer():
        return str(int(result))

    return str(result)


def ai_calculate(user_text):
    """
    Main NLP decision system.
    It identifies the user's intent and sends the
    request to the appropriate calculator function.
    """
    text = clean_text(user_text)

    if not text:
        return "Please type a question."

    # Greetings
    if text in ["hi", "hello", "hey"]:
        return "Hello! Ask me a mathematical question."

    # Help
    if text == "help" or "what can you do" in text:
        return (
            "Try:\n"
            "• What is 25% of 800?\n"
            "• What is the square root of 144?\n"
            "• Square of 12\n"
            "• Cube of 5\n"
            "• Add 10, 20 and 30\n"
            "• Subtract 5 from 20\n"
            "• Multiply 8 and 7\n"
            "• Divide 100 by 4\n"
            "• Calculate 25 + 10 * 2"
        )

    result = calculate_percentage(text)
    if result is not None:
        return format_result(result)

    result = calculate_square_root(text)
    if result is not None:
        return format_result(result)

    result = calculate_square(text)
    if result is not None:
        return format_result(result)

    result = calculate_cube(text)
    if result is not None:
        return format_result(result)

    result = add_numbers(text)
    if result is not None:
        return format_result(result)

    result = subtract_numbers(text)
    if result is not None:
        return format_result(result)

    result = multiply_numbers(text)
    if result is not None:
        return format_result(result)

    result = divide_numbers(text)
    if result is not None:
        return format_result(result)

    # Basic arithmetic expression
    result = evaluate_expression(text)
    if result is not None:
        return format_result(result)

    return (
        "I couldn't understand that question.\n\n"
        "Try: 'What is 25% of 800?' or 'Calculate 45 + 12'."
    )


# -------------------- GUI FUNCTIONS --------------------

def ask_ai():
    question = question_entry.get().strip()

    answer = ai_calculate(question)

    answer_box.config(state="normal")
    answer_box.delete("1.0", tk.END)
    answer_box.insert(tk.END, answer)
    answer_box.config(state="disabled")


def clear_all():
    question_entry.delete(0, tk.END)

    answer_box.config(state="normal")
    answer_box.delete("1.0", tk.END)
    answer_box.config(state="disabled")


def use_example(example):
    question_entry.delete(0, tk.END)
    question_entry.insert(0, example)
    ask_ai()


# -------------------- GUI --------------------

title_label = tk.Label(
    root,
    text="AI Natural Language Calculator",
    font=("Arial", 24, "bold")
)
title_label.pack(pady=15)

instruction_label = tk.Label(
    root,
    text="Type a mathematical question in normal English:",
    font=("Arial", 13)
)
instruction_label.pack()

question_entry = tk.Entry(
    root,
    font=("Arial", 17),
    width=50
)
question_entry.pack(pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

ask_button = tk.Button(
    button_frame,
    text="Ask AI",
    font=("Arial", 13, "bold"),
    width=12,
    command=ask_ai
)
ask_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(
    button_frame,
    text="Clear",
    font=("Arial", 13),
    width=12,
    command=clear_all
)
clear_button.grid(row=0, column=1, padx=5)

# Answer
answer_label = tk.Label(
    root,
    text="Answer:",
    font=("Arial", 15, "bold")
)
answer_label.pack(pady=(15, 5))

answer_box = tk.Text(
    root,
    font=("Arial", 14),
    width=52,
    height=7,
    wrap="word"
)
answer_box.pack()
answer_box.config(state="disabled")

# Examples
examples_frame = tk.Frame(root)
examples_frame.pack(pady=15)

examples = [
    "What is 25% of 800?",
    "What is the square root of 144?",
    "Add 10, 20 and 30"
]

for i, example in enumerate(examples):
    example_button = tk.Button(
        examples_frame,
        text=example,
        font=("Arial", 10),
        command=lambda e=example: use_example(e)
    )
    example_button.grid(row=0, column=i, padx=3)


root.mainloop()

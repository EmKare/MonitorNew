import tkinter as tk

def check_input():
    try:
        # Try converting the entry text to a float
        float(entry.get())
        label.config(text="Valid number")
    except ValueError:
        label.config(text="Error")

def clear_label(event):
    # Clear the label text with a slight delay after focusing the Entry
    root.after(10, lambda: label.config(text=""))

# Create the main window
root = tk.Tk()
root.title("Number Checker")

# Create an Entry widget
entry = tk.Entry(root)
entry.pack(pady=10)
entry.bind("<FocusIn>", clear_label)  # Bind FocusIn event to clear_label function

# Create a Button to check input
button = tk.Button(root, text="Check", command=check_input)
button.pack(pady=5)

# Create a Label to display messages
label = tk.Label(root, text="")
label.pack(pady=10)

# Run the application
root.mainloop()

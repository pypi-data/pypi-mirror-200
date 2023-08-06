import os
import tkinter as tk
import re
from tkinter import messagebox
from typing import Optional, Tuple, Union


def show_warning(title: str, message: str):
    """
    Displays a warning message box with the given title and message.

    Args:
        title (str): The title of the warning message box.
        message (str): The message to be displayed in the warning message box.

    Returns:
        None: This function does not return anything.

    Raises:
        N/A

    Example:
        >>> show_warning("Warning", "This is a warning message.")
    """
    messagebox.showwarning(title, message)


def show_info(title: str, message: str):
    messagebox.showinfo(title, message)


def show_error(title: str, message: str):
    messagebox.showerror(title, message)


def get_user_input(
    linesinputbox: int = 1,
    size: str = "300x150",
    title: str = "Your input",
    textabovebox: str = "Enter your text below:",
    submitbutton: str = "Submit",
    regexcheck: str = ".*",
    showerror: Union[Tuple[str, str], None] = ("Error", "Try again!"),
    showinfo: Union[Tuple[str, str], None] = None,
    showwarning: Union[Tuple[str, str], None] = None,
    icon=None,
) -> Optional[str]:
    """
    Displays a dialog box with a text input box and a submit button.

    Args:
        linesinputbox (int): The number of lines to display in the text input box. Defaults to 1.
        size (str): The size of the window in pixels. Defaults to "300x150".
        title (str): The title of the window. Defaults to "Your input".
        textabovebox (str): The text to display above the text input box. Defaults to "Enter your text below:".
        submitbutton (str): The text to display on the submit button. Defaults to "Submit".
        regexcheck (str): A regular expression to validate the user's input. Defaults to ".*" (match any string).
        showerror (Tuple[str, str] or None): A tuple containing the title and message to display in an error messagebox
                                             if the input does not match the regular expression. Defaults to ("Error",
                                             "Try again!").
        showinfo (Tuple[str, str] or None): A tuple containing the title and message to display in an info messagebox
                                            if specified.
        showwarning (Tuple[str, str] or None): A tuple containing the title and message to display in a warning
                                               messagebox if specified.
        icon (str or None): The path to an icon file to display in the window. Defaults to None.

    Returns:
        Optional[str]: The text entered by the user, or None if the user clicked the cancel button or the input did not
                       match the regular expression.
    """

    def get_input_and_close_window(event):
        """
        Retrieves user input from a tkinter input box and closes the window.
        Validates the input against a regular expression pattern. If the input matches the pattern,
        the tkinter root window is destroyed. If the input does not match the pattern, the user_input
        variable is set to None and error, info, or warning message boxes may be displayed.

        Args:
            event (Event): The event that triggered the function.

        Returns:
            None
        """
        nonlocal user_input
        user_input = input_box.get("1.0", "end-1c")
        pattern = re.compile(regexcheck)
        if pattern.match(user_input):
            root.destroy()
        else:
            user_input = None
            if showerror:
                messagebox.showerror(*showerror)
            if showinfo:
                messagebox.showinfo(*showinfo)
            if showwarning:
                messagebox.showwarning(*showwarning)

    user_input = None
    root = tk.Tk()
    if icon:
        root.iconbitmap(os.path.normpath(icon))
    root.geometry(size)
    root.title(title)
    instructions_label = tk.Label(root, text=textabovebox)
    instructions_label.pack(pady=5)
    input_box = tk.Text(root, height=linesinputbox)
    input_box.pack(padx=10, pady=5)
    submit_button = tk.Button(
        root, text=submitbutton, command=lambda: get_input_and_close_window(event=None)
    )
    submit_button.pack(pady=5)
    root.mainloop()
    return user_input


def get_user_input_checkbox(
    checkbox_options: tuple = ("Option 1", "Option 2", "Option 3", "Option 4"),
    size: str = "300x350",
    title: str = "Your input",
    textabovebox: str = "Enter your text below:",
    submitbutton: str = "Submit",
        icon=None,
):
    user_input = []
    root = tk.Tk()
    if icon:
        root.iconbitmap(os.path.normpath(icon))
    root.geometry(size)
    root.title(title)

    # Define the checkbox options

    # Create a label for the checkboxes
    checkbox_label = tk.Label(root, text=textabovebox)
    checkbox_label.pack(pady=5)

    # Create the checkboxes
    checkboxes = []
    for option in checkbox_options:
        checkbox_var = tk.IntVar()
        checkbox = tk.Checkbutton(root, text=str(option), variable=checkbox_var)
        checkbox.pack()
        checkboxes.append((option, checkbox_var))

    # Function to get the user input when the user presses the Enter key
    def get_input_and_close_window():
        nonlocal user_input
        for option, checkbox_var in checkboxes:
            if checkbox_var.get() == 1:
                user_input.append(option)
        root.destroy()

    # Create the submit button
    submit_button = tk.Button(
        root, text=submitbutton, command=get_input_and_close_window
    )
    submit_button.pack(pady=5)

    # Start the main event loop
    root.mainloop()

    # Return the user input
    return user_input


def get_user_input_radio(
    radio_options: tuple = ("Option 1", "Option 2", "Option 3", "Option 4"),
    indexdefault: int = 0,
    size: str = "300x350",
    title: str = "Your input",
    textabovebox: str = "Enter your text below:",
    submitbutton: str = "Submit",
icon=None,
):
    user_input = None
    root = tk.Tk()
    if icon:
        root.iconbitmap(os.path.normpath(icon))
    root.geometry(size)
    root.title(title)

    # Define the radio button options
    radio_button_options = radio_options

    # Create a label for the radio buttons
    radio_button_label = tk.Label(root, text=textabovebox)
    radio_button_label.pack(pady=5)

    # Create the radio buttons
    radio_button_var = tk.StringVar(value=radio_button_options[indexdefault])
    for option in radio_button_options:
        radio_button = tk.Radiobutton(
            root, text=option, variable=radio_button_var, value=option
        )
        radio_button.pack()

    def get_input_and_close_window():
        nonlocal user_input
        user_input = radio_button_var.get()
        root.destroy()

    # Create the submit button
    submit_button = tk.Button(
        root, text=submitbutton, command=get_input_and_close_window
    )
    submit_button.pack(pady=5)

    # Start the main event loop
    root.mainloop()

    # Return the user input
    return user_input


def get_user_input_varbuttons(
    options: tuple = ("Option 1", "Option 2", "Option 3", "Option 4"),
    size: str = "300x350",
    title: str = "Your input",
    textabovebox: str = "Enter your text below:",
    buttonwidth: int = 15,
    buttonheight: int = 3,
        icon=None,
):
    user_input = None

    def select_option(option):
        nonlocal user_input
        user_input = option
        root.destroy()

    root = tk.Tk()
    if icon:
        root.iconbitmap(os.path.normpath(icon))
    root.geometry(size)
    root.title(title)

    instructions_label = tk.Label(root, text=textabovebox)
    instructions_label.pack(pady=5)

    for option in options:
        button = tk.Button(
            root,
            text=str(option),
            width=buttonwidth,
            height=buttonheight,
            command=lambda optionxx=option: select_option(optionxx),
        )
        button.pack(padx=5, pady=5)

    root.mainloop()

    return user_input


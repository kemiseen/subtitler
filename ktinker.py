import threading
import tkinter as tk
from tkinter import ttk
from functions import perform_translation

class Video_dict:
    def __init__(self):
        self.number = 0 
        self.url_dict = {}

    def on_Translate_click(self, label):
        # Update the label to inform the user to wait
        if self.url_dict == {}:
            label.config(text="You need to at least enter one URL")
            return
        label.config(text="Wait for the translation please...")

        # Start the translation process in a separate thread
        threading.Thread(target=perform_translation, args=(self.url_dict, label)).start()

    def on_Add_click(self, user_url, target_lang, label, text_input):
        if text_input.get() == "":
            print("You did not enter a URL")
        else:
            self.url_dict.update({user_url : target_lang})
            self.number = self.number + 1
            label.config(text=f"The number of URL you've entered: {self.number}")
            text_input.delete(0,100)

# Create the main application window
root = tk.Tk()
root.title("Subtitler")
#create Videodict obj
video_dict = Video_dict()

# Create a text input field
text_input = ttk.Entry(root, width=30)
text_input.grid(row=0, column=1, padx=10, pady=10)

# Create a dropdown menu
dropdown_var = tk.StringVar()
dropdown_var.set("en")  # Set default value
dropdown_menu = ttk.OptionMenu(root, dropdown_var, "en", "en", "fr", "de", "es")
dropdown_menu.grid(row=1, column=1, padx=10, pady=10)

# Create a status label to show translation status
status_label = ttk.Label(root, text="")
status_label.grid(row=3, column=0, padx=10, pady=10)

# Create a button
button = ttk.Button(root, text="Translate", command=lambda: video_dict.on_Translate_click(status_label))
button.grid(row=3, column=1, padx=10, pady=10)

button = ttk.Button(root, text="Add", command=lambda: video_dict.on_Add_click(text_input.get(), dropdown_var.get(), label3, text_input))
button.grid(row=2, column=1, padx=10, pady=10)

# Create labels for better UI
label1 = ttk.Label(root, text="Enter URL:")
label1.grid(row=0, column=0, padx=10, pady=10)

label2 = ttk.Label(root, text="Choose Language:")
label2.grid(row=1, column=0, padx=10, pady=10)

label3 = ttk.Label(root, text="The number of URL you've entered: 0")
label3.grid(row=2, column=0, padx=10, pady=10)

# Run the application
root.mainloop()

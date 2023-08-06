import tkinter as tk
from tkinter import ttk
import openai
import urllib.request
from PIL import Image as Ig
from PIL import ImageTk
from tkinter import *
import customtkinter
import os

class ChatBot:
    def __init__(self, api_key):
        openai.api_key = api_key

        self.home = customtkinter.CTk()
        self.home.title("Create Bot")
        self.home.geometry("400x300")

        self.name_entry = customtkinter.CTkEntry(self.home, placeholder_text="Bot Name", width=300, height=30)
        self.name_entry.place(x=50, y=50)

        self.objective_entry = customtkinter.CTkEntry(self.home, placeholder_text="Define Use", width=300, height=40)
        self.objective_entry.place(x=50, y=100)

        self.open_root_button = customtkinter.CTkButton(self.home, text="Let's GO", command=self.show_root, corner_radius=0)
        self.open_root_button.place(x=200, y=170)

        self.root = customtkinter.CTk()
        self.root.geometry("640x540")
        self.root.withdraw()

        self.code_text = customtkinter.CTkTextbox(self.root, height=150, width=640)
        self.code_text.pack(padx=10, pady=10)

        self.code_text.insert("1.0", "Write your Query here")

        self.code_button = customtkinter.CTkButton(self.root, text="Submit", command=lambda: [self.correct_code(), self.clear_text()])
        self.code_button.pack()

        self.code_conversation = customtkinter.CTkTextbox(self.root, height=320, width=640)
        self.code_conversation.pack(padx=10, pady=10)

        self.code_conversation.tag_config("red", foreground="pink")
        self.code_conversation.tag_config("green", foreground="yellow")

        self.home.mainloop()

    def show_root(self):
        self.root.deiconify()
        name = self.name_entry.get()
        self.root.title(name)

    def correct_code(self):
        code = self.code_text.get("1.0", "end")
        objective = self.objective_entry.get()

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=objective + "\n" + code,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        corrected_code = response["choices"][0]["text"]

        self.code_conversation.delete("1.0", "end")
        self.code_conversation.insert("1.0", "User: " + code, "red")
        self.code_conversation.insert("end", "Chatbot: " + corrected_code, "green")

    def clear_text(self):
        self.code_text.delete("1.0", END)




        
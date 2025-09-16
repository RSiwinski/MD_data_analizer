import customtkinter as ctk

def quick_popup(display_text):
    popup = ctk.CTkToplevel()
    popup.title("Error")
    popup.attributes('-topmost', True)
    popup.resizable(False, False)
    label = ctk.CTkLabel(popup, text=display_text, font=("Arial", 14),width=200)
    label.pack(padx=20, pady=20)
    close_button = ctk.CTkButton(popup, text="OK", command=popup.destroy)
    close_button.pack(pady=10)
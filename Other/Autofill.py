import customtkinter as ctk



class AutoFillBox:
    def __init__(self, dictionary,origin,mode):

        title = ""
        if mode == 1:
            title = "Atom identifier"
        else:
            title = "Residue name"
        self.frame = ctk.CTkFrame(master=origin,fg_color="transparent")    
        self.dict = dictionary
        self.label = ctk.CTkLabel(master=self.frame,text=title)
        self.label.pack(side="left",pady=5)
        self.entry_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(master = self.frame, textvariable=self.entry_var, width=250)
        
        self.entry.bind("<KeyRelease>", self.on_key_release)

        self.suggestion = ctk.CTkButton(self.frame, text="No match", command=self.on_select)
        self.suggestion.pack(side="right",padx=(10,0),pady=5)
        self.entry.pack(side="right",padx=(26,0),pady=5)
        

    def on_key_release(self, event):
        typed = self.entry_var.get().strip()
        if typed == "":
            self.suggestion.configure(text="No match")
            return

        suggestions = [word for word in self.dict if word.startswith(typed.upper())]
        if suggestions:
            suggestions.sort(key=lambda w: (len(w),w))
            self.suggestion.configure(text=suggestions[0])
        else:
            self.suggestion.configure(text="No match")

    def on_select(self):
        choice = self.suggestion.cget("text")
        if choice != "No match":
            self.entry_var.set(choice)

    def Entry(self):
        return self.entry
    
    def suggest(self):
        return self.suggestion

    def create(self):
        return self.frame


import customtkinter as ctk
import Other.Elements as oe

def SearchForFile():
    filename=ctk.filedialog.askopenfilename(
        title="Select a file",
        filetypes=[
            ("Plik .pdb", ".pdb")
        ]
    )
    oe.wybierz_button.configure(fg_color="red")
    oe.filename_input.delete(0,ctk.END)
    oe.filename_input.insert(0,filename)
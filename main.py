from buildfg import buildfg
from buildbg import buildbg
import customtkinter as ctk
import Other.Elements as oe
import Other.Shared as ots
from Other.image_path import image_path
from PIL import Image




ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

oe.root = ctk.CTk()
oe.root.geometry("800x550")
oe.root.title("Program do analizy")
path = image_path("klepsydra_resized.png")
if path != "Empty":
    image = Image.open(path)
    tk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(200, 200))
buildfg(oe.root)
ots.Loading_frame = ctk.CTkFrame(master=oe.tabview.tab("DCD Analysis"),fg_color="transparent")
if path != "Empty":
    Loading_label = ctk.CTkLabel(master=ots.Loading_frame,image=tk_image,fg_color="transparent",text="")
else:
    Loading_label = ctk.CTkLabel(master=ots.Loading_frame,fg_color="transparent",text="Loading...",font=("Arial",35),text_color="black")
Loading_label.pack(expand=True,fill="both",padx=0,pady=0)
buildbg()



oe.root.minsize(850,650)
oe.root.mainloop()

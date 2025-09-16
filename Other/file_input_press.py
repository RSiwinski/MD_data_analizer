import Other.Shared as ost
import Other.Elements as oe


def file_input_press(event):

    read = oe.filename_input.get()
    if read == "":
        return
    elif ost.filename == read:
        oe.wybierz_button.configure(fg_color="green")
    else:
        oe.wybierz_button.configure(fg_color="red")
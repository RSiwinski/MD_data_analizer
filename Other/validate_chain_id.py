def validate_chain_id(entry_var,box,min_val, max_val, *args):
    try:
        val = int(entry_var.get())
        if val < min_val or val > max_val:
            box.configure(fg_color="red")
        else:
            box.configure(fg_color="#323738")
    except ValueError:
        box.configure(fg_color="#323738")   
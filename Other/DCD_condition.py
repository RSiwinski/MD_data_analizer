
def check_array(arr, Addargs, mode):
    allowed = {"energ", "btr"}

    if mode == "pdb":
        if len(arr) == 1 and arr[0] == "energ":
            if Addargs.get("energ") != [0, 0, 1, 0]:
                return True
    else:
        for item in arr:
            if item not in allowed:
                return True
        
        if "energ" in arr:
            if Addargs.get("energ") != [0, 0, 1, 0]:
                return True
    
    return False

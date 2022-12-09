def get_hp_key():
    with open("./.env") as a :
        lines = a.readlines()
        return lines[1]
def get_rak_key():
    with open("./.env") as a :
        lines = a.readlines()
        return lines[4]
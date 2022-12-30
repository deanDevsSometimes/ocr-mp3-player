
file = open("colours.txt", "r")
temp = file.readlines()
primary = temp[0].replace("\n", '')
secondary = temp[1].replace("\n", '')
file.close()


colours = {
    "primary": "#" + primary,
    "secondary": "#" + secondary
}

def is_colour_valid(colour):
    try:
        if colour[0] == "#":
            colour = colour[1:]

    except:
        pass

    if len(colour) != 6:
        return False

    for c in colour[1:]:
        if not c.isdigit() and not c.isalpha() or c.lower() > 'f':
            return False

    return True

def change_primary(colour):

    if is_colour_valid(colour):
        colours["primary"] = "#" + colour
        file = open("colours.txt", "w")
        file.write(colour + "\n" + colours["secondary"][1:])
        file.close()
        print("Changed Primary Colour")
        return

    print("Invalid Colour")


def change_secondary(colour):
    if is_colour_valid(colour):
        colours["secondary"] = "#" + colour
        file = open("colours.txt", "w")
        file.write(colours["primary"][1:] + "\n" + colour)
        print("Changed Secondary Colour")
        return

    print("Invalid Colour")


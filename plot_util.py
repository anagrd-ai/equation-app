

def hex_to_rgb(hex_color: str):
    # Remove the '#' if present
    hex_color = hex_color.lstrip('#')
    # Convert hex to decimal
    red = int(hex_color[:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:], 16)
    # Return the RGB string
    return f"rgb({red}, {green}, {blue})"

def create_colorscale(locolor: str, hicolor:str):
    return [[0, hex_to_rgb(locolor)], [1, hex_to_rgb(hicolor)]]

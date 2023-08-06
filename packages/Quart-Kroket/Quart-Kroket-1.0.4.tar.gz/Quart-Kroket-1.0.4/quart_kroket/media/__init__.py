def proportional_scale(width: int, height: int, max_width_or_height: int):
    if width > max_width_or_height:
        return int(max_width_or_height), int((height / width) * max_width_or_height)
    if height > max_width_or_height:
        return int((width / height) * max_width_or_height), int(max_width_or_height)
    return width, height
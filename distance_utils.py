def calculate_focal_length(known_distance, known_width, marker_width_in_pixels):
    """
    Calculate the camera's focal length using a known distance and object width.
    """
    return (marker_width_in_pixels * known_distance) / known_width

def calculate_distance(focal_length, known_width, marker_width_in_pixels):
    """
    Estimate the distance to an object using the focal length and the marker's width.
    """
    return (known_width * focal_length) / marker_width_in_pixels

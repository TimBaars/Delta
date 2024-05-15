def convert_to_tuples(x_coords, y_coords):
    """
    Convert separate x and y coordinate lists to a list of tuples.
    
    Args:
        x_coords: List of x coordinates.
        y_coords: List of y coordinates.

    Returns:
        List of (x, y) tuples representing path points.
    """
    return list(zip(x_coords, y_coords))

def convert_nodes_to_flat_list(nodes):
    """
    Convert a list of Node objects to a flat list of coordinates.

    Args:
        nodes (list): List of Node objects.

    Returns:
        list: A flat list containing (x, y) coordinates.
    """
    flat_list = []
    for node in nodes:
        for x, y in zip(node.parent_x, node.parent_y):
            flat_list.append(x)
            flat_list.append(y)
    return flat_list



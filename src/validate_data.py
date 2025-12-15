def validate_node(node_data):
    """
    validate: the id of one node exists and the progress_percentage for
      content in one node exists;
      return True/False
    """
    if (
        node_data["id"] is not None
        and node_data["content"]["progress_percentage"] is not None
    ):
        return True
    else:
        return False


def validate_edge(edge_data, nodes):
    """
    validate: the from and to for the edge must in note;
    return True/False
    """
    node_ids = {node["id"] for node in nodes}
    if edge_data["from"] in node_ids and edge_data["to"] in node_ids:
        return True
    else:
        return False

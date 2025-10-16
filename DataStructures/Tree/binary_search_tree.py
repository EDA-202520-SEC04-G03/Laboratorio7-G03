import DataStructures.Tree.bst_node as bst


def new_map():
    map = {"root":None}
    return map

def insert_node(root, key, value):
    if root is None:
        return bst.new_node(key, value)
    if key < root["left"]["key"]:
        root["left"] = insert_node(root["left"], key, value)
    elif key > root["right"]["key"]:
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value
    return root

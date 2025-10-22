import DataStructures.Tree.bst_node as bst
import DataStructures.List.single_linked_list as ll


def new_map():
    return {"root": None}

def insert_node(root, key, value):
    if root is None:
        return bst.new_node(key, value)

    if key < root["key"]:
        root["left"] = insert_node(root["left"], key, value)
    elif key > root["key"]:
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value
    return root

def put(my_bst, key, value):
    my_bst["root"] = insert_node(my_bst["root"], key, value)
    return my_bst

def get_node(root, key):
    if root is None:
        return None
    if key < root["key"]:
        return get_node(root["left"], key)
    elif key > root["key"]:
        return get_node(root["right"], key)
    else:
        return root

def get(my_bst, key):
    node = get_node(my_bst["root"], key)
    return None if node is None else node["value"]

def size_tree(root):
    if root is None:
        return 0
    return 1 + size_tree(root["left"]) + size_tree(root["right"])

def size(my_bst):
    return size_tree(my_bst["root"])

def is_empty(my_bst):
    return my_bst["root"] is None   

def contains(my_bst, key):
    return get_node(my_bst["root"], key) is not None

def get_min_node(my_bst):
    current = my_bst["root"]
    if current is None:
        return None
    while current["left"] is not None:
        current = current["left"]
    return current


def get_min(my_bst):
    node = get_min_node(my_bst)
    return None if node is None else node["key"]


def get_max_node(my_bst):
    current = my_bst["root"]
    if current is None:
        return None
    while current["right"] is not None:
        current = current["right"]
    return current


def get_max(my_bst):
    node = get_max_node(my_bst)
    return None if node is None else node["key"]


def height_tree(root):
    if root is None:
        return -1
    left_height = height_tree(root["left"])
    right_height = height_tree(root["right"])
    return 1 + (left_height if left_height > right_height else right_height)


def height(my_bst):
    return height_tree(my_bst["root"])

def delete_min_tree(root):
    if root is None:
        return None
    if root["left"] is None:
        return root["right"]
    root["left"] = delete_min_tree(root["left"])
    return root


def delete_min(my_bst):
    my_bst["root"] = delete_min_tree(my_bst["root"])
    return my_bst


def delete_max_tree(root):
    if root is None:
        return None
    if root["right"] is None:
        return root["left"]
    root["right"] = delete_max_tree(root["right"])
    return root


def delete_max(my_bst):
    my_bst["root"] = delete_max_tree(my_bst["root"])
    return my_bst

def key_set_tree(root, key_list):
    
    if root is not None:
        
        key_set_tree(root["left"], key_list)
         
        ll.add_last(key_list, root["key"])

        key_set_tree(root["right"], key_list)

def key_set(my_bst):
    
    key_list = ll.new_list()

    root = my_bst["root"]
    
    key_set_tree(root, key_list)
    
    return key_list


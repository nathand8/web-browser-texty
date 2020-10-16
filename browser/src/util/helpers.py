def tree_to_string(tree, indent=""):
    print(indent, tree)
    if isinstance(tree, ElementNode):
        for node in tree.children:
            tree_to_string(node, indent + "  ")
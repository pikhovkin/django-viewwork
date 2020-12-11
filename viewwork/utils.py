def build_nested_tree(
        raw_items,
        parent_name='parent_id',
        children_name='items',
        id_name='id',
        parent_null=None
):
    parent_null = parent_null or 0
    nodes = {item[id_name]: item for item in raw_items}
    nested_tree = []
    for item in raw_items:
        parent_id = item[parent_name] or parent_null
        node = nodes[item[id_name]]
        if parent_id == parent_null:
            nested_tree.append(node)
        else:
            parent = nodes[parent_id]
            if not children_name in parent:
                parent[children_name] = []
            parent[children_name].append(node)
    return nested_tree

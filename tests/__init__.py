def menu_id_list(nested_nodes):
    nodes = nested_nodes[:]
    ids = set()
    while nodes:
        node = nodes.pop()
        ids.add(node['id'])
        if node.get('items', []):
            nodes.extend(node['items'])
    return ids

from . import settings


def empty_items(raw_items, nodes, parent_name='parent_id', id_name='id'):
    empty_parents = {item[id_name] for item in raw_items if not item['view']}
    parents = {item[parent_name] for item in raw_items if item['view'] and item[parent_name]}
    for p in parents:
        while p is not None:
            empty_parents -= {p}
            p = nodes[p].get(parent_name)
    return empty_parents


def build_nested_tree(
        raw_items,
        parent_name='parent_id',
        children_name='items',
        id_name='id',
        parent_null=None
):
    REMOVE_EMPTY_ITEM = getattr(settings, 'REMOVE_EMPTY_ITEM', True)
    nodes = {item[id_name]: item for item in raw_items}
    remove_parents = empty_items(raw_items, nodes, parent_name=parent_name, id_name=id_name) if REMOVE_EMPTY_ITEM else {}
    nested_tree = []
    parent_null = parent_null or 0
    for item in raw_items:
        if item[id_name] in remove_parents:
            continue
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

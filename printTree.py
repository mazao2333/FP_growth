from print_tree import print_tree

class printFPtree(print_tree):
    def get_children(self, node):
        return node.children
    def get_node_str(self, node):
        return str(node.name)+'('+str(node.value)+')'
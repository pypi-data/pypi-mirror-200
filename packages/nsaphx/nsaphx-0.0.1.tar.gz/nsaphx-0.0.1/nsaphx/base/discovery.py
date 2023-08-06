
class Node:

    def __init__(self, val):
        self.val = val
        self.adjlist = []

    def add_node(self, node):
        self.adjlist.append(node)

    def __str__(self):
        return str(self.val)
    
class Graph:

    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def add_connection(self, node_a, node_b):
        # check if node_a and node_b are Node type
        if not isinstance(node_a, Node):
            raise TypeError("node_a is not a Node type")
        if not isinstance(node_b, Node):
            raise TypeError("node_b is not a Node type")
        
        if node_a not in self.nodes:
            self.nodes.append(node_a)

        if node_b not in self.nodes:
            self.nodes.append(node_b)

        node_a.add_node(node_b)


    def dfs(self, start_node = None):
        
        if start_node is None:
            start_node = self.nodes[0]
        
        if start_node not in self.nodes:
            return
        
        
        stack = []
        visited = []
        stack.append(start_node)
        visited.append(start_node)

        while stack: 
            if stack[-1].adjlist:
                val = stack[-1].adjlist.pop()
                if val in visited:
                    continue
                stack.append(val)
                visited.append(val)
            else:
                stack.pop() 
        return visited
    
    def print_graph(self):
        if not self.nodes:
            print("Graph is empty")
            return
        root = self.nodes[0]
        print_graph(root)

def print_graph(node, is_root=True, prefix='', is_last=True):
    # Print the current node
    if not is_root:
        print(prefix, end='')
        if is_last:
            print('└─', end='')
        else:
            print('├─', end='')
    print(node)

    # Recursively print the adjacent nodes
    for i, adj_node in enumerate(node.adjlist):
        is_last = i == len(node.adjlist) - 1
        print_graph(adj_node, is_root=False,
                    prefix=prefix + ('   ' if is_last else '│  '),
                    is_last=is_last)



if __name__ == '__main__':
    import networkx as nx
    import matplotlib.pyplot as plt
    graph = Graph()
    node_a = Node("A", type="t1")
    node_b = Node("B", type="t1")
    node_c = Node("C", type="t1")
    node_d = Node("D", type="t2")
    node_e = Node("E", type="t2")
    node_f = Node("F", type="t2")
    node_g = Node("G", type="t2")


    graph.add_connection(node_a, node_b)
    graph.add_connection(node_b, node_c)
    graph.add_connection(node_c, node_d)
    graph.add_connection(node_d, node_e)
    graph.add_connection(node_b, node_f)
    graph.add_connection(node_a, node_g)
    # visited = graph.dfs(node_a)
    # for item in visited:
    #     print(item)

    print_graph(node_a)


    # G = nx.Graph()

    # G.add_node(node_a)
    # G.add_node(node_b)
    # G.add_node(node_c)
    # G.add_node(node_d)
    # G.add_node(node_e)
    # G.add_node(node_f)
    # G.add_node(node_g)

    # G.add_edge(node_a, node_b)
    # G.add_edge(node_b, node_c)
    # G.add_edge(node_c, node_d)
    # G.add_edge(node_d, node_e)
    # G.add_edge(node_b, node_f)
    # G.add_edge(node_a, node_g)

    # pos = {node_a: (-1, 0), node_b: (0, 0.5), node_c: (0, -0.5), node_d: (1, 0.0),
    #        node_e: (2, 0), node_f: (1, 1.5), node_g: (0, -1.5)}

    # node_colors = []
    # for node in G.nodes:
    #     if node.type == "t1":
    #         node_colors.append("skyblue")
    #     elif node.type == "t2":
    #         node_colors.append("yellow")
    #     else:
    #         node_colors.append("gray")

    # def custom_draw(G, pos=None, ax=None, **kwargs):
    #     if pos is None:
    #         pos = nx.spring_layout(G)
    #     if ax is None:
    #         cf = plt.gcf()
    #         ax = cf.gca()
    #     nx.draw_networkx(G, pos=pos, ax=ax, **kwargs)
    #     # ax.set_axis_off()
    #     # return ax

    # custom_draw(G, pos=pos, with_labels=True, font_weight="bold", node_color=node_colors)
    # plt.show()


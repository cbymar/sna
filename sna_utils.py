import heapq
import operator



#### Build a tree
class Node(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def insert_left(self, child):
        if self.left is None:
            self.left = child
        else:
            child.left = self.left
            self.left = child

    def insert_right(self, child):
        if self.right is None:
            self.right = child
        else:
            child.right = self.right
            self.right = child


root = Node("alpha")
root.val
root.left

root.insert_left(Node("beta"))
root.left
root.left.val

root.insert_right(Node("gamma"))
root.right.val

#### Build a parse tree
# from https://bradfieldcs.com/algos/trees/parse-trees/
OPERATORS = dict(zip(["+","-","*","/"],
                     [operator.add, operator.sub, operator.mul, operator.truediv])
                 )
LEFT_PAREN = "("
RIGHT_PAREN = ")"

def build_parse_tree(expression):
    """
    Reads an expression left to right, maps it to nested structure
    number: current node gets number's value, move to parent
    operator: current node (which is a parent by definition) gets operator's value
    leftparen = current node creates child, move to child
    rightparen = current node is a parent of complete expression, go to its parent
    """
    tree = {}
    stack = [tree]  # push each new parent to the stack as kids become parents
    node = tree

    for token in expression:
        if token == LEFT_PAREN:
            node["left"] = {}
            stack.append(node)
            node = node["left"]  # move to this child node
        elif token == RIGHT_PAREN:
            node = stack.pop()  # move to the parent node; kept track of in the stack
        elif token in OPERATORS:
            node["val"] = token
            node["right"] = {}  # a new subtree (or leaf)
            stack.append(node)  # this node's a parent, because as an operator, it has operands (kids)
            node = node["right"]  # find out what's being operated on
        else:
            node["val"] = int(token)
            parent = stack.pop()  # we want to go to parent
            node = parent  # go to parent
    return tree


build_parse_tree("((3*4)+(5*6))")
build_parse_tree("(2*((3*4)+(5*6)))")


def evaluate(tree):
    """
    recursively apply the unary operators to the two kids
    The root node is defined as being an operator
    """
    try:
        operate = OPERATORS[tree["val"]]
        return operate(evaluate(tree["left"]), evaluate(tree["right"]))
    except KeyError:
        return tree["val"]  # this is the case where the node value is a leaf

evaluate(build_parse_tree("(2*((3*4)+(5*6)))"))  # entire expression must be in parentheses
evaluate(build_parse_tree("((3*4)+(5*6))"))

#### Priority queue with binary heap
# Complete binary tree has all nodes except at most distal level
# If complete, parent node of a node at list position n is always at position floor(n/2)


class BinaryHeap(object):
    def __init__(self):
        self.items = [0]

    def __len__(self):
        return len(self.items) - 1

    def min_child(self, i):
        """
        returns list index position of smaller child node for a parent
        either left by default, left by comparison, or right
        """
        if i * 2 + 1 > len(self):
            return i * 2
        if self.items[i * 2] < self.items[i * 2 + 1]:
            return i * 2
        return i * 2 + 1

    def percolate_up(self):
        """Apply this after appending to end of list representation"""
        i = len(self)  #
        while i // 2 > 0:
            if self.items[i] < self.items[i//2]:
                self.items[i], self.items[i // 2] = self.items[i//2], self.items[i]
            i = i // 2

    def percolate_down(self, i):
        """Apply this after unshifting min node and swapping terminal node with root"""
        while i * 2 <= len(self):
            mc = self.min_child(i)
            if self.items[mc] < self.items[i]:
                self.items[mc], self.items[i] = self.items[i], self.items[mc]
            i = mc

    def insert(self, k):
        self.items.append(k)
        self.percolate_up()

    def delete_min(self):
        """unshifts the root node, replaces with distal node """
        return_value = self.items[1]  # 0th item is dummy
        self.items[1] = self.items[len(self)].pop()  # we can do this in one step
        self.percolate_down(1)
        return return_value

    def build_heap(self, alist):
        """Builds heap from list in O(n) worst case"""
        i = len(alist) // 2
        self.items = [0] + alist
        while i > 0:
            self.percolate_down(i)
            i -= 1

#### Dijkstra

def calculate_distances(graph, startv):

    distances = {vertex: float("infinity") for vertex in graph}
    distances[startv] = 0

    pq = [(0, startv)]
    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight   # each neighbor gets its last mile added to current distance

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances

example_graph = {
    'U': {'V': 2, 'W': 5, 'X': 1},
    'V': {'U': 2, 'X': 2, 'W': 3},
    'W': {'V': 3, 'U': 5, 'X': 3, 'Y': 1, 'Z': 5},
    'X': {'U': 1, 'V': 2, 'W': 3, 'Y': 1},
    'Y': {'X': 1, 'W': 1, 'Z': 1},
    'Z': {'W': 5, 'Y': 1},
}





def get_graph(train, str_from="FROM", str_to="TO", directed=False):
    """
    Graph object from data frame
    """
    pass
    # G = nx.DiGraph() if directed==True else nx.Graph()
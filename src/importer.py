import os
from typing import List, Optional

from node import Node, euclidean_distance


class Importer:
    def __init__(self, file_path: str) -> None:
        """
        Initializes the Importer object.

        :param file_path: The path to the input file.
        """
        self.file_path = file_path
        self.data = self.read_input_file()
        self.Tmax, self.P, self.node_data = self.read_nodes()

    def read_input_file(self) -> List[str]:
        """
        Reads the input file and returns its content as a list of lines.

        :return: A list of lines in the input file.
        """
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
            print(f"Instance read: {os.path.basename(self.file_path)}")
            return lines
        except FileNotFoundError:
            print("File not found.")
            return []

    def read_nodes(self) -> tuple[float, int, List[Node]]:
        """
        Parses the input data and extracts information about nodes.

        :return: A tuple containing Tmax (float), P (int), and a list of Node objects.
        """
        print("Reading nodes:")
        node_data: List[Node] = []
        # Extract Tmax and P from the first line
        first_line_data = self.data[0].strip().split()
        Tmax: float = float(first_line_data[0])
        P: int = int(first_line_data[1])
        if P != 1:
            print("This is not an OP instance")
            return Tmax, P, node_data

        # Extract the first
        x, y, score = map(float, self.data[1].strip().split())
        instance = Node(0, x, y, score, isFirst=True)
        node_data.append(instance)
        
        # Extract last node
        N = len(self.data) - 2
        x, y, score = map(float, self.data[2].strip().split())
        instance = Node(N, x, y, score, isLast=True)
        node_data.append(instance)

        # Extract data for each node starting from the fourth line
        for i, line in enumerate(self.data[3:]):
            x, y, score = map(float, line.strip().split())
            instance = Node(i+1, x, y, score)
            node_data.append(instance)

        # Sort by node id
        node_data.sort(key=lambda x: x.id)

        return Tmax, P, node_data

    def print_nodes(self) -> None:
        """
        Prints the nodes and their scores.
        """
        for node in self.node_data:
            if node.isFirst:
                print("First node -> ", end=" ")
            elif node.isLast:
                print("Last node: -> ", end=" ")
            print(f"Node {node.id} (x={node.x}, y={node.y}), Score: {node.score}")


if __name__ == "__main__":
    # file_path = "input/ref/set_64_1/set_64_1_15.txt"
    file_path = "input/ref/Tsiligirides 3/tsiligirides_problem_3_budget_070.txt"
    # file_path = "input/ref/set_64_1/set_64_1_15_err_test.txt"
    importer = Importer(file_path)
    importer.print_nodes()

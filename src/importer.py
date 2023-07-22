import os
import math
from typing import List, Optional

class Node:
    def __init__(self, x: float, y: float, score: float, isFirst: bool = False, isLast: bool = False):
        """
        Represents a node with coordinates (x, y) and a score.

        :param x: X-coordinate of the node.
        :param y: Y-coordinate of the node.
        :param score: The score associated with the node.
        :param isFirst: True if the node is the first node in the sequence (optional, default is False).
        :param isLast: True if the node is the last node in the sequence (optional, default is False).
        """
        self.x = x
        self.y = y
        self.score = score
        self.isFirst = isFirst
        self.isLast = isLast

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

        # Extract the first and last node
        x, y, score = map(float, self.data[1].strip().split())
        instance = Node(x, y, score, isFirst=True)
        node_data.append(instance)
        x, y, score = map(float, self.data[2].strip().split())
        instance = Node(x, y, score, isLast=True)
        node_data.append(instance)

        # Extract data for each node starting from the fourth line
        for line in self.data[3:]:
            x, y, score = map(float, line.strip().split())
            instance = Node(x, y, score)
            node_data.append(instance)

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
            print(f"Node (x={node.x}, y={node.y}), Score: {node.score}")


if __name__ == "__main__":
    file_path = "input/ref/set_64_1/set_64_1_15.txt"
    # file_path = "input/ref/Tsiligirides 3/tsiligirides_problem_3_budget_070.txt"
    # file_path = "input/ref/set_64_1/set_64_1_15_err_test.txt"
    importer = Importer(file_path)
    importer.print_nodes()

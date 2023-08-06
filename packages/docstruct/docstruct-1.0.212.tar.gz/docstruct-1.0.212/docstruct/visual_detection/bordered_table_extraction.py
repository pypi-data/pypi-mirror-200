from typing import Optional
from .constants import HEIGHT_SCALE, WIDTH_SCALE
from ..graph import Node, BipartiteGraph
from .vis_line import Orientation, VisLine
from ..text_block import Cell, Table
from ..bounding_box import BoundingBox

# TODO make the cell more robust by recognizing potential cells


class BorderedTableExtractor:
    def __init__(
        self,
        hor_lines: list[VisLine],
        ver_lines: list[VisLine],
        hor_threshold: float,
        ver_threshold: float,
    ):
        self.hor_lines = sorted(hor_lines, key=lambda line: line.axis)
        self.ver_lines = sorted(ver_lines, key=lambda line: line.axis)
        self.hor_threshold = hor_threshold
        self.ver_threshold = ver_threshold
        self.map_line_id_to_order = self.get_map_line_id_to_order()

    def get_map_line_id_to_order(self) -> dict:
        map_line_id_to_order = {}
        for order, line in enumerate(self.hor_lines):
            map_line_id_to_order[line.id] = order
        for order, line in enumerate(self.ver_lines):
            map_line_id_to_order[line.id] = order
        return map_line_id_to_order

    def get_common_node_with_minimal_order(
        self, first_nodes: list[Node], second_nodes: list[Node], bottom_node: Node
    ) -> Optional[Node]:
        """
        Get the minimal common node between two lists of nodes s.t. the node index is bigger than threshold.
        The function assumes the lists are sorted by node index.
        """
        first_nodes = [
            node
            for node in first_nodes
            if self.map_line_id_to_order[node.data.id]
            > self.map_line_id_to_order[bottom_node.data.id]
        ]
        second_nodes = [
            node
            for node in second_nodes
            if self.map_line_id_to_order[node.data.id]
            > self.map_line_id_to_order[bottom_node.data.id]
        ]
        i = 0
        j = 0
        while i < len(first_nodes) and j < len(second_nodes):
            if first_nodes[i].data.id == second_nodes[j].data.id:
                return first_nodes[i]
            elif (
                self.map_line_id_to_order[first_nodes[i].data.id]
                < self.map_line_id_to_order[second_nodes[j].data.id]
            ):
                i += 1
            else:
                j += 1
        return None

    def get_graph(self):
        hor_nodes = []
        ver_nodes = []

        for hor_line in self.hor_lines:
            hor_nodes.append(Node(hor_line))

        for ver_line in self.ver_lines:
            ver_nodes.append(Node(ver_line))

        map_line_id_to_node = {}
        for node in hor_nodes:
            map_line_id_to_node[node.data.id] = node
        for node in ver_nodes:
            map_line_id_to_node[node.data.id] = node

        for hor_line in self.hor_lines:
            for ver_line in self.ver_lines:
                if self.are_adjacent_lines(hor_line, ver_line):
                    hor_node = map_line_id_to_node[hor_line.id]
                    ver_node = map_line_id_to_node[ver_line.id]
                    hor_node.add_neighbor(ver_node)
                    ver_node.add_neighbor(hor_node)

        bipartite_graph = BipartiteGraph(left_nodes=hor_nodes, right_nodes=ver_nodes)
        dummy_nodes = bipartite_graph.get_nodes_with_bounded_degree(
            min_degree=0, max_degree=1
        )
        for dummy_node in dummy_nodes:
            bipartite_graph.remove_node(dummy_node)
        return bipartite_graph

    def are_adjacent_lines(
        self,
        first_line: VisLine,
        second_line: VisLine,
    ):
        first_bb = first_line.convert_to_bb(
            height_scale=HEIGHT_SCALE,
            width_scale=WIDTH_SCALE,
            length_threshold=self.hor_threshold,
        )
        second_bb = second_line.convert_to_bb(
            height_scale=HEIGHT_SCALE,
            width_scale=WIDTH_SCALE,
            length_threshold=self.ver_threshold,
        )
        return first_bb.intersect(second_bb)

    def get_bounding_box(
        self, left: VisLine, right: VisLine, top: VisLine, bottom: VisLine
    ):
        return BoundingBox(
            left=left.axis, right=right.axis, top=top.axis, bottom=bottom.axis
        )

    def get_cells(self, hor_nodes: list[Node]):

        cells = []
        for bottom in hor_nodes:
            for j, left in enumerate(bottom.neighbors):
                # (bottom, left) is the bottom left corner of potential cell
                # we are looking for the top right corner = (top, right)
                # then we have a cycle (bottom -> left -> top -> right -> bottom)

                for k in range(j + 1, len(bottom.neighbors)):
                    right = bottom.neighbors[k]

                    # we want to find the lowest node s.t. is bigger than bottom order, in left.neighbors and right.neighbors
                    first_potentials_hor = left.neighbors
                    second_potentials_hor = right.neighbors
                    top = self.get_common_node_with_minimal_order(
                        first_potentials_hor,
                        second_potentials_hor,
                        bottom_node=bottom,
                    )
                    if top is None:
                        continue
                    bbox = self.get_bounding_box(
                        left.data, right.data, top.data, bottom.data
                    )
                    cell = Cell(bounding_box=bbox)
                    cells.append(cell)
                    break
        return cells

    def get_map_line_id_to_cc_order(self, ccs: list[list[Node]]) -> dict:
        map_line_id_to_cc = {}
        for i, cc in enumerate(ccs):
            for node in cc:
                map_line_id_to_cc[node.data.id] = i
        return map_line_id_to_cc

    def group_cells_to_tables(
        self, cells: list[Cell], map_line_id_to_cc: dict
    ) -> list[Table]:
        tables_cells = {}
        for cell in cells:
            cc = map_line_id_to_cc[cell.left.id]
            if cc not in tables_cells:
                tables_cells[cc] = []
            tables_cells[cc].append(cell)
        tables = []
        for table in tables_cells.values():
            tables.append(Table(cells=table))
        return tables

    def main(self) -> list[Table]:
        bipartite_graph = self.get_graph()
        ccs = bipartite_graph.get_connected_components()
        tables = []
        for cc in ccs:
            hor_nodes = [
                node for node in cc if node.data.orientation == Orientation.HORIZONTAL
            ]
            cells = self.get_cells(hor_nodes)
            if cells:
                table = Table(cells=cells)
                tables.append(table)
        return tables

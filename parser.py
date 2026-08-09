import ast


class VariableTracker(ast.NodeVisitor):

    def visit_Assign(self, node):
        for target in node.targets:

            if isinstance(target, ast.Name):
                print(
                    f"Variable found: "
                    f"{target.id} "
                    f"(line {node.lineno})"
                )

        self.generic_visit(node)


def parse_file(filename):

    with open(filename, "r", encoding="utf-8") as file:
        code = file.read()

    tree = ast.parse(code)

    tracker = VariableTracker()
    tracker.visit(tree)

    return code
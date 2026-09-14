from __future__ import annotations

import argparse
import ast
from pathlib import Path

PASS_MARKER = "NATIVE_RESPONSE_GATE_PASS"


def _is_next_data_true_assignment(node: ast.AST) -> bool:
    if isinstance(node, ast.Assign):
        if not (isinstance(node.value, ast.Constant) and node.value.value is True):
            return False
        return any(isinstance(target, ast.Name) and target.id == "next_data" for target in node.targets)
    if isinstance(node, ast.AnnAssign):
        return (
            isinstance(node.target, ast.Name)
            and node.target.id == "next_data"
            and isinstance(node.value, ast.Constant)
            and node.value.value is True
        )
    return False


def _is_response_loop_test(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, ast.Not)
        and isinstance(node.operand, ast.Name)
        and node.operand.id == "next_data"
    )


def _contains_is_pressed_in(node: ast.AST) -> bool:
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        func = child.func
        if isinstance(func, ast.Attribute) and func.attr == "isPressedIn":
            return True
    return False


def validate(main_py: Path) -> None:
    if not main_py.is_file():
        raise RuntimeError(f"Missing upstream main.py: {main_py}")

    source = main_py.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(main_py))
    parent: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent[child] = node

    main_fn = next(
        (node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "main"),
        None,
    )
    if main_fn is None:
        raise RuntimeError("Upstream main.py does not define main()")

    loops = [
        node
        for node in ast.walk(main_fn)
        if isinstance(node, ast.While) and _is_response_loop_test(node.test)
    ]
    if len(loops) != 1:
        raise RuntimeError(f"Expected exactly one 'while not next_data' response loop, found {len(loops)}")

    loop = loops[0]
    transitions = [node for node in ast.walk(loop) if _is_next_data_true_assignment(node)]
    if not transitions:
        raise RuntimeError("Response loop never assigns next_data=True")

    for transition in transitions:
        cursor = transition
        protected_by_response = False
        while cursor is not loop:
            cursor = parent.get(cursor)
            if cursor is None:
                break
            if isinstance(cursor, ast.If) and _contains_is_pressed_in(cursor.test):
                protected_by_response = True
                break
        if not protected_by_response:
            raise RuntimeError("Found next_data=True outside a mouse response-button condition")

    # A bare break would allow a future timer or unrelated condition to end the
    # stimulus even without setting next_data from a response button.
    if any(isinstance(node, ast.Break) for node in ast.walk(loop)):
        raise RuntimeError("Response loop contains 'break'; trial could end without an answer")

    print(f"{PASS_MARKER} source={main_py}")
    print("response_loop=while_not_next_data")
    print(f"response_transitions={len(transitions)}")
    print("stimulus_timeout=none")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail closed unless upstream native trials remain response-gated with no stimulus timeout."
    )
    parser.add_argument("--upstream-root", required=True, type=Path)
    args = parser.parse_args()

    try:
        validate(args.upstream_root.resolve() / "src" / "tobii_pytracker" / "main.py")
    except Exception as exc:
        print(f"NATIVE_RESPONSE_GATE_FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

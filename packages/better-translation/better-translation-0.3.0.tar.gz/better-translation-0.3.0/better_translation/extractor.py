from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from pathlib import Path

    from better_translation.types import MessageID, TranslatedText


FUNCTION_NAMES_TO_EXTRACT_FROM = (
    "gettext",
    "ngettext",
    "lazy_gettext",
    "lazy_ngettext",
    "_",
    "__",
)


@dataclass(slots=True)
class ExtractedMessage:
    id: MessageID = field(init=False)
    default: TranslatedText | None = field(init=False)
    default_plural: TranslatedText | None = field(init=False)
    context: Any | None = field(init=False)
    extra: dict[str, str | int | None] = field(init=False)

    def __init__(
        self,
        message_id: str,
        /,
        default: TranslatedText | None = None,
        default_plural: TranslatedText | None = None,
        context: Any | None = None,
        **extra: Any,
    ) -> None:
        self.id = message_id
        self.default = default
        self.default_plural = default_plural
        self.context = context
        self.extra = extra


def extract_from_code(
    code: str,
    function_names: Sequence[str] = FUNCTION_NAMES_TO_EXTRACT_FROM,
) -> Iterable[ExtractedMessage]:
    """Extract messages from Python code."""
    function_calls_params: list[dict[str, Any]] = []

    class FunctionCallVisitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
            if (
                isinstance(node.func, ast.Name)
                and node.func.id in function_names
            ):
                args = [
                    ast.literal_eval(arg)
                    if isinstance(arg, ast.Constant)
                    else None
                    for arg in node.args
                ]
                kwargs = {
                    kw.arg: ast.literal_eval(kw.value)
                    if isinstance(kw.value, ast.Constant)
                    else None
                    for kw in node.keywords
                }
                function_calls_params.append({"args": args, "kwargs": kwargs})

            self.generic_visit(node)

    visitor = FunctionCallVisitor()
    tree = ast.parse(code)
    visitor.visit(tree)

    for function_call_params in function_calls_params:
        call_params = ", ".join(
            (
                *(f"{value!r}" for value in function_call_params["args"]),
                *(
                    f"{key}={value!r}"
                    for key, value in function_call_params["kwargs"].items()
                ),
            ),
        )
        yield eval(f"ExtractedMessage({call_params})")  # noqa: PGH001


def extract_from_file(
    file_path: Path,
    function_names: Sequence[str] = FUNCTION_NAMES_TO_EXTRACT_FROM,
) -> Iterable[ExtractedMessage]:
    """Extract messages from a Python file."""
    yield from extract_from_code(file_path.read_text(), function_names)


def extract_from_dir(
    directory_path: Path,
    function_names: Sequence[str] = FUNCTION_NAMES_TO_EXTRACT_FROM,
) -> Iterable[ExtractedMessage]:
    """Extract messages from Python files in a directory."""
    for path in directory_path.rglob("*.py"):
        yield from extract_from_file(path, function_names)

"""Core JSONPath configuration object."""
from __future__ import annotations

import re
from collections.abc import Collection
from operator import getitem
from typing import TYPE_CHECKING
from typing import Any
from typing import AsyncIterable
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Union

from .exceptions import JSONPathSyntaxError
from .filter import UNDEFINED
from .lex import Lexer
from .parse import Parser
from .path import CompoundJSONPath
from .path import JSONPath
from .stream import TokenStream
from .token import TOKEN_EOF
from .token import TOKEN_INTERSECTION
from .token import TOKEN_UNION

if TYPE_CHECKING:
    from .match import FilterContextVars
    from .match import JSONPathMatch


class JSONPathEnvironment:
    """JSONPath configuration."""

    # These should be unescaped strings. `re.escape` will be called
    # on them automatically when compiling lexer rules.
    intersection_token = "&"
    root_token = "$"
    self_token = "@"
    union_token = "|"
    filter_context_token = "#"

    lexer_class = Lexer
    parser_class = Parser

    def __init__(self) -> None:
        self.lexer = self.lexer_class(env=self)
        self.parser = self.parser_class(env=self)

    def compile(self, path: str) -> Union[JSONPath, CompoundJSONPath]:  # noqa: A003
        """Prepare an internal representation of a JSONPath string."""
        tokens = self.lexer.tokenize(path)
        stream = TokenStream(tokens)
        _path: Union[JSONPath, CompoundJSONPath] = JSONPath(
            env=self, selectors=self.parser.parse(stream)
        )

        if stream.current.kind != TOKEN_EOF:
            _path = CompoundJSONPath(_path)
            while stream.current.kind != TOKEN_EOF:
                if stream.current.kind == TOKEN_UNION:
                    stream.next_token()
                    _path.union(
                        JSONPath(
                            env=self,
                            selectors=self.parser.parse(stream),
                        )
                    )
                elif stream.current.kind == TOKEN_INTERSECTION:
                    stream.next_token()
                    _path.intersection(
                        JSONPath(
                            env=self,
                            selectors=self.parser.parse(stream),
                        )
                    )
                else:  # pragma: no cover
                    # Parser.parse catches this too
                    raise JSONPathSyntaxError(  # noqa: TRY003
                        f"unexpected token {stream.current.value!r}",
                        token=stream.current,
                    )

        return _path

    def findall(
        self,
        path: str,
        data: Union[str, Sequence[Any], Mapping[str, Any]],
        *,
        filter_context: Optional[FilterContextVars] = None,
    ) -> List[object]:
        """Find all objects in `data` matching the given JSONPath `path`.
        Return a list of matches, or an empty list if no matches.

        If `data` is a string, it will be loaded using :meth:`json.loads` and
        the default `JSONDecoder`.

        Raises a :class:`JSONPathSyntaxError` if the path is invalid.
        """
        return self.compile(path).findall(data, filter_context=filter_context)

    def finditer(
        self,
        path: str,
        data: Union[str, Sequence[Any], Mapping[str, Any]],
        *,
        filter_context: Optional[FilterContextVars] = None,
    ) -> Iterable[JSONPathMatch]:
        """Return an iterator yielding :class:`JSONPathMatch` objects for each
        match of the path in the given `data`.

        If `data` is a string, it will be loaded using :meth:`json.loads`.

        Raises a :class:`JSONPathSyntaxError` if the path is invalid.
        """
        return self.compile(path).finditer(data, filter_context=filter_context)

    async def findall_async(
        self,
        path: str,
        data: Union[str, Sequence[Any], Mapping[str, Any]],
        *,
        filter_context: Optional[FilterContextVars] = None,
    ) -> List[object]:
        """An async version of :meth:`findall`."""
        return await self.compile(path).findall_async(
            data, filter_context=filter_context
        )

    async def finditer_async(
        self,
        path: str,
        data: Union[str, Sequence[Any], Mapping[str, Any]],
        *,
        filter_context: Optional[FilterContextVars] = None,
    ) -> AsyncIterable[JSONPathMatch]:
        """An async version of :meth:`finditer`."""
        return await self.compile(path).finditer_async(
            data, filter_context=filter_context
        )

    def getitem(self, obj: Any, key: Any) -> Any:
        """Sequence and mapping item getter used throughout JSONPath resolution."""
        return getitem(obj, key)

    async def getitem_async(self, obj: Any, key: object) -> Any:
        """An async sequence and mapping item getter."""
        if hasattr(obj, "__getitem_async__"):
            return await obj.__getitem_async__(key)
        return getitem(obj, key)

    def is_truthy(self, obj: object) -> bool:
        """Test for truthiness when evaluating JSONPath filters."""
        if obj is UNDEFINED:
            return False
        if isinstance(obj, Collection):
            return True
        if obj is None:
            return True
        return bool(obj)

    # ruff: noqa: PLR0912, PLR0911
    def compare(self, left: object, operator: str, right: object) -> bool:
        """Object comparison within JSONPath filters."""
        if operator == "&&":
            return self.is_truthy(left) and self.is_truthy(right)
        if operator == "||":
            return self.is_truthy(left) or self.is_truthy(right)

        if operator == "==":
            return bool(left == right)
        if operator in ("!=", "<>"):
            return bool(left != right)

        if isinstance(right, Sequence) and operator == "in":
            return left in right

        if isinstance(left, Sequence) and operator == "contains":
            return right in left

        if left is UNDEFINED or right is UNDEFINED:
            return operator == "<="

        if operator == "=~" and isinstance(right, re.Pattern) and isinstance(left, str):
            return bool(right.match(left))

        if isinstance(left, str) and isinstance(right, str):
            if operator == "<=":
                return left <= right
            if operator == ">=":
                return left >= right
            if operator == "<":
                return left < right

            assert operator == ">"
            return left > right

        # This will catch booleans too.
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if operator == "<=":
                return left <= right
            if operator == ">=":
                return left >= right
            if operator == "<":
                return left < right

            assert operator == ">"
            return left > right

        if (
            isinstance(left, Mapping)
            and isinstance(right, Mapping)
            and operator == "<="
        ):
            return left == right

        if (
            isinstance(left, Sequence)
            and isinstance(right, Sequence)
            and operator == "<="
        ):
            return left == right

        if left is None and right is None and operator in ("<=", ">="):
            return True

        return False

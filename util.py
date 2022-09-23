from typing import List, Sequence, cast

from clingo import ast
from clingo.ast import AST, ASTType


def parse_files(files: Sequence[str]) -> list[AST]:
    """
    Parse a statement.
    """
    stms: List[AST] = []
    ast.parse_files(files, stms.append, lambda code, msg: None, 1)
    return [stm for stm in stms if stm.ast_type == ASTType.Rule]


def parse_program(stm: str) -> list[AST]:
    """
    Parse a statement.
    """
    stms: List[AST] = []
    ast.parse_string(stm, stms.append, lambda code, msg: None, 1)
    return [stm for stm in stms if stm.ast_type == ASTType.Rule]


def parse_statement(stm: str) -> AST:
    """
    Parse a statement.
    """
    stms: List[AST] = []
    ast.parse_string(stm, stms.append, lambda code, msg: None, 1)
    if len(stms) != 2:
        raise RuntimeError(
            f"syntax error: stm must contain exactly one statement, {len(stms)} given"
        )
    return cast(AST, stms[1])


def head_as_disjunction(head: AST) -> AST:
    if head.ast_type == ASTType.Literal:
        clit = ast.ConditionalLiteral(head.location, head, [])
        return ast.Disjunction(head.location, [clit])
    elif head.ast_type == ASTType.Disjunction:
        return head
    assert False


def head_symbolic_atoms(rule: AST) -> List[AST]:
    assert rule.ast_type == ASTType.Rule
    head = head_as_disjunction(rule.head)
    return [
        clit.literal.atom.symbol
        for clit in head.elements
        if clit.literal.atom.ast_type == ASTType.SymbolicAtom
    ]


def body_symbolic_atoms(rule: AST) -> List[AST]:
    assert rule.ast_type == ASTType.Rule
    return [
        lit.atom.symbol
        for lit in rule.body
        if lit.atom.ast_type == ASTType.SymbolicAtom
    ]

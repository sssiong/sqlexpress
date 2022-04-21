from typing import List

from .structures import clauses as cl, basics as bs


def remove_comments(text: str) -> str:

    new_lines = []

    # loop through each line
    for line in text.split('\n'):

        # loop through each character
        for i in range(len(line)):

            # if exist comment characters, cut short the line
            if line[i] == '#':
                line = line[:i]
                break
            if i > 0 and line[i-1:i+1] == '--':
                line = line[:i-1]
                break

        # keep line if it's not a comment line
        if len(line.strip()) > 0:
            new_lines.append(line.strip())

    return '\n'.join(new_lines)


def split_with_brackets(text: str) -> List[str]:
    output = []
    tmp = ''
    counter = 0
    for char in text:
        if char == ',' and counter == 0:
            output.append(tmp.strip())
            tmp = ''
            continue
        if char == ',' and counter > 0:
            tmp += char
            continue
        if char == '(':
            counter += 1
            tmp += char
            continue
        if char == ')':
            counter -= 1
            tmp += char
            continue
        tmp += char

    if len(tmp) > 0:
        output.append(tmp)

    return output


def print_clauses(clause_list: List[cl.Clause], indent: int = 0) -> None:

    for clause in clause_list:

        if isinstance(clause, cl.CteEndClause) \
                or isinstance(clause, cl.SubqueryEndClause):
            indent -= 2

        print(f'{" "*indent}{clause}')

        if isinstance(clause, cl.CteStartClause) \
                or isinstance(clause, cl.SubqueryStartClause):
            indent += 2


def print_basics(basic_list: List[bs.BasicQuery]) -> None:
    indent = 0
    for basic in basic_list:
        print(f'{basic.__class__.__name__}(clauses=[')
        print_clauses(basic.clauses, indent+2)
        print(f'])')

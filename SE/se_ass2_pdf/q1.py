
import re
import math


def remove_comments(code):
    pattern = (
        r'"(?:\\.|[^"\\])*"'
        r"|'(?:\\.|[^'\\])*'"
        r'|//[^\n]*'
        r'|/\*.*?\*/'
    )

    def replace(match):
        token = match.group()

        if token.startswith('"') or token.startswith("'"):
            return token

        return "".join("\n" if ch == "\n" else " " for ch in token)

    return re.sub(pattern, replace, code, flags=re.DOTALL)


def tokenize(code):
    pattern = (
        r'"(?:\\.|[^"\\])*"'
        r"|'(?:\\.|[^'\\])*'"
        r'|#include'
        r'|<[A-Za-z_][A-Za-z0-9_.]*>'
        r'|[A-Za-z_][A-Za-z0-9_]*'
        r'|[0-9][A-Za-z0-9.]*'
        r'|==|!=|<=|>=|\+\+|--|&&|\|\||\+=|-=|\*=|/='
        r'|[^\s]'
    )
    return re.findall(pattern, code)


HALSTEAD_OPERATORS = {
    "#include", "void", "main", "int",
    "scanf", "printf",
    "&", "=", "+", "-", "*", "/", "%",
    "==", "!=", "<", ">", "<=", ">=",
    "++", "--", "&&", "||", "!",
    "+=", "-=", "*=", "/="
}

SYMBOLIC_OPERATORS = {
    "+", "-", "*", "/", "%", "=",
    "==", "!=", "<", ">", "<=", ">=",
    "++", "--", "&", "&&", "||", "!",
    "+=", "-=", "*=", "/="
}

DELIMITERS = {",", ";", "(", ")", "{", "}", "[", "]"}


def classify(token):
    if not token:
        return "invalid token"

    if token == "#include":
        return "operator"

    if token.startswith('"') and token.endswith('"'):
        return "operand"

    if token.startswith("'") and token.endswith("'"):
        return "operand"

    if re.fullmatch(r'<[A-Za-z_][A-Za-z0-9_.]*>', token):
        return "operand"

    if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', token):
        if not token[0].isalpha() or len(token) > 8:
            return "invalid identifier"
        return "identifier"

    if re.fullmatch(r'[0-9]+(\.[0-9]+)?', token):
        return "constant"

    if re.fullmatch(r'[0-9][A-Za-z0-9.]*', token):
        return "invalid constant"

    if token in SYMBOLIC_OPERATORS:
        return "operator"

    if token in DELIMITERS:
        return "delimiter"

    return "invalid token"


def classify_halstead(token):
    if token in DELIMITERS:
        return "delimiter"

    if token in HALSTEAD_OPERATORS:
        return "operator"

    if token.startswith('"') and token.endswith('"'):
        return "operand"

    if token.startswith("'") and token.endswith("'"):
        return "operand"

    if re.fullmatch(r'<[A-Za-z_][A-Za-z0-9_.]*>', token):
        return "operand"

    if re.fullmatch(r'[0-9]+(\.[0-9]+)?', token):
        return "operand"

    if re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', token):
        return "operand"

    return "other"


def find_invalid_tokens(tokens):
    invalid_identifiers = []
    invalid_constants = []
    invalid_operators = []

    for token in tokens:
        category = classify(token)

        if category == "invalid identifier":
            invalid_identifiers.append(token)
        elif category == "invalid constant":
            invalid_constants.append(token)
        elif category == "invalid token":
            invalid_operators.append(token)

    return (
        sorted(set(invalid_identifiers)),
        sorted(set(invalid_constants)),
        sorted(set(invalid_operators))
    )


def count_halstead(tokens):
    operators = []
    operands = []

    for token in tokens:
        category = classify_halstead(token)

        if category == "operator":
            operators.append(token)
        elif category == "operand":
            operands.append(token)

    N1 = len(operators)
    N2 = len(operands)
    eta1 = len(set(operators))
    eta2 = len(set(operands))

    return N1, N2, eta1, eta2, operators, operands


def find_input_operands(tokens):
    input_operands = set()

    for i, token in enumerate(tokens):
        if token != "scanf":
            continue

        j = i + 1

        if j >= len(tokens) or tokens[j] != "(":
            continue

        while j < len(tokens) and tokens[j] != ")":
            if tokens[j] == "&" and j + 1 < len(tokens):
                candidate = tokens[j + 1]

                if re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', candidate):
                    if len(candidate) <= 8:
                        input_operands.add(candidate)

            j += 1

    return input_operands


def calculate_metrics(N1, N2, eta1, eta2, eta2_star):
    N = N1 + N2

    if eta1 == 0 or eta2 == 0:
        print("Cannot calculate metrics: operators or operands are missing.")
        return

    Ne = eta1 * math.log2(eta1) + eta2 * math.log2(eta2)
    V = N * math.log2(eta1 + eta2)
    Vc = (2 + eta2_star) * math.log2(2 + eta2_star)
    L = Vc / V
    E = V / L if L != 0 else float("inf")

    print("\n--- Halstead Metrics ---")
    print("N1 (Total operator occurrences):", N1)
    print("N2 (Total operand occurrences):", N2)
    print("eta1 (Distinct operators):", eta1)
    print("eta2 (Distinct operands):", eta2)
    print("eta2* (Distinct input operands):", eta2_star)
    print("N (Actual program length):", N)
    print("Ne (Estimated program length):", round(Ne, 4))
    print("V (Program volume):", round(V, 4), "bits")
    print("Vc (Critical volume):", round(Vc, 4), "bits")
    print("L (Program level):", round(L, 4))
    print("E (Program effort):", round(E, 4))


def main():
    filename = input("Enter the source filename (.txt): ")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            source_code = file.read()
    except FileNotFoundError:
        print("Error: File not found. Check the filename and path.")
        return
    except OSError as error:
        print("Error reading file:", error)
        return

    clean_code = remove_comments(source_code)
    tokens = tokenize(clean_code)

    invalid_ids, invalid_consts, invalid_ops = find_invalid_tokens(tokens)

    print("\n--- Lexical Analysis ---")
    print("Invalid identifiers:", invalid_ids)
    print("Invalid constants:", invalid_consts)
    print("Invalid operators/tokens:", invalid_ops)

    N1, N2, eta1, eta2, operators, operands = count_halstead(tokens)

    print("\n--- Halstead Token Counts ---")
    print("Operator occurrences:", operators)
    print("Operand occurrences:", operands)
    print("Distinct operators:", eta1)
    print("Distinct operands:", eta2)

    input_operands = find_input_operands(tokens)
    print("Input operands:", sorted(input_operands))

    calculate_metrics(N1, N2, eta1, eta2, len(input_operands))


if __name__ == "__main__":
    main()

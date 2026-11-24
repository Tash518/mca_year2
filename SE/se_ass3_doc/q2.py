import re
import math

OPERATORS = {
    "+",
    "-",
    "*",
    "/",
    "%",
    "=",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "==",
    "!=",
    "<",
    ">",
    "<=",
    ">=",
    "&&",
    "||",
    "!",
    "&",
    "|",
    "^",
    "~",
    "<<",
    ">>",
    "<<=",
    ">>=",
    "++",
    "--",
    "->",
    ".",
    "?",
    ":",
}

KEYWORDS = {
    "auto",
    "break",
    "case",
    "char",
    "const",
    "continue",
    "default",
    "do",
    "double",
    "else",
    "enum",
    "extern",
    "float",
    "for",
    "goto",
    "if",
    "inline",
    "int",
    "long",
    "register",
    "restrict",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "struct",
    "switch",
    "typedef",
    "union",
    "unsigned",
    "void",
    "volatile",
    "while",
    "_Bool",
}


def read_file(filename):
    with open(filename, "r") as file:
        source = file.read()
    return source


def tokenize(source):

    # remove preprocessor
    source = re.sub(r"^\s*#.*$", "", source, flags=re.MULTILINE)

    # regex to identify tokens
    pattern = (
        r'"(?:\\.|[^"\\])*"'
        r"|'(?:\\.|[^'\\])*'"
        r"|//[^\n]*"
        r"|/\*[\s\S]*?\*/"
        r"|(?:0[xX][0-9a-fA-F]+|\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)"
        r"|[A-Za-z_][A-Za-z0-9_]*"
        r"|>>=|<<=|->|\+\+|--|==|!=|<=|>="
        r"|&&|\|\||<<|>>|\+=|-=|\*=|/=|%="
        r"|[+\-*/%=<>!&|^~?:.]"
        r"|[(){}\[\],;]"
    )

    tokens = re.findall(pattern, source)

    # handle comments
    tokens = [
        token
        for token in tokens
        if not token.startswith("//") and not token.startswith("/*")
    ]

    return tokens


# ==========================================
# STEP 4: CLASSIFY OPERATORS AND OPERANDS
# ==========================================


def classify_tokens(tokens):

    operators = []
    operands = []

    input_operands = set()

    for i, token in enumerate(tokens):
        if token in KEYWORDS:
            operators.append(token)
        elif token in OPERATORS:
            operators.append(token)
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            if i + 1 < len(tokens) and tokens[i + 1] == "(":
                operators.append(token)

            else:
                operands.append(token)

        elif (
            token.startswith('"')
            or token.startswith("'")
            or re.fullmatch(
                r"(?:0[xX][0-9a-fA-F]+|\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)", token
            )
        ):
            operands.append(token)
        else:
            continue
    for i, token in enumerate(tokens):
        if token == "scanf":
            j = i + 1
            while j < len(tokens) and tokens[j] != ";":
                if (
                    tokens[j] == "&"
                    and j + 1 < len(tokens)
                    and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", tokens[j + 1])
                ):
                    input_operands.add(tokens[j + 1])

                j += 1
        if token == "cin":
            j = i + 1
            while j + 1 < len(tokens) and tokens[j] == ">>":

                input_operands.add(tokens[j + 1])
                j += 2

    return operators, operands, input_operands


# hastead part
def calculate_metrics(operators, operands, input_operands):
    eta1 = len(set(operators))
    eta2 = len(set(operands))
    N1 = len(operators)
    N2 = len(operands)

    N = N1 + N2

    Ne = 0
    if eta1 > 0:
        Ne += eta1 * math.log2(eta1)
    if eta2 > 0:
        Ne += eta2 * math.log2(eta2)

    vocabulary = eta1 + eta2

    if vocabulary > 0:
        V = N * math.log2(vocabulary)
    else:
        V = 0

    eta2_star = len(input_operands)

    critical_vocabulary = 2 + eta2_star

    Vc = critical_vocabulary * math.log2(critical_vocabulary)

    if V > 0:
        L = Vc / V
    else:
        L = 0

    if L > 0:
        E = V / L
    else:
        E = 0

    # program time (mental discrimination = 18 seconds)
    T = E / 18

    # NO of people (development duration = 5 months)
    duration = 5 * 30 * 24 * 60 * 60

    if T > 0:
        people = math.ceil(T / duration)
    else:
        people = 0

    metrics = {
        "eta1": eta1,
        "eta2": eta2,
        "N1": N1,
        "N2": N2,
        "N": N,
        "Ne": Ne,
        "V": V,
        "eta2_star": eta2_star,
        "Vc": Vc,
        "L": L,
        "E": E,
        "T": T,
        "people": people,
    }

    return metrics


# menu


def display_menu():

    print("\n========== HALSTEAD SOFTWARE METRICS ==========")

    print("1. Unique number of operators and operands")
    print("2. Total number of operators and operands")
    print("3. Actual Program Length")
    print("4. Expected Program Length")
    print("5. Program Volume")
    print("6. Program Critical Volume")
    print("7. Program Level")
    print("8. Effort to develop Program")
    print("9. Program Time")
    print("10. Number of People engaged")
    print("0. Exit")

    print("================================================")


def main():

    filename = input("Enter C program filename: ")

    try:
        source = read_file(filename)

    except FileNotFoundError:
        print("Error: File not found!")
        return
    # tokenis
    tokens = tokenize(source)

    # classify
    operators, operands, input_operands = classify_tokens(tokens)

    # calculate all metrics
    metrics = calculate_metrics(operators, operands, input_operands)

    print("\nC program successfully analysed!")

    print("Total tokens:", len(tokens))
    while True:

        display_menu()

        choice = input("Enter your choice: ")

        if choice == "1":

            print("\nUnique operators:", metrics["eta1"])
            print("Unique operands:", metrics["eta2"])

        elif choice == "2":

            print("\nTotal operators:", metrics["N1"])
            print("Total operands:", metrics["N2"])

        elif choice == "3":

            print("\nActual Program Length:", metrics["N"])

        elif choice == "4":

            print("\nExpected Program Length:", round(metrics["Ne"], 4))

        elif choice == "5":

            print("\nProgram Volume:", round(metrics["V"], 4))

        elif choice == "6":

            print("\nProgram Critical Volume:", round(metrics["Vc"], 4))

        elif choice == "7":

            print("\nProgram Level:", round(metrics["L"], 6))

        elif choice == "8":

            print("\nEffort to develop Program:", round(metrics["E"], 4))

        elif choice == "9":

            print("\nProgram Time:", round(metrics["T"], 4), "seconds")

            print("Program Time:", round(metrics["T"] / 3600, 4), "hours")

        elif choice == "10":

            print("\nNumber of People engaged:", metrics["people"])

        elif choice == "0":

            print("\nExiting program...")
            break

        else:

            print("\nInvalid choice! Please enter a valid option.")


if __name__ == "__main__":
    main()

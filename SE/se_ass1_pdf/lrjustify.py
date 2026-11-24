def justify_line(words, width):
    if len(words) == 1:
        return words[0].ljust(width)

    total_chars = sum(len(word) for word in words)
    total_spaces = width - total_chars

    gaps = len(words) - 1

    spaces_per_gap = total_spaces // gaps
    extra_spaces = total_spaces % gaps

    line = ""

    for i in range(gaps):
        line += words[i]
        spaces = spaces_per_gap

        if i < extra_spaces:
            spaces += 1

        line += " " * spaces

    line += words[-1]

    return line


def format_paragraph(text, width, indent, alignment):
    words = text.split()

    lines = []
    current_line = []
    current_length = 0

    first_line = True

    for word in words:

        # Available width considering indentation
        available_width = width - indent if first_line else width

        if not current_line:
            current_line.append(word)
            current_length = len(word)

        elif current_length + 1 + len(word) <= available_width:
            current_line.append(word)
            current_length += 1 + len(word)

        else:
            lines.append((current_line, available_width))
            current_line = [word]
            current_length = len(word)
            first_line = False

    if current_line:
        available_width = width - indent if first_line else width
        lines.append((current_line, available_width))

    result = []

    for i, (line_words, available_width) in enumerate(lines):

        prefix = " " * indent if i == 0 else ""

        # Last line is not fully justified
        if i == len(lines) - 1:
            line = " ".join(line_words)

            if alignment == "left":
                line = line.ljust(available_width)
            else:
                line = line.rjust(available_width)

        else:
            line = justify_line(line_words, available_width)

        result.append(prefix + line)

    return result


def main():
    print("TEXT JUSTIFICATION PROGRAM")

    width = int(input("Enter line width: "))
    indent = int(input("Enter paragraph indentation: "))

    if width <= 0 or indent < 0 or indent >= width:
        print("Invalid width or indentation.")
        return

    print("\nEnter text.")
    print("Enter a blank line to finish a paragraph.")
    print("Enter END to finish input.\n")

    paragraphs = []
    current_paragraph = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            if current_paragraph:
                paragraphs.append(" ".join(current_paragraph))
            break

        elif line.strip() == "":
            if current_paragraph:
                paragraphs.append(" ".join(current_paragraph))
                current_paragraph = []

        else:
            current_paragraph.append(line.strip())

    print("\nChoose alignment:")
    print("1. Left Justification")
    print("2. Right Justification")

    choice = input("Enter choice: ")

    if choice not in ("1", "2"):
        print("Invalid choice.")
        return

    alignment = "left" if choice == "1" else "right"

    print("\nFormatted Text:\n")

    for paragraph in paragraphs:
        formatted = format_paragraph(
            paragraph, width, indent, alignment
        )

        for line in formatted:
            print(line)

        print()


if __name__ == "__main__":
    main()

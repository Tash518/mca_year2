text = input("Enter the text: ")
pattern = input("Enter the pattern to search for: ")
relacement = input("Enter te replacement string: ")

if pattern in text:
    print("pattern found...")
    text = text.replace(pattern, relacement)
    print("New text:\n", text)
else:
    print("pattern not found")
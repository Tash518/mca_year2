from enum import Enum, auto


class Token:

    def __init__(self, token_type, value, position, error_msg=None):
        self.type = token_type
        self.value = value
        self.position = position
        self.error_msg = error_msg

    def __repr__(self):
        if self.error_msg:
            return f"Token(ERROR, value{self.value}, pos = {self.position}, msg = {self.error_msg})"
        return f"Token({self.type.name}, value{self.value}, pos = {self.position})"


class TokenType(Enum):
    KEYWORD = auto()
    OPERATOR = auto()
    CONSTANT = auto()
    IDENTIFIER = auto()
    SYMBOL = auto()
    ERROR = auto()


class TransitionLexer:
    KEYWORDS = {"if", "for", "while", "int", "float", "char"}
    OPERATORS = {"+", "-", "*", "/", "=", "<", ">"}
    SYMBOLS = {",", "(", ")", ";", "?"}

    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0
        self.length = len(source_code)

    def _peek(self):
        return self.source[self.pos] if self.pos < self.length else ""

    def _advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        return ch

    def _transition_identifier_or_keyword(self):
        start_pos = self.pos
        lexeme = ""
        while self.pos < self.length and (self._peek().isalnum() or self._peek == "_"):
            lexeme += self._advance()
        if len(lexeme) > 8:
            return Token(
                TokenType.ERROR,
                lexeme,
                start_pos,
                f"Identifier '{lexeme}' exceedds 8 characters.",
            )
        if lexeme in self.KEYWORDS:
            return Token(TokenType.KEYWORD, lexeme, start_pos)
        return Token(TokenType.IDENTIFIER, lexeme, start_pos)

    def _transition_constant(self):
        start_pos = self.pos
        lexeme = ""

        if self._peek() == "0":
            while self.pos < self.length and self._peek().isdigit():
                lexeme += self._advance()
            return Token(
                TokenType.ERROR,
                lexeme,
                start_pos,
                "Invalid constant: Leading zeros notnot allowed.",
            )
        while self.pos < self.length and self._peek().isdigit():
            lexeme += self._advance()
        if self.pos < self.length and (self._peek().isalpha() or self._peek() == "_"):
            while self.pos < self.length and (
                self._peek().isalpha() or self._peek() == "_"
            ):
                lexeme += self._advance()
            return Token(
                TokenType.ERROR,
                lexeme,
                start_pos,
                f"Invalid token {lexeme} : numbers cant attach to letters",
            )
        val = int(lexeme)
        if 1 <= val <= 999:
            return Token(TokenType.CONSTANT, lexeme, start_pos)
        else:
            return Token(
                TokenType.ERROR,
                lexeme,
                start_pos,
                f"Invalid constant: {val} is out of range (1-999).",
            )

    def tokenise(self):
        tokens = []
        while self.pos < self.length:
            ch = self._peek()
            if ch.isspace():
                self._advance()
                continue
            start_pos = self.pos
            if ch.isalpha():
                tokens.append(self._transition_identifier_or_keyword())
            elif ch.isdigit():
                tokens.append(self._transition_constant())
            elif ch in self.OPERATORS:
                tokens.append(Token(TokenType.OPERATOR, self._advance(), start_pos))
            elif ch in self.SYMBOLS:
                tokens.append(Token(TokenType.SYMBOL, self._advance(), start_pos))
            else:
                invalid_char = self._advance()
                tokens.append(
                    Token(
                        TokenType.ERROR,
                        invalid_char,
                        start_pos,
                        f"Invalid character: {invalid_char}",
                    )
                )
        return tokens


if __name__ == "__main__":
    test_statements = [
        "if (val1 <= 99) count = count + 1;",
        "int long_identifier_name = 1000;",
        "float x = 0 + 10 ? y : z;",
        "char 123var = @;"
    ]

    for i, statement in enumerate(test_statements, 1):
        print(f'\n--- Test Statement {i}: "{statement}" ---')
        lexer = TransitionLexer(statement)
        for token in lexer.tokenise():
            print(token)

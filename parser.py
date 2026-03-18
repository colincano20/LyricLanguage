from tokenizer import TokenType, Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def current(self):
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return None

    def eat(self, expected_type):
        token = self.current()
        if token is None:
            raise SyntaxError(f"LyricScript Error: Unexpected end of file, expected {expected_type}")
        if token.type != expected_type:
            raise SyntaxError(f"LyricScript Error [line {token.line}]: Expected '{{' but got '{token.value}'")
        self.i += 1
        return token

    def parse(self):
        result = {
            "song": None,
            "structure": [],
            "sections": {}
        }

        while self.current() is not None:
            token = self.current()

            if token.type == TokenType.KEYWORD and token.value == "song":
                self.eat(TokenType.KEYWORD)
                title = self.eat(TokenType.STRING)
                result["song"] = title.value

            elif token.type == TokenType.KEYWORD and token.value == "structure":
                self.eat(TokenType.KEYWORD)
                self.eat(TokenType.LBRACE)
                result["structure"] = self.parse_structure()
                self.eat(TokenType.RBRACE)

            elif token.type == TokenType.KEYWORD and token.value == "meta":
                self.eat(TokenType.KEYWORD)
                self.eat(TokenType.LBRACE)
                self.skip_block()

            elif token.type == TokenType.SECTION:
                name = self.eat(TokenType.SECTION).value
                self.eat(TokenType.LBRACE)
                lines = self.parse_section_body()
                self.eat(TokenType.RBRACE)
                result["sections"][name] = {"lines": lines}

            else:
                raise SyntaxError(f"LyricScript Error [line {token.line}]: Unexpected token '{token.value}'")

        return result

    def parse_structure(self):
        order = []
        while self.current() and self.current().type != TokenType.RBRACE:
            if self.current().type == TokenType.SECTION:
                order.append(self.eat(TokenType.SECTION).value)
            elif self.current().type == TokenType.ARROW:
                self.eat(TokenType.ARROW)
            else:
                token = self.current()
                raise SyntaxError(f"LyricScript Error [line {token.line}]: Unexpected token '{token.value}' in structure")
        return order

    def parse_section_body(self):
        lines = []

        while self.current() and self.current().type != TokenType.RBRACE:
            token = self.current()

            if token.type == TokenType.STRING:
                self.eat(TokenType.STRING)
                lines.append(token.value)

            elif token.type == TokenType.KEYWORD and token.value == "repeat":
                self.eat(TokenType.KEYWORD)
                count = self.eat(TokenType.NUMBER).value
                if lines:
                    last_line = lines[-1]
                    for _ in range(count - 1):
                        lines.append(last_line)

            else:
                raise SyntaxError(f"LyricScript Error [line {token.line}]: Unexpected token '{token.value}' in section")

        return lines

    def skip_block(self):
        depth = 1
        while self.current() and depth > 0:
            if self.current().type == TokenType.LBRACE:
                depth += 1
            elif self.current().type == TokenType.RBRACE:
                depth -= 1
            self.i += 1
#!/usr/local/bin/python3

INT, MINUS, PLUS, MUL, DIV, EOF = 1, 2, 3, 4, 5, 0

class Token:
    def __init__(self, t, value = 0):
        self.type = t
        self.value = value


class EOFError(Exception):
    pass

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if len(self.text) else None

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespaces(self):
        while self.current_char == ' ':
            self.advance()

    def get_integer_token(self):
        result = ''
        while self.current_char != None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(INT, int(result))

    def get_next_token(self):
        self.skip_whitespaces()
        if self.current_char == None:
            return Token(EOF)
        if self.current_char.isdigit():
            return self.get_integer_token()
        elif self.current_char == '+':
            self.advance()
            return Token(PLUS)
        elif self.current_char == '-':
            self.advance()
            return Token(MINUS)
        elif self.current_char == '*':
            self.advance()
            return Token(MUL)
        elif self.current_char == '/':
            self.advance()
            return Token(DIV)
        else:
            raise Exception


class Interpreter:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()

    def eat(self, token):
        if self.current_token.type == token:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception

    def term(self):
        token = self.current_token
        self.eat(INT)
        return token.value

    def expr(self):
        result = self.term()

        while self.current_token and self.current_token.type in [MINUS, PLUS, DIV, MUL]:
            token = self.current_token
            if token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()
            elif token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.term()
            elif token.type == MUL:
                self.eat(MUL)
                result = result * self.term()
        return result


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()

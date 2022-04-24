#!/usr/local/bin/python3

PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, INT, EOF = 1,2,3,4,5,6,7,0

class Token:
    def __init__(self, token_type, value = 0):
        self.type = token_type
        self.value = value



class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def advance(self):
        self.pos += 1

    def skip_whitespaces(self):
        while self.pos < len(self.text) and self.text[self.pos] == ' ':
            self.advance()

    def get_digits(self):
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self.advance()
        return Token(INT, int(self.text[start : self.pos]))

    def get_next_token(self):

        if self.pos == len(self.text):
            return Token(EOF)

        self.skip_whitespaces()
        if self.text[self.pos] == '+':
            self.current_token = Token(PLUS)
            self.advance()
        elif self.text[self.pos] == '-':
            self.current_token = Token(MINUS)
            self.advance()
        elif self.text[self.pos] == '*':
            self.current_token = Token(MUL)
            self.advance()
        elif self.text[self.pos] == '/':
            self.current_token = Token(DIV)
            self.advance()
        elif self.text[self.pos] == '(':
            self.current_token = Token(LPAREN)
            self.advance()
        elif self.text[self.pos] == ')':
            self.current_token = Token(RPAREN)
            self.advance()
        elif self.text[self.pos].isdigit():
            self.current_token = self.get_digits()
        else:
            raise Exception
        return self.current_token

class Interpreter:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception


# factor = INT | ( expr )
# term = factor ([*/] term)*
# expr = term ([+-] term)*

    def factor(self):
        token = self.current_token
        if token.type == INT:
            self.eat(INT)
            return token.value
        else:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
        return result

    def term(self):
        result = self.factor()

        while self.current_token and self.current_token.type in [MUL, DIV]:
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.term()
            else:
                self.eat(DIV)
                result = result / self.term()

        return result

    def expr(self):
        result = self.term()

        while self.current_token and self.current_token.type in [PLUS, MINUS]:
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            else:
                self.eat(MINUS)
                result = result - self.term()
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

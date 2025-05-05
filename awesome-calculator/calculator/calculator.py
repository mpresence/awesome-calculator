import math
import re

class Calculator:
    def __init__(self):
        self.operations = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '^': lambda a, b: a ** b,
            'sqrt': lambda a: math.sqrt(a),
            'sin': lambda a: math.sin(math.radians(a)),
            'cos': lambda a: math.cos(math.radians(a)),
            'tan': lambda a: math.tan(math.radians(a)),
            'log': lambda a, base=10: math.log(a, base)
        }
    
    def tokenize(self, expression):
        # Replace functions with placeholders
        for func in ['sqrt', 'sin', 'cos', 'tan', 'log']:
            expression = expression.replace(func, f' {func} ')
        
        # Add spaces around operators and parentheses
        expression = re.sub(r'([\+\-\*\/\^\(\)])', r' \1 ', expression)
        
        # Split by whitespace and filter out empty strings
        tokens = [token for token in expression.split() if token.strip()]
        return tokens
    
    def parse(self, tokens):
        def parse_expression():
            return parse_add_sub()
        
        def parse_add_sub():
            left = parse_mul_div()
            while tokens and tokens[0] in ['+', '-']:
                op = tokens.pop(0)
                right = parse_mul_div()
                left = self.operations[op](left, right)
            return left
        
        def parse_mul_div():
            left = parse_power()
            while tokens and tokens[0] in ['*', '/']:
                op = tokens.pop(0)
                right = parse_power()
                if op == '/' and right == 0:
                    raise ZeroDivisionError("Division by zero")
                left = self.operations[op](left, right)
            return left
        
        def parse_power():
            left = parse_factor()
            if tokens and tokens[0] == '^':
                tokens.pop(0)  # Remove '^'
                right = parse_factor()
                return self.operations['^'](left, right)
            return left
        
        def parse_factor():
            if not tokens:
                raise ValueError("Unexpected end of expression")
            
            token = tokens.pop(0)
            
            if token == '(':
                result = parse_expression()
                if tokens and tokens[0] == ')':
                    tokens.pop(0)  # Remove ')'
                    return result
                raise ValueError("Missing closing parenthesis")
            elif token in ['sqrt', 'sin', 'cos', 'tan']:
                # Handle functions
                if tokens and tokens[0] == '(':
                    tokens.pop(0)  # Remove '('
                    arg = parse_expression()
                    if tokens and tokens[0] == ')':
                        tokens.pop(0)  # Remove ')'
                        return self.operations[token](arg)
                    raise ValueError(f"Missing closing parenthesis for {token}")
                raise ValueError(f"Expected '(' after {token}")
            elif token == 'log':
                # Handle log function with optional base
                if tokens and tokens[0] == '(':
                    tokens.pop(0)  # Remove '('
                    arg = parse_expression()
                    if tokens and tokens[0] == ',':
                        tokens.pop(0)  # Remove ','
                        base = parse_expression()
                        if tokens and tokens[0] == ')':
                            tokens.pop(0)  # Remove ')'
                            return self.operations[token](arg, base)
                    elif tokens and tokens[0] == ')':
                        tokens.pop(0)  # Remove ')'
                        return self.operations[token](arg)
                    raise ValueError("Missing closing parenthesis for log")
                raise ValueError("Expected '(' after log")
            else:
                # Parse numbers
                try:
                    return float(token)
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")
        
        return parse_expression()
    
    def evaluate(self, expression):
        # Clean up the expression
        expression = expression.lower().replace(' ', '')
        if not expression:
            return 0
        
        tokens = self.tokenize(expression)
        result = self.parse(tokens[:])  # Pass a copy of tokens
        
        # Check if all tokens were consumed
        if tokens:
            raise ValueError(f"Unexpected tokens at end of expression: {' '.join(tokens)}")
        
        # Return int if result is a whole number
        if result == int(result):
            return int(result)
        return result
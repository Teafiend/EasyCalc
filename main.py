#!/usr/bin/env python3


class Interpreter:
	def __init__(self, n={}):
		self.names = n;
		self.done_interpreting = False
	
	def evaluate(self, expression: str):
		super_tokens = expression.split(' ', 1)	
		if len(super_tokens) == 1:
			self.execute_command(super_tokens[0])
		else:
			self.execute_operation(super_tokens[0], super_tokens[1])
	
	def execute_command(self, command: str):
		if command == 'quit' or command == 'exit':
			self.done_interpreting = True
		elif command == 'vars' or command == 'variables':
			for key, val in self.names.items():
				print("{} = {}".format(key, val))
		else:
			print("Not a valid command")
		
	
	def execute_operation(self, verb, statement):
		if verb == 'let':
			self.perform_assignment(statement)
		else:
			print("not an assignment")
	
	def perform_assignment(self, statement):
		super_tokens = statement.split('=') # super_tokens[0] is name, [1] is value
		if '(' not in super_tokens[0]:
			self.names[super_tokens[0]] = \
			eval(super_tokens[1], globals(), self.names)
		else:
			# super_tokens[0] is of form: func_name(arg1, arg2, ...)
			tokens = super_tokens[0].rstrip(')').split('(')
			name = tokens[0]
			args = tuple(arg.strip() for arg in tokens[1].split(','))
			

def prompt(inter: Interpreter):
	user_in = input("$ ")
	inter.evaluate(user_in)
	return inter.done_interpreting

def main():
	inter = Interpreter()
	done = False
	while(not done):
		done = prompt(inter)

if __name__ == "__main__":
	main()

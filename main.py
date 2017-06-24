#!/usr/bin/env python3

class Interpreter:
	def __init__(self, v={}, f={}):
		self.variables = v
		self.functions = f	
		self.done_interpreting = False
	
	def evaluate(self, expression: str):
		super_tokens = expression.split(' ', 1)	
		if len(super_tokens) == 1:
			self.execute_command(super_tokens[0])
		else:
			print("More than one word")
	
	def execute_command(self, command: str):
		if command == 'quit' or command == 'exit':
			self.done_interpreting = True
		if command == 'vars' or command == 'variables':
			for key, val in self.variables.items():
				print("{} = {}".format(key, value))

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

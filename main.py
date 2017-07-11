#!/usr/bin/env python3

# TODO Add "help" command

INTEGRAL_ITERATIONS = 1000000

DEBUG_MODE = True

class InvalidCommandError(Exception):
	pass

class InvalidOperationError(Exception):
	pass

	

class Interpreter:
	def __init__(self, n={}):
		self.names = n;
		self.done_interpreting = False
	
	def build_function(self, expression: str, arg_tuple: tuple):
		def inner_function(*args):
			# arg_tuple = (x, y)
			# args = 3, 5
			arg_mapping = {arg_tuple[i] : args[i] for i in range(len(arg_tuple))}
			# TODO Potential name conflict between args and global names; fix it
			arg_mapping.update(self.names)
			print(arg_mapping)
			return eval(expression, globals(), arg_mapping)
		return inner_function

	def evaluate(self, expression: str):
		super_tokens = expression.split(' ', 1)	
		# TODO does not correctly evaluate expressions with spaces
		if len(super_tokens) == 1:
			self.execute_command(super_tokens[0])
		else:
			self.execute_operation(super_tokens[0], super_tokens[1])
	
	def execute_command(self, command: str):
		# A command is a verb; it does something
		if command == 'quit' or command == 'exit' or command == "q":
			self.done_interpreting = True
		elif command == 'vars' or command == 'variables':
			if DEBUG_MODE: 
				print(self.names)
			for key, val in self.names.items():
				print("{} = {}".format(key, val))
		elif command in self.names or command.split('(')[0] in self.names:
			print(eval(command, globals(), self.names))
		else:
			raise InvalidCommandError()
	
	def execute_operation(self, verb, statement):
		# An operation has a verb and a statement;
		# it does something with the statement
		if verb == 'let':
			self.perform_assignment(statement)
		elif verb == 'integrate':
			value = self.integrate(statement)
			# Ideally, truncate at 1/(square root of number of iterations)
			# TODO Make sure that math is correct
			print("{:.3f}".format(value))
		else:
			raise InvalidOperationError()
	
	def integrate(self, statement):
		tokens = statement.split()
		# [0]=func, [1]=from, [2]=lower, [3]=to, [4]=upper, [5]=over, [6]=var
		func = tokens[0]
		lower = int(tokens[2])
		upper = int(tokens[4])
		var = tokens[6]
		diff = upper - lower
		delta = diff / INTEGRAL_ITERATIONS
		mapping = {var: lower}
		accum = 0
		# TODO Animate this with some kind of loading bar
		print("Integrating with delta-{} of {}...".format(var, delta))
		while mapping[var] < upper:
			accum += self.names[func](mapping[var]) * delta
			mapping[var] += delta
		return accum
	
	def perform_assignment(self, statement):
		super_tokens = statement.split('=') # super_tokens[0] is name, [1] is value
		if '(' not in super_tokens[0]:
			self.names[super_tokens[0]] = \
			eval(super_tokens[1], globals(), self.names)
		else:
			# super_tokens[0] is of form: func_name(arg1, arg2, ...)
			tokens = super_tokens[0].rstrip(')').split('(')
			name = tokens[0] # maybe not needed
			args = tuple(arg.strip() for arg in tokens[1].split(','))
			func = self.build_function(super_tokens[1], args)
			self.names[name] = func


def prompt(inter: Interpreter):
	user_in = input("$ ")
	try:
		inter.evaluate(user_in)
	except InvalidOperationError:
		print("Invalid Operation")
		prompt(inter)
	except InvalidCommandError:
		print("Invalid Command")
		prompt(inter)
	return inter.done_interpreting


def main():
	inter = Interpreter()
	done = False
	while(not done):
		done = prompt(inter)


if __name__ == "__main__":
	main()

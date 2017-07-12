#!/usr/bin/env python3

# TODO Add "help" command
# TODO Allow user to input variables into function calls

INTEGRAL_ITERATIONS = 1000000

DEBUG_MODE = True

class InvalidCommandError(Exception):
	pass

class InvalidOperationError(Exception):
	pass

class MathExpression:
	def __init__(self, expr_string="", args=tuple()):
		self.expr = expr_string
		self.arg_names = args
	
	def __call__(self, names, arg_values):
		arg_mapping = {self.arg_names[i] : arg_values[i] \
			for i in range(len(self.arg_names))}
		arg_mapping.update(names)
		return eval(self.expr, globals(), arg_mapping)


class Interpreter:
	def __init__(self, n={}):
		self.names = n;
		self.done_interpreting = False
	
	def evaluate(self, expression: str):
		super_tokens = expression.split(' ', 1)	
		# TODO does not correctly evaluate expressions with spaces; fix
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
				if callable(val):
					formatted_args = ','.join(val.arg_names)
					print("{}({}) = {}".format(key, formatted_args, val.expr))
				else:
					print("{} = {}".format(key, val))
		elif command in self.names:
			print(eval(command, globals(), self.names))
		elif command.split('(')[0] in self.names:
			# TODO Make this use regex instead of splitting on commas
			arg_tokens = command.split('(')[1].rstrip(')').split(',')
			print(arg_tokens)
			arg_values = tuple((float(a) if '.' in a else int(a)) for a in arg_tokens)
			print(self.names[command.split('(')[0]](self.names, arg_values))
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
			# TODO Split on a regex instead of commas; need to account for spaces
			args = tuple(arg.strip() for arg in tokens[1].split(','))
			expression = MathExpression(super_tokens[1], args)
			self.names[name] = expression


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

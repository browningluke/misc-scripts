import sympy
s, u, v, a, t = sympy.var('s,u,v,a,t')

e1 = (u+a*t)-v
e2 = (0.5*(v+u)*t)-s
e3 = ((u*t) + (0.5*a*t*t))-s
e4 = ((u*u)+(2*a*s))-(v*v)

def solve(var_passed, variable):
	h1 = None
	var_used = None
	if var_passed == "s":
		var_used = s
	elif var_used == "u":
		var_used = u
	elif var_used == "v":
		var_used = v
	elif var_used == "a":
		var_used = a
	elif var_used == "t":
		var_used = t

	h = []
	for x in [e1, e2, e3, e4]:
		try:
			h1 = sympy.solve(x, var_passed)[0].evalf(subs={
				s:None if variable['s'] == "" else variable['s'],
				u:None if variable['u'] == "" else variable['u'],
				v:None if variable['v'] == "" else variable['v'],
				a:None if variable['a'] == "" else variable['a'],
				t:None if variable['t'] == "" else variable['t']})
		except Exception:
			pass
		else:
			h.append(h1)
	
	for x in h:
		if x is not None:
			return x

def main():
	print("\nPhysics Laws of Motion Calculator\n\
Variables:\n\
	u - initial velocity (m/s)\n\
	v - final velocity (m/s)\n\
	s - distance/displacement (m)\n\
	t - time (s)\n\
	a - acceleration (m/s^2)\n\
If variable is missing, hit 'enter' key")
	variable = {
		"s": input("Enter 's' variable: "),
		"u": input("Enter 'u' variable: "),
		"v": input("Enter 'v' variable: "),
		"a": input("Enter 'a' variable: "),
		"t": input("Enter 't' variable: "),
	}

	var_count = 0
	if variable["s"] != "":
		var_count += 1

	if variable["u"] != "":
		var_count += 1

	if variable["v"] != "":
		var_count += 1

	if variable["a"] != "":
		var_count += 1

	if variable["t"] != "":
		var_count += 1

	if var_count < 3:
		print("Please enter 3 or more variables.")
		return None

	for x in ["s", "u", "v", "a", "t"]:
		if variable[x] == "":
			print("{}: {}".format(x, solve(x, variable)))


if __name__ == '__main__':
	main()
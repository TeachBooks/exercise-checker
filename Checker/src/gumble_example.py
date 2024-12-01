from grading import check
from math import isclose

tolerance = 0.001

# Using rel_tol is more reliable in the face of aliasing, but to fit the instructions give we use abs_total
check_float = lambda a, b: isclose(a, b, rel_tol=0, abs_tol=tolerance)

# We have to pass in the globals object since we need to have access to changes as well
@check
def check_example(glob):
	mu, beta = glob["mu"], glob["beta"]
	if (check_float(mu, -1.7461520011511888) and check_float(beta, 2.553428469837263)):
		print(f"Part 1: you got the parameters right, well done! (checked with tolerance {tolerance})")
	else:
		print(f"Part 1: your parameters are incorrect. (checked with tolerance {tolerance})")
		print(f"          Other parts won't be graded until these are fixed. ")
		return 

	function = glob["find_x_with_probability_p"]
	
	test_inputs = [(1 - 0.001, 15.891029744351862), (1 - 0.2, 2.0838374640878863), (1 - 0.9, -3.875794191615308)]
	failed = []

	for x, out in test_inputs:
		result = function(x)
		if not check_float(result, out):
			failed.append((x, out, result))

	if len(failed) == 0:
		print(f"Part 2: Well done, your inverse function is correct! (checked with tolerance {tolerance})")	
	else:
		print(f"Part 2: Your function failed some tests. Keep in mind the tolerance is {tolerance}")
		print("    --> Failed inputs:")
		for case in failed:
			print(f"{case[0]} gave {case[2]}, expected {case[1]}")
		print(f"      Other parts won't be graded until these are fixed.")

	x = glob["x"]
	if check_float(x, 15.891029744351862):
		print(f"Part 3: you got the value of x right, well done! (checked with tolerance {tolerance})")
	else:
		print(f"Part 3: your value of x is incorrect. (checked with tolerance {tolerance})")
		return 
"""
Task 0:
x_1 = 4
p_1 = 1 - .1
x_2 = 10
p_2 = 1 - .01

Task 1:
	beta = -(x_2 - x_1) / log(log(p_2) / log(p_1))
    mu = x_1 + beta * log(-log(p_1))

Task 2:
x = mu - beta * log(-log(p))

Task 3:
x = find_x_with_probability_p(1 - 0.001)
"""
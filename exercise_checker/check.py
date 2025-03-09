from IPython.display import display
import ipywidgets as widgets
from math import isclose

def check(f):
	def wrapper(*args, **kwargs):
		output = widgets.Output()
		button = widgets.Button(description="Check Answer(s)")
		@output.capture(clear_output=True,wait=True)
		def _inner_check(button):
			try:	
				f(*args, **kwargs)
			except:
				print("Something went wrong, have you filled all the functions and run the cells?")
		button.on_click(_inner_check)
		display(button, output)
	return wrapper

@check
def check_exercise(glob, ex):
    check_float = lambda a, b: isclose(a, b, rel_tol=0, abs_tol=ex["tolerance"])
    check_string = lambda a,b: a == b
    check_type = lambda a, types: any(isinstance(a, t) for t in types)
    
    if not ex:
        print("Empty exercise.")
        return

    elif ex["type"] == "values":

        # Initialize result as an empty list
        result = []
        for i in range(len(ex["values"])):
            # Access global variables dynamically
            result.append(glob[ex["variables"][i]])
        for j in range(len(result)):
            # Check if the values match within tolerance
            if check_float(result[j], ex["values"][j]):
                print(f"You got the parameter '{ex['variables'][j]}' right, well done! (checked with tolerance {ex['tolerance']})")
            else:
                print(f"The parameter '{ex['variables'][j]}' is incorrect. {result[j]} (checked with tolerance {ex['tolerance']})")
                print("          Other parts won't be graded until these are fixed.")
                return
            
    elif ex["type"] == "function":
        function = glob[ex["name"]]
	
        tests = ex["tests"]
        failed = []

        for x, out in tests:
            result = function(x)
            if not check_float(result, out):
                failed.append((x, out, result))

        if len(failed) == 0:
            print(f"Well done, your function is correct! (checked with tolerance {ex['tolerance']})")	
        else:
            print(f"Your function failed some tests. Keep in mind the tolerance is {ex['tolerance']}")
            print("    --> Failed inputs:")
            for case in failed:
                print(f"{case[0]} gave {case[2]}, expected {case[1]}")
            print(f"      Other parts won't be graded until these are fixed.")
            return
        
    elif ex["type"] == "strings":

        # Initialize string as an empty list
        result = []
        for i in range(len(ex["values"])):
            # Access global variables dynamically
            result.append(glob[ex["variables"][i]])
            
            # Check if the strings match
            if check_string(result[i], ex["values"][i]):
                print(f"You got the string '{ex['variables'][i]}' right, well done!")
            else:
                print(f"The string '{ex['variables'][i]}' is incorrect.")
                print("          Ensure proper capitalization is used where necessary.")
                print("          Other parts won't be graded until these are fixed.")
                return
            
    elif ex["type"] == "values_type":
        
        for i in range(len(ex["variables"])):
            var_name = ex["variables"][i]
            expected_type = ex["values_type"][i]  # This should store actual type objects like int, str, float, etc.
            actual_value = glob[var_name]

            # Ensure expected_types is a list (handle cases where it's a single type like int)
            expected_type = expected_type if isinstance(expected_type, list) else [expected_type]

            if check_type(actual_value, expected_type):
                print(f"The type of '{var_name}' is correct, well done!")
            else:
                expected_type_str = ', '.join(t.__name__ for t in expected_type)
                print(f"The type of '{var_name}' is incorrect. Expected {expected_type_str}, but got {type(actual_value).__name__}.")
                print("          Other parts won't be graded until these are fixed.")
                return
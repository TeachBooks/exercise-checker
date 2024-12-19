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
def check_example(glob, dict):
    check_float = lambda a, b: isclose(a, b, rel_tol=0, abs_tol=dict["tolerance"])
    check_string = lambda a,b: a == b
    
    if not dict:
        print("Empty exercise.")
        return

    elif dict["type"] == "values":

        # Initialize result as an empty list
        result = []
        for i in range(len(dict["values"])):
            # Access global variables dynamically
            result.append(glob[dict["variables"][i]])
            
            # Check if the values match within tolerance
            if check_float(result[i], dict["values"][i]):
                print(f"You got the parameter '{dict['variables'][i]}' right, well done! (checked with tolerance {dict['tolerance']})")
            else:
                print(f"The parameter '{dict['variables'][i]}' is incorrect. (checked with tolerance {dict['tolerance']})")
                print("          Other parts won't be graded until these are fixed.")
                return
            
    elif dict["type"] == "function":
        function = glob[dict["name"]]
	
        test_inputs = dict["inputs"]
        failed = []

        for x, out in test_inputs:
            result = function(x)
            if not check_float(result, out):
                failed.append((x, out, result))

        if len(failed) == 0:
            print(f"Well done, your function is correct! (checked with tolerance {dict['tolerance']})")	
        else:
            print(f"Your function failed some tests. Keep in mind the tolerance is {dict['tolerance']}")
            print("    --> Failed inputs:")
            for case in failed:
                print(f"{case[0]} gave {case[2]}, expected {case[1]}")
            print(f"      Other parts won't be graded until these are fixed.")
            return
        
    elif dict["type"] == "strings":

        # Initialize string as an empty list
        result = []
        for i in range(len(dict["values"])):
            # Access global variables dynamically
            result.append(glob[dict["variables"][i]])
            
            # Check if the strings match
            if check_string(result[i], dict["values"][i]):
                print(f"You got the string '{dict['variables'][i]}' right, well done!")
            else:
                print(f"The string '{dict['variables'][i]}' is incorrect.")
                print("          Ensure proper capitalization is used where necessary.")
                print("          Other parts won't be graded until these are fixed.")
                return
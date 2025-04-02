from IPython.display import display
import ipywidgets as widgets
from math import isclose

def check(f):
    """
    A decorator that wraps a function to provide a button and output widget for checking answers.

    Parameters
    ----------
    f : function
        The function to be wrapped.

    Returns
    -------
    function
        The wrapped function with a button and output widget.
    """
    def wrapper(*args, **kwargs):
        output = widgets.Output()
        button = widgets.Button(description="Check Answer(s)")
        @output.capture(clear_output=True, wait=True)
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
    """
    Checks the exercise based on the provided global variables and exercise specifications.

    Parameters
    ----------
    glob : dict
        A dictionary containing the global variables.
    ex : dict
        A dictionary containing the exercise specifications. It should have the following keys:
        - type : str
            The type of exercise. Can be "values", "function", "strings", or "values_type".
        - tolerance : float, optional
            The tolerance for checking float values (only for "values" and "function" types).
        - variables : list of str, optional
            The list of variable names to check (only for "values" and "strings" types).
        - values : list, optional
            The list of expected values (only for "values" and "strings" types).
        - name : str, optional
            The name of the function to check (only for "function" type).
        - tests : list of tuples, optional
            The list of test cases for the function (only for "function" type).
        - values_type : list of types, optional
            The list of expected types for the variables (only for "values_type" type).

    Returns
    -------
    None
    """
    check_float = lambda a, b, c: isclose(a, b, rel_tol=0, abs_tol = c)
    check_float_limits = lambda a, c: a >= c[0] and a <= c[1]
    check_string = lambda a, b: a == b
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
            if isinstance(ex["tolerance"], (int, float)):
                if check_float(result[j], ex["values"][j], ex["tolerance"]):
                    print(f"You got the parameter '{ex['variables'][j]}' right, well done! (checked with tolerance {ex['tolerance']})")
                else:
                    print(f"The parameter '{ex['variables'][j]}' is incorrect. {result[j]} (checked with tolerance {ex['tolerance']})")
                    print("          Other parts won't be graded until these are fixed.")

            elif ex["tolerance"]["type"] == "absolute":
                tolerance_value = ex["tolerance"]["value"][j] if isinstance(ex["tolerance"]["value"], list) else ex["tolerance"]["value"]
                if check_float(result[j], ex["values"][j], tolerance_value):
                    print(f"You got the parameter '{ex['variables'][j]}' right, well done! (checked with absolute tolerance {tolerance_value})")
                else:
                    print(f"The parameter '{ex['variables'][j]}' is incorrect. {result[j]} (checked with absolute tolerance {tolerance_value})")
                    print("          Other parts won't be graded until these are fixed.")

            elif ex["tolerance"]["type"] == "limits":
                # Ensure tolerance_limits is a tuple for each variable
                tolerance_limits = ex["tolerance"]["value"][j] if isinstance(ex["tolerance"]["value"][0], (list, tuple)) else ex["tolerance"]["value"]
                if check_float_limits(result[j], tolerance_limits):
                    print(f"You got the parameter '{ex['variables'][j]}' right, well done! (checked with limits {tolerance_limits})")
                else:
                    print(f"The parameter '{ex['variables'][j]}' is incorrect. {result[j]} (checked with limits {tolerance_limits})")
                    print("          Other parts won't be graded until these are fixed.")
            
            else:
                print("Unknown tolerance type. Please check the exercise specification.")
                return
            
    elif ex["type"] == "function":
        function = glob[ex["name"]]
    
        tests = ex["tests"]
        failed = []

        for x, out in tests:
            result = function(x)
            if not check_float(result, out, ex["tolerance"]):
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
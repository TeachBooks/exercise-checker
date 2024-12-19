from IPython.display import display
import ipywidgets as widgets

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
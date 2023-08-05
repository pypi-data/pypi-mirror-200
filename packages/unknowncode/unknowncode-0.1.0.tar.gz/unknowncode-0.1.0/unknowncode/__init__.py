__version__ = '0.1.0'

def yes_no(prompt):
  allowed_responses = {"Yes","yes","Y","y"}
  yes_no_input = input(prompt)
  if yes_no_input in allowed_responses:
    return True
  else:
    return False
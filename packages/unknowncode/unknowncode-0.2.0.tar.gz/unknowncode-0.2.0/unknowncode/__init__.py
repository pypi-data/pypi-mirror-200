__version__ = '0.2.0'

def custom_response(response_list,cap_sense,prompt)
  allowed_responses = response_list
  input = input(prompt)
if cap_sense == False:
  if input.casefold() in allowed_responses:
    return True
  else:
    return False
else:
  if input in allowed_responses:
    return True
  else:
    return False

def yes_no(prompt):
  allowed_responses = {"Yes","yes","Y","y"}
  input = input(prompt)
  if input.casefold() in allowed_responses:
    return True
  else:
    return False




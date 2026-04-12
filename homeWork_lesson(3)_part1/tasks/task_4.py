text_input: str = "hhhabchghhh"

first_h = text_input.find('h')
last_h = text_input.rfind('h')

text_replace_output = (
    text_input[:first_h + 1]
    + text_input[first_h + 1:last_h].replace('h', 'H')
    + text_input[last_h:]
)

print(f"Измененный текст: {text_replace_output}")
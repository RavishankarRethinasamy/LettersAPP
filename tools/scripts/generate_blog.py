import string
import random
from pdb import set_trace as bp

LINES = 100
LINE_LENGTH = 50

def generate_content():
    content = ""
    i = True 
    while i:
        new_line = "".join(random.choices(string.ascii_letters, k=LINE_LENGTH))
        new_line = new_line + "/n"
        content = content + new_line  
        i += 1
        if i == LINES:
            break
    return content

test_path = "/opt/core/Letters/resources/test" + "/test_blog.txt"

content = generate_content()

print(content)

with open(test_path, "w") as tw:
    tw.write(content)
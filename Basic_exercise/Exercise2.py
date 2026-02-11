text = "  Hello, World! Welcome to Python Programming.  "
text_strip = text.strip()
print("Stripped: ", text_strip)

new_text = text.split()
print("Number of words: ", len(new_text))
print("Title case: ", text.title())
print("Starts with Hello: ", text_strip.startswith("Hello"))
print("Ends with ing. : ", text_strip.endswith("ing."))
print("Python position: ", text_strip.find("Python"))
print("Joined: "," - ".join(new_text))
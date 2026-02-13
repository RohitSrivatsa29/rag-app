from thefuzz import process, fuzz

print("Import successful")
choices = ["Sundar Pichai", "Satya Nadella"]
print(process.extractOne("sundar picai", choices))

import bcrypt

print("la1")

password = "new"
hashed = bcrypt.hashpw(password('utf-8'), bcrypt.gensalt())
print("la")
print(hashed)

# if bcrypt.checkpw(password, hashed):
#     print("It Matches!")
# else:
#     print("It Does not Match :(")

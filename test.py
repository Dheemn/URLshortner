uname = None
password = None
garba = ""

if uname is None:
    uname = "Rando"
if not password:
    password = "password"
if not (garba := str(input("Enter something: "))):
    garba = "bjad"

print("Enter the name of the database you want to give. " +
      "Press ENTER for default(Default is database): ")

print("sudo -u postgres psql -c 'create user uname with encrypted " +
      f"password {password}' {garba}s")

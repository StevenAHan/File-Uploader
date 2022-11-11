from app import db, files
with open("./files/README_(Do_not_delete_please).txt", "rb") as file:
  file = files(file_name = "README_(Do_not_delete_please).txt", file_blob = file.read())
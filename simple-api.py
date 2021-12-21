from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

con = sqlite3.connect('myDatabase.db')
cursorObj = con.cursor()


jj = 234
search_tovara = "SELECT prod_link FROM Cards where id = ?"
cursorObj.execute(search_tovara, (jj,))

f=''
for row in cursorObj.fetchall():
    f = row 
h= " , " .join(f)
aa= '-'.join(h.split('-')[:-1])

search_first_img_tovara = "SELECT image_link FROM Cards where prod_link = ?"
cursorObj.execute(search_first_img_tovara,(h,))
picfer =''
for row in cursorObj.fetchall():
    picfer = row 

search_all_tovarov = "SELECT prod_link FROM Cards where prod_link LIKE ?"
cursorObj.execute(search_all_tovarov,(aa+'%',))
fff=cursorObj.fetchall()


search_all_img_tovarov = "SELECT image_link FROM Cards where prod_link LIKE ?"
cursorObj.execute(search_all_img_tovarov,(aa+'%',))
pic = cursorObj.fetchall()








origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/request/")
def request(name: int = Form(...), first: str = Form(h), img_ferst: str = Form(picfer),  ff: str = Form(fff), image: str = Form(pic)):
    return {"username": name, "first": first, "img_ferst": img_ferst ,  "ff": ff, "image": image }
   



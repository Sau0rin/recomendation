from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/request/")
def request(name: str = Form(...)):

    con = sqlite3.connect('myDatabase.db')
    cursorObj = con.cursor()

    search_tovara = "SELECT prod_link FROM Cards where id = ?"
    cursorObj.execute(search_tovara, (name,))

    f=''
    for row in cursorObj.fetchall():
        f = row 
    h= " , " .join(f)
    aa= '-'.join(h.split('-')[:-1])

    search_first_img_tovara = "SELECT image_link FROM Cards where prod_link = ?"
    cursorObj.execute(search_first_img_tovara,(h,))
    img_ferst =''
    for row in cursorObj.fetchall():
        img_ferst = row 

    search_all_tovarov = "SELECT prod_link FROM Cards where prod_link LIKE ?"
    cursorObj.execute(search_all_tovarov,(aa+'%',))
    ff=cursorObj.fetchall()


    search_all_img_tovarov = "SELECT image_link FROM Cards where prod_link LIKE ?"
    cursorObj.execute(search_all_img_tovarov,(aa+'%',))
    image = cursorObj.fetchall()

    return {"username": name, "first": h, "img_ferst": img_ferst ,  "ff": ff, "image": image }
   



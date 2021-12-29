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

    con = sqlite3.connect('myDatabase11.db')
    cursorObj = con.cursor()

    search_tovara = "SELECT prod_link FROM Cards where artikul = ?"
    cursorObj.execute(search_tovara, (name,))

    link=''
    for row in cursorObj.fetchall():
        link = row 
    link_str= " , " .join(link)
    link_str_split= '-'.join(link_str.split('-')[:-1])

    search_first_img_tovara = "SELECT image_link FROM Cards where prod_link = ?"
    cursorObj.execute(search_first_img_tovara,(link_str,))
    img_ferst =''
    for row in cursorObj.fetchall():
        img_ferst = row 

    search_all_tovarov = "SELECT prod_link FROM Cards where prod_link LIKE ?"
    cursorObj.execute(search_all_tovarov,(link_str_split+'%',))
    similar_link=cursorObj.fetchall()


    search_all_img_tovarov = "SELECT image_link FROM Cards where prod_link LIKE ?"
    cursorObj.execute(search_all_img_tovarov,(link_str_split+'%',))
    image = cursorObj.fetchall()



    return {"username": name, "first": link_str, "img_ferst": img_ferst ,  "similar_link": similar_link, "image": image }
   



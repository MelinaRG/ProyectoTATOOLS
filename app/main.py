import uvicorn
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from scripts.db_postgres import create_user
from scripts.db_postgres import conn
from scripts.db_postgres import get_asistencia
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })

#COPIERINO
@app.get("/asistencia", response_class=HTMLResponse)
async def asistenciax(request:Request):
    return templates.TemplateResponse('asistencia.html',{
        "request": request,
        "alumnos": get_asistencia()
    })
#HASTA ACA

@app.get("/login", response_class=HTMLResponse)
async def loginx(request: Request):
    return templates.TemplateResponse("login.html",{
        "request": request
        })

@app.get("/juegos", response_class=HTMLResponse)
async def juegos(request: Request):
    return templates.TemplateResponse("juegos.html",{
        "request": request
        })

@app.get("/temas", response_class=HTMLResponse)
async def temas(request: Request):
    return templates.TemplateResponse("temas.html",{
        "request": request
        })

@app.post("/add_contact", response_class=HTMLResponse)
async def post_form (request: Request, 
            grupo_sup: int = Form(...),
            nombre: str = Form(...),
            apellido: str = Form(...),
            edad: int = Form(...),
            email: str = Form(...),
            nacionalidad: str = Form(...),
            pais_residencia: str = Form(...),
            ocupacion: str = Form(...),
            dispositivo: str = Form(...),
            mic_y_cam: str = Form(...),
            funcion_sup: str = Form(...),
            gustos_sup: str = Form(...),):

            lista = []

            lista.append(grupo_sup)
            lista.append(nombre)
            lista.append(apellido)
            lista.append(edad)
            lista.append(email)
            lista.append(nacionalidad)
            lista.append(pais_residencia)
            lista.append(ocupacion)
            lista.append(dispositivo)
            lista.append(mic_y_cam)
            lista.append(funcion_sup)
            lista.append(gustos_sup)

            create_user(lista)

            return 'Gracias por responder'



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    nombre: str
    apellido: str


def fake_decode_token(token):

    cursor = conn.cursor()
    
    cursor.execute("SELECT id_sup FROM ta_test_fede WHERE email =%s", (token,))
    
    result = cursor.fetchone()
    
    cursor.close()
    
    if result:
        return result
    else:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/ingreso_usuario")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  
    cursor = conn.cursor()
    
   
    cursor.execute("SELECT * FROM ta_test_fede WHERE email=%s AND apellido=%s", (form_data.username, form_data.password))
    
    result = cursor.fetchone()
    

    if result:
        return {"access_token": form_data.username, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


if __name__ == '__main__':
    uvicorn.run(app, port=80)



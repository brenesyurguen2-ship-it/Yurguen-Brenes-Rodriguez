from flask import Flask, render_template, request, redirect
import json, os, uuid



app = Flask(__name__)


if not os.path.exists("datos.json"):
    with open("datos.json", "w", encoding="utf-8") as archivo:
        json.dump([], archivo)


@app.route("/", methods=["GET","POST"])
def inicio():

    if request.method == "POST":

        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        edad = request.form["edad"]
        seccion = request.form["seccion"]
        especialidad = request.form["especialidad"] 

        nuevo_registro = {
            "id": str(uuid.uuid4()),
            "nombre": nombre,
            "apellido": apellido,
            "edad": edad,
            "seccion": seccion,
            "especialidad": especialidad
        }

        with open("datos.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        datos.append(nuevo_registro)

        with open("datos.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    with open("datos.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return render_template("index.html", datos=datos)


@app.route("/eliminar/<id>")
def eliminar(id):

    with open("datos.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    datos = [estudiante for estudiante in datos if estudiante["id"] != id]

    with open("datos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    return redirect("/")
    


@app.route("/editar/<id>")
def editar(id):

    with open("datos.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    estudiante_editar = None

    for estudiante in datos:

        if estudiante["id"] == id:
            estudiante_editar = estudiante
            break


    # quitar remporalmente
    datos = [e for e in datos if e["id"] != id]

    with open("datos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    
    return render_template("index.html", datos=datos, estudiante_editar=estudiante_editar)


if __name__ == "__main__":
    app.run(debug=True)
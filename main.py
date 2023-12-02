import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    jsonify,
    send_from_directory,
)
from flask import redirect, url_for
from controlador.ClienteController import ClienteController
from controlador.HotelController import HotelController
from clase.Cliente import Cliente
from clase.Hotel import Hotel
from clase.Habitacion import Habitacion
from controlador.HabitacionController import HabitacionController
from clase.LugarTuristico import LugarTuristico
from controlador.LugarTuristicoController import LugarTuristicoController

from clase.Reserva import Reserva
from controlador.ReservaController import ReservaController

from controlador.LugarTuristicoController import LugarTuristicoController
from werkzeug.utils import secure_filename
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
import bcrypt
import traceback
import base64
import os

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "Dios"  # Cambia esto con una clave secreta más segura
app.secret_key = (
    "Dios"  # Agrega esta línea para establecer la clave secreta de la sesión
)
jwt = JWTManager(app)

UPLOAD_FOLDER = "image"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/imagen/<path:filename>")
def mostrar_imagen(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/api_login", methods=["POST"])
def api_login():
    try:
        p_dni = request.json.get("dni")
        password = request.json.get("password")
        usuario = ClienteController.validar_credenciales(p_dni, password)
        if usuario:
            # Generar un token JWT
            token = create_access_token(identity=usuario["id"])
            return jsonify(
                {
                    "Estado": True,
                    "Mensaje": "Inicio de sesión exitoso",
                    "Usuario": usuario,
                    "token": token,
                }
            )
        else:
            return jsonify({"Estado": False, "Mensaje": "Credenciales incorrectas"})
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_obtener_clientes")
@jwt_required()
def api_obtener_clientes():
    try:
        clientes = ClienteController.obtener_clientes()
        listaserializable = []

        for cliente_data in clientes:
            if len(cliente_data) == 6:
                cliente = Cliente(*cliente_data)
            else:
                cliente = Cliente(*(cliente_data + (None,)))
            listaserializable.append(cliente.midic.copy())

        return jsonify({"Estado": True, "Mensaje": "OK", "Datos": listaserializable})
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


# registro de reserva


@app.route("/api_guardar_reserva", methods=["POST"])
def api_guardar_reserva():
    try:
        # Obtener datos del cuerpo de la solicitud en formato JSON
        data = request.json
        # Extraer datos del JSON
        p_id = data.get("id")
        p_cliente_id = data.get("cliente_id")
        p_habitacion_id = data.get("habitacion_id")
        p_fecha_inicio = data.get("fecha_inicio")
        p_fecha_fin = data.get("fecha_fin")
        p_estado = data.get("estado")
        # Insertar reserva utilizando el controlador
        ReservaController.insertar_reserva(
            p_id, p_cliente_id, p_habitacion_id, p_fecha_inicio, p_fecha_fin, p_estado
        )
        # Retornar una respuesta exitosa en formato JSON
        return jsonify({"Estado": True, "Mensaje": "Reserva registrada correctamente"})
    except Exception as e:
        # Retornar un mensaje de error en caso de excepción
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_listar_reservas_por_cliente/<int:cliente_id>", methods=["GET"])
def api_listar_reservas_por_cliente(cliente_id):
    try:
        # Obtener reservas por cliente utilizando el controlador
        reservas = ReservaController.obtener_reservas_por_cliente(cliente_id)

        # Retornar la lista de reservas en formato JSON
        return jsonify({"Estado": True, "Reservas": reservas})
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_guardar_cliente", methods=["POST"])
def api_guardar_cliente():
    try:
        # Obtener datos del cuerpo de la solicitud en formato JSON
        data = request.json
        # Extraer datos del JSON
        p_nombre = data.get("nombre")
        p_apellido = data.get("apellido")
        p_dni = data.get("dni")
        p_lugar_procedencia = data.get("lugar_procedencia")
        p_password = data.get("password")
        # Insertar cliente utilizando el controlador
        ClienteController.insertar_cliente(
            p_nombre, p_apellido, p_dni, p_lugar_procedencia, p_password
        )
        # Retornar una respuesta exitosa en formato JSON
        return jsonify({"Estado": True, "Mensaje": "Cliente registrado correctamente"})
    except Exception as e:
        # Retornar un mensaje de error en caso de excepción
        return jsonify({"Estado": False, "Mensaje": str(e)})


# planbtilla HTML
@app.route("/api_guardar_clienteplantilla", methods=["POST"])
def api_guardar_clienteplantilla():
    try:
        p_nombre = request.form["nombre"]
        p_apellido = request.form["apellido"]
        p_dni = request.form["dni"]
        p_lugar_procedencia = request.form["lugar_procedencia"]
        p_password = request.form["password"]
        ClienteController.insertar_cliente(
            p_nombre, p_apellido, p_dni, p_lugar_procedencia, p_password
        )
        # Redirigir a la pantalla principal
        return redirect(url_for("listadoclientes"))
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_eliminar_cliente", methods=["POST"])
def api_eliminar_cliente():
    try:
        ClienteController.eliminar_cliente(request.json["id"])
        return jsonify({"Estado": True, "Mensaje": "Cliente eliminado correctamente"})

    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_eliminar_clientePlantilla", methods=["POST"])
def api_eliminar_cliente_plantilla():
    try:
        ClienteController.eliminar_cliente(request.form["id"])
        return redirect(url_for("listadoclientes"))
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_actualizar_cliente", methods=["POST"])
def api_actualizar_cliente():
    try:
        p_id = request.json["id"]
        p_nombre = request.json["nombre"]
        p_apellido = request.json["apellido"]
        p_dni = request.json["dni"]
        p_lugar_procedencia = request.json["lugar_procedencia"]

        ClienteController.actualizar_cliente(
            p_id, p_nombre, p_apellido, p_dni, p_lugar_procedencia
        )

        return jsonify({"Estado": True, "Mensaje": "Cliente actualizado correctamente"})

    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_obtener_cliente/<int:id>")
def api_obtener_cliente(id):
    try:
        cliente = ClienteController.obtener_cliente_por_id(id)
        listaserializable = []

        miobj = ClienteController(
            cliente[0], cliente[1], cliente[2], cliente[3], cliente[4]
        )
        listaserializable.append(miobj.midic.copy())

        return jsonify({"Estado": True, "Mensaje": "OK", "Datos": listaserializable})

    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/")
@app.route("/index")
def obtener_clientes():
    return render_template("index.html")


@app.route("/listadoclientes")
def listadoclientes():
    # Lógica para obtener datos si es necesario
    clientes = ClienteController.obtener_clientes()
    return render_template("listadoclientes.html", clientes=clientes)


@app.route("/formulario_agregar_cliente")
def formulario_agregar_cliente():
    # Lógica para manejar el formulario de agregar cliente
    return render_template("agregar_Cliente.html")


@app.route("/editar_cliente/<int:id>")
def editar_cliente(id):
    # Logic to retrieve client information by ID
    cliente = ClienteController.obtener_cliente_por_id(id)
    return render_template("editar_cliente.html", cliente=cliente)


@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_cliente():
    try:
        # Logic to delete a client using the request data
        ClienteController.eliminar_cliente(request.json["id"])
        return jsonify({"Estado": True, "Mensaje": "Cliente eliminado correctamente"})
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_actualizar_cliente_y_redirigir/<int:id>", methods=["POST"])
def api_actualizar_cliente_y_redirigir(id):
    try:
        p_id = id
        p_nombre = request.form["nombre"]
        p_apellido = request.form["apellido"]
        p_dni = request.form["dni"]
        p_lugar_procedencia = request.form["lugar_procedencia"]

        ClienteController.actualizar_cliente(
            p_id, p_nombre, p_apellido, p_dni, p_lugar_procedencia
        )

        flash("Cliente actualizado correctamente", "success")
        return redirect(url_for("listadoclientes"))
    except Exception as e:
        flash(f"Error al actualizar el cliente: {str(e)}", "error")
        return redirect(url_for("editar_cliente", id=id))


# HOTEL
@app.route("/api_guardar_hotel", methods=["POST"])
def api_guardar_hotel():
    try:
        # Obtener datos del formulario
        p_nombre = request.form["nombre"]
        p_ubicacion = request.form["ubicacion"]
        p_ruc = request.form["ruc"]
        p_descripcion = request.form["descripcion"]
        # Verificar si se ha enviado un archivo
        if "imagen" in request.files:
            imagen = request.files["imagen"]
            # Verificar si el archivo tiene un nombre
            if imagen.filename != "":
                # Generar un nombre seguro para el archivo
                nombre_seguro = secure_filename(imagen.filename)
                # Guardar la imagen en la carpeta designada
                ruta_guardado = os.path.join(app.config["UPLOAD_FOLDER"], nombre_seguro)
                imagen.save(ruta_guardado)

                # Insertar el hotel en la base de datos con el nombre de la imagen
                HotelController.insertar_hotel(
                    p_nombre, p_ubicacion, p_ruc, p_descripcion, nombre_seguro
                )

        return jsonify({"Estado": True, "Mensaje": "Hotel registrado correctamente"})
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_guardar_hotel_template", methods=["POST"])
def api_guardar_hotel_template():
    # Obtener datos del formulario
    p_nombre = request.form["nombre"]
    p_ubicacion = request.form["ubicacion"]
    p_ruc = request.form["ruc"]
    p_descripcion = request.form["descripcion"]
    foto = request.files["foto"]
    if foto:
        # Generar un nombre único para el archivo
        nombre_archivo = secure_filename(foto.filename)
        ruta_guardado = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
        foto.save(ruta_guardado)
    else:
        nombre_archivo = "default.png"
    # Guardar la información del producto en la base de datos
    HotelController.insertar_hotel(
        p_nombre, p_ubicacion, p_ruc, p_descripcion, nombre_archivo
    )
    return redirect("/listadoHoteles")


@app.route("/api_actualizar_hotel/<int:id>", methods=["POST"])
def api_actualizar_hotel(id):
    try:
        # Obtener datos del formulario de edición
        p_nombre = request.form["nombre"]
        p_ubicacion = request.form["ubicacion"]
        p_ruc = request.form["ruc"]
        p_descripcion = request.form["descripcion"]

        # Verificar si se ha enviado una nueva imagen
        if "nueva_imagen" in request.files:
            nueva_imagen = request.files["nueva_imagen"]
            if nueva_imagen.filename != "":
                # Generar un nombre seguro para la nueva imagen
                nuevo_nombre_seguro = secure_filename(nueva_imagen.filename)
                # Guardar la nueva imagen en la carpeta designada
                nueva_ruta_guardado = os.path.join(
                    app.config["UPLOAD_FOLDER"], nuevo_nombre_seguro
                )
                nueva_imagen.save(nueva_ruta_guardado)
                # Actualizar la referencia de imagen en la base de datos
                HotelController.actualizar_hotel(
                    id, p_nombre, p_ubicacion, p_ruc, p_descripcion, nuevo_nombre_seguro
                )
        else:
            # Si no se proporciona una nueva imagen, actualizar sin cambiar la foto
            HotelController.actualizar_hotel(
                id, p_nombre, p_ubicacion, p_ruc, p_descripcion
            )

        return jsonify({"Estado": True, "Mensaje": "Hotel actualizado correctamente"})
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_obtener_hoteles")
# @jwt_required()
def api_obtener_hoteles():
    try:
        hoteles = HotelController.obtener_hoteles()
        listaserializable = []
        for hotel_data in hoteles:
            # Asegúrate de que hotel_data tenga al menos 6 elementos
            if len(hotel_data) >= 6:
                hotel = Hotel(*hotel_data)
                hotel_dict = hotel.midic.copy()
                listaserializable.append(hotel_dict)
            else:
                print(f"Datos insuficientes para hotel: {hotel_data}")
        return jsonify({"Estado": True, "Mensaje": "OK", "Datos": listaserializable})
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_eliminar_hotel", methods=["POST"])
def api_eliminar_hotel():
    try:
        HotelController.eliminar_hotel(request.json["id"])
        return jsonify({"Estado": True, "Mensaje": "Hotel eliminado correctamente"})
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_eliminar_hotelPlantilla", methods=["POST"])
def api_eliminar_hotelPlantilla():
    try:
        HotelController.eliminar_hotel(request.form["id"])
        return redirect(
            url_for("listadoHoteles")
        )  # Asegúrate de que el nombre sea correcto
    except Exception as e:
        return redirect(
            url_for("listadoHoteles")
        )  # Asegúrate de que el nombre sea correctoç


@app.route("/listado_lugares_turisticos")
def listado_lugares_turisticos():
    LugarTuristico = LugarTuristicoController.obtener_lugares_turisticos()
    return render_template("listaLugarTuristico.html", LugarTuristico=LugarTuristico)


@app.route("/api_eliminar_lugar_turistico_plantilla", methods=["POST"])
def api_eliminar_lugar_turistico_plantilla():
    if request.method == "POST":
        habitacion_id = request.form.get("id")
        LugarTuristicoController.eliminar_lugar_turistico(habitacion_id)
        # Redirigir al listado de habitaciones después de la eliminación
    return redirect(url_for("listado_lugares_turisticos"))


@app.route("/formulario_agregar_lugar_turistico")
def formulario_agregar_lugar_turistico():
    # Lógica para manejar el formulario de agregar cliente
    return render_template("formulario_agregar_lugar_turistico.html")


@app.route("/api_guardar_lugar_turistico_template", methods=["POST"])
def api_guardar_lugar_turistico_template():
    try:
        # Obtener los datos del formulario
        nombre = request.form.get("nombre")
        ubicacion = request.form.get("ubicacion")
        descripcion = request.form.get("descripcion")
        foto = request.files.get("foto")
        if foto:
            # Generar un nombre único para el archivo
            nombre_archivo = secure_filename(foto.filename)
            ruta_guardado = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
            foto.save(ruta_guardado)
        else:
            nombre_archivo = "default.png"

        # Usar el nombre de la foto como argumento
        LugarTuristicoController.insertar_lugar_turistico(
            p_nombre=nombre,
            p_descripcion=descripcion,
            p_ubicacion=ubicacion,
            p_foto_url=nombre_archivo,  # Cambié el nombre del argumento aquí
        )

        # Después de procesar el formulario, redirige a la página de listado de lugares turísticos
        return redirect(url_for("listado_lugares_turisticos"))
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/listadoHoteles")
def listadoHoteles():
    # Lógica para obtener datos si es necesario
    hotel = HotelController.obtener_hoteles()
    return render_template("listadohoteles.html", hoteles=hotel)


@app.route("/formulario_agregar_hotel")
def formulario_agregar_hotel():
    return render_template("agregar_hotel.html")


@app.route("/Api_guardarHabitacionGet", methods=["POST"])
def Api_guardarHabitacionGet():
    try:
        # Extraer los campos necesarios del formulario
        hotel_id = request.form.get("hotel_id")
        numero = request.form.get("numero")
        tipo = request.form.get("tipo")
        precio = request.form.get("precio")
        foto = request.files.get("foto")
        if foto:
            # Generar un nombre único para el archivo
            nombre_archivo = secure_filename(foto.filename)
            ruta_guardado = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
            foto.save(ruta_guardado)
        else:
            nombre_archivo = "default.png"
        HabitacionController.insertar_habitacion(
            numero, tipo, precio, hotel_id, nombre_archivo
        )
        response = {"mensaje": "Habitación guardada correctamente"}
        return jsonify(response), 200

    except Exception as e:
        # Manejar errores, por ejemplo, si no se pueden obtener los datos correctamente
        response = {"error": str(e)}
        return jsonify(response), 500


@app.route("/api_guardar_habitacionPlantilla", methods=["POST"])
def api_guardar_habitacionPlantilla():
    try:
        # Extraer los campos necesarios del formulario
        hotel_id = request.form.get("hotel_id")
        numero = request.form.get("numero")
        tipo = request.form.get("tipo")
        precio = request.form.get("precio")
        foto = request.files.get("foto")
        if foto:
            # Generar un nombre único para el archivo
            nombre_archivo = secure_filename(foto.filename)
            ruta_guardado = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
            foto.save(ruta_guardado)
        else:
            nombre_archivo = "default.png"
        HabitacionController.insertar_habitacion(
            numero, tipo, precio, hotel_id, nombre_archivo
        )
        return redirect(url_for("listadoHabitaciones", hotel_id=hotel_id))

    except Exception as e:
        # Manejar errores, por ejemplo, si no se pueden obtener los datos correctamente
        response = {"error": str(e)}
        return jsonify(response), 500


@app.route("/formulario_agregar_habitacion/<int:hotel_id>", methods=["GET", "POST"])
def formulario_agregar_habitacion(hotel_id):
    return render_template("formulario_agregar_habitacion.html", hotel_id=hotel_id)


@app.route("/editar_habitacion/<int:id>", methods=["GET", "POST"])
def editar_habitacion(id):
    # Obtener la habitación a editar desde la base de datos
    habitacion = HabitacionController.obtener_habitacion_por_id(id)

    if request.method == "POST":
        # Procesar el formulario enviado
        numero = request.form.get("numero")
        tipo = request.form.get("tipo")
        precio = request.form.get("precio")

        # Realizar la actualización en la base de datos
        HabitacionController.actualizar_habitacion(
            id, numero, tipo, precio, habitacion.hotel_id, habitacion.foto_url
        )

        # Redirigir a la lista de habitaciones del hotel
        return redirect(url_for("listadoHabitaciones", hotel_id=habitacion.hotel_id))

    # Renderizar la plantilla de edición con los datos de la habitación
    return render_template("editarhabitacion.html", habitacion=habitacion)


@app.route("/listado_habitaciones/<int:hotel_id>")
def listadoHabitaciones(hotel_id):
    # Lógica para obtener las habitaciones
    habitaciones = HabitacionController.obtener_habitaciones_por_hotel(hotel_id)

    # Renderiza la plantilla y pasa el hotel_id al contexto
    return render_template(
        "listadohabitaciones.html", habitaciones=habitaciones, hotel_id=hotel_id
    )


@app.route("/eliminar_habitacion", methods=["POST"])
def eliminar_habitacion():
    if request.method == "POST":
        habitacion_id = request.form.get("id")
        HabitacionController.eliminar_habitacion(habitacion_id)
        # Redirigir al listado de habitaciones después de la eliminación
        return redirect(url_for("listadoHabitaciones", hotel_id=1))


@app.route("/api_obtener_habitaciones_por_hotel/<int:hotel_id>")
def api_obtener_habitaciones_por_hotel(hotel_id):
    try:
        habitaciones = HabitacionController.obtener_habitaciones_por_hotel(hotel_id)
        if habitaciones:
            # Convertir la lista de habitaciones a un formato JSON
            habitaciones_json = [
                {
                    "id": habitacion[0],
                    "numero": habitacion[1],
                    "tipo": habitacion[2],
                    "precio": habitacion[3],
                    "hotel_id": habitacion[4],
                    "foto_url": habitacion[5],
                }
                for habitacion in habitaciones
            ]

            return jsonify(
                {"Estado": True, "Mensaje": "OK", "Datos": habitaciones_json}
            )
        else:
            return jsonify(
                {
                    "Estado": False,
                    "Mensaje": "No hay habitaciones para el hotel especificado",
                }
            )

    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


if __name__ == "__main__":
    app.run(host="localhost", debug=True)

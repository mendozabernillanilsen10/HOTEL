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
from datetime import date
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


@app.route("/editar_lugar_turistico/<int:id>", methods=["GET", "POST"])
def editar_lugar_turistico(id):
    lugar_turistico = LugarTuristicoController.obtener_lugar_turistico_por_id(id)

    if lugar_turistico is None:
        # Handle non-existing tourist location
        return jsonify({"error": "Tourist location not found"})

    if request.method == "GET":
        return render_template(
            "editar_lugar_turistico.html", lugar_turistico=lugar_turistico
        )
    elif request.method == "POST":
        try:
            # Process the editing form
            nombre = request.form.get("nombre")
            ubicacion = request.form.get("ubicacion")
            descripcion = request.form.get("descripcion")
            foto = request.files.get("imegHlugar")

            # Check if a new photo is provided
            if foto:
                # Generate a unique filename for the file

                nombre_archivo = secure_filename(foto.filename)
                ruta_guardado = os.path.join(
                    app.config["UPLOAD_FOLDER"], nombre_archivo
                )
                foto.save(ruta_guardado)

            else:
                # No new photo provided, keep the existing photo
                nombre_archivo = lugar_turistico[4]

            # Update the tourist location in the database
            LugarTuristicoController.actualizar_lugar_turistico(
                id, nombre, descripcion, ubicacion, nombre_archivo
            )

            # Redirect to the tourist locations listing after editing
            return redirect(url_for("listado_lugares_turisticos"))
        except Exception as e:
            return jsonify({"error": str(e)})


@app.route("/api_obtener_habitaciones_por_hotel/<int:hotel_id>")
@jwt_required()
def api_obtener_habitaciones_por_hotel(hotel_id):
    try:
        habitaciones = HabitacionController.obtener_habitaciones_por_hotel(hotel_id)
        if habitaciones:
            # Construir la URL base para las imágenes
            base_url = request.url_root + "imagen/"

            # Convertir la lista de habitaciones a un formato JSON con URL completa
            habitaciones_json = [
                {
                    "id": habitacion[0],
                    "numero": habitacion[1],
                    "tipo": habitacion[2],
                    "precio": habitacion[3],
                    "hotel_id": habitacion[4],
                    "foto_url": base_url + habitacion[5],  # Construir la URL completa
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


@app.route("/api_obtener_hoteles")
@jwt_required()
def api_obtener_hoteles():
    try:
        hoteles = HotelController.obtener_hoteles()

        # Serializar la lista de hoteles
        hoteles_serializados = []
        for hotel in hoteles:
            foto_nombre = hotel[5]
            foto_url = f"{request.url_root}imagen/{foto_nombre}"

            hotel_serializado = {
                "id": hotel[0],
                "nombre": hotel[1],
                "ubicacion": hotel[2],
                "ruc": hotel[3],
                "descripcion": hotel[4],
                "foto_url": foto_url,
            }
            hoteles_serializados.append(hotel_serializado)

        # Devolver la respuesta JSON con los datos serializados
        return jsonify({"Estado": True, "Mensaje": "OK", "Datos": hoteles_serializados})
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/optenerLugaresTuristicos")
@jwt_required()
def optenerLugaresTuristicos():
    try:
        lugares = LugarTuristicoController.obtener_lugares_turisticos()
        lugar_list = []

        for citas_data in lugares:
            foto_nombre = citas_data[4]
            foto_url = f"{request.url_root}imagen/{foto_nombre}"

            citas_dict = {
                "id": citas_data[0],
                "nombre": citas_data[1],
                "descripcion": citas_data[2],
                "ubicacion": citas_data[3],
                "foto_url": foto_url,
            }
            lugar_list.append(citas_dict)

        return jsonify({"Estado": True, "Mensaje": "OK", "Datos": lugar_list})

    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


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


@app.route("/api_guardar_reserva", methods=["POST"])
@jwt_required()
def api_guardar_reserva():
    try:
        # Obtener datos del cuerpo de la solicitud en formato JSON
        data = request.json
        # Extraer datos del JSON
        p_cliente_id = data.get("cliente_id")
        p_habitacion_id = data.get("habitacion_id")
        p_fecha_inicio = data.get("fecha_inicio")
        p_fecha_fin = data.get("fecha_fin")
        p_estado = data.get("estado")

        # Verificar disponibilidad antes de insertar la reserva
        if verificar_disponibilidad(p_habitacion_id, p_fecha_inicio, p_fecha_fin):
            # La habitación está disponible, proceder con la inserción
            ReservaController.insertar_reserva(
                p_cliente_id, p_habitacion_id, p_fecha_inicio, p_fecha_fin, p_estado
            )
            # Retornar una respuesta exitosa en formato JSON
            return jsonify(
                {"Estado": True, "Mensaje": "Reserva registrada correctamente"}
            )
        else:
            # La habitación no está disponible en ese período
            return jsonify(
                {
                    "Estado": False,
                    "Mensaje": "La habitación no está disponible en ese período",
                }
            )

    except Exception as e:
        # Retornar un mensaje de error en caso de excepción
        return jsonify({"Estado": False, "Mensaje": str(e)})


def verificar_disponibilidad(habitacion_id, fecha_inicio, fecha_fin):
    # Obtener las reservas para la habitación y período especificado
    reservas = ReservaController.obtener_reservas_por_habitacion_y_periodo(
        habitacion_id, fecha_inicio, fecha_fin
    )
    # Verificar si hay reservas que coincidan en el período
    return not reservas


@app.route("/api_listar_reservas_por_cliente/<int:cliente_id>", methods=["GET"])
@jwt_required()
def api_listar_reservas_por_cliente(cliente_id):
    try:
        # Obtener reservas por cliente utilizando el controlador
        reservas = ReservaController.obtener_reservas_por_cliente(cliente_id)

        # Transformar las reservas a un formato con nombres de columnas y fechas formateadas
        reservas_con_nombres = []
        for reserva in reservas:
            reserva_formateada = {
                "reserva_id": reserva[0],
                "cliente_id": reserva[1],
                "habitacion_id": reserva[2],
                "fecha_inicio": reserva[3].strftime("%Y-%m-%d"),
                "fecha_fin": reserva[4].strftime("%Y-%m-%d"),
                "estado": reserva[5],
                "habitacion_numero": reserva[6],
                "habitacion_tipo": reserva[7],
                "habitacion_precio": reserva[8],
                "hotel_nombre": reserva[9],
                "hotel_ubicacion": reserva[10],
            }
            reservas_con_nombres.append(reserva_formateada)

        # Retornar la lista de reservas en formato JSON
        return jsonify({"Estado": True, "Reservas": reservas_con_nombres})
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


@app.route("/api_actualizar_hotelTemplate/<int:id>", methods=["POST"])
def api_actualizar_hotelTemplate(id):
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
        return redirect(url_for("listadoHoteles"))
    except Exception as e:
        return redirect(url_for("listadoHoteles"))


# ... (importaciones y configuraciones anteriores) ...


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


@app.route("/editar_hotel/<int:id>", methods=["GET", "POST"])
def editar_hotel(id):
    hotel = HotelController.obtener_hotel_por_id(id)
    return render_template("editar_hotel.html", hotel=hotel)


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


@app.route("/editar_habitacion/<int:id>", methods=["GET", "POST"])
def editar_habitacion(id):
    habitacion = HabitacionController.obtener_habitacion_por_id(id)

    if request.method == "POST":
        # Lógica para actualizar los detalles de la habitación con los datos del formulario
        numero = request.form["numero"]
        tipo = request.form["tipo"]
        precio = request.form["precio"]

        # Manejo de la carga de la nueva imagen (si se proporciona)
        if "nueva_imagen" in request.files:
            nueva_imagen = request.files["nueva_imagen"]
            if nueva_imagen.filename != "":
                filename = secure_filename(nueva_imagen.filename)
                nueva_imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                habitacion.foto_url = filename

        # Lógica para actualizar los detalles de la habitación en la base de datos
        HabitacionController.actualizar_habitacion(
            id, numero, tipo, precio, habitacion.foto_url
        )

        # Redirigir a la página de listado de habitaciones después de la edición
        return redirect(
            url_for("listado_habitaciones_template", hotel_id=habitacion.hotel_id)
        )

    # Renderizar la plantilla de edición de habitación
    return render_template("editar_habitacion.html", habitacion=habitacion)


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
        return redirect(url_for("listado_habitaciones_template", hotel_id=hotel_id))

    except Exception as e:
        # Manejar errores, por ejemplo, si no se pueden obtener los datos correctamente
        response = {"error": str(e)}
        return jsonify(response), 500


@app.route("/formulario_agregar_habitacion/<int:hotel_id>", methods=["GET", "POST"])
def formulario_agregar_habitacion(hotel_id):
    return render_template("formulario_agregar_habitacion.html", hotel_id=hotel_id)


@app.route("/listado_habitaciones_template/<int:hotel_id>", methods=["GET", "POST"])
def listado_habitaciones_template(hotel_id):
    # Lógica para obtener las habitaciones
    habitaciones = HabitacionController.obtener_habitaciones_por_hotel(hotel_id)
    # Renderiza la plantilla y pasa el hotel_id al contexto
    return render_template(
        "listado_Habitaciones.html", habitaciones=habitaciones, hotel_id=hotel_id
    )


@app.route("/formulario_agregar_reserva/<cliente_id>", methods=["GET", "POST"])
def formulario_agregar_reserva(cliente_id):
    return redirect(url_for("listado_habitaciones_template", hotel_id=1))
    # Your view logic here


@app.route("/listado_reservas/<int:hotel_id>", methods=["GET", "POST"])
def listado_Reservas(hotel_id):
    reservas = ReservaController.obtener_reservas_por_hotel(hotel_id)
    return render_template("listadoreservas.html", reservas=reservas, hotel_id=hotel_id)


@app.route("/eliminar_habitacion", methods=["POST"])
def eliminar_habitacion():
    if request.method == "POST":
        habitacion_id = request.form.get("id")
        HabitacionController.eliminar_habitacion(habitacion_id)
        # Redirigir al listado de habitaciones después de la eliminación
        return redirect(url_for("listado_habitaciones_template", hotel_id=1))


if __name__ == "__main__":
    app.run(host="172.20.10.5", debug=True)

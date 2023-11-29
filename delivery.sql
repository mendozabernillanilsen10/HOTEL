-- Crear la tabla de clientes
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    lugar_procedencia VARCHAR(100) NOT NULL,
    password varchar(250) DEFAULT NULL
);

-- Crear la tabla de hoteles
CREATE TABLE hoteles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(255) NOT NULL,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    descripcion TEXT
);
-- Crear la tabla de habitaciones con campo de foto_url
CREATE TABLE habitaciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    hotel_id INT,
    foto_url VARCHAR(255), -- Añadido para la URL de la foto
    FOREIGN KEY (hotel_id) REFERENCES hoteles(id)
);
-- Crear la tabla de lugares turísticos con campo de foto_url
CREATE TABLE lugares_turisticos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    ubicacion VARCHAR(255) NOT NULL,
    foto_url VARCHAR(255) -- Añadido para la URL de la foto
);
-- Crear la tabla de reservas
CREATE TABLE reservas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT,
    habitacion_id INT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id)
);

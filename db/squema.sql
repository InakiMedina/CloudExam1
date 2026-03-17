CREATE TABLE Clients (
    id SERIAL PRIMARY KEY,
    rfc VARCHAR(13) UNIQUE NOT NULL,
    razon_social VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    comercial_name VARCHAR(255),
    telefono VARCHAR(20)
);

CREATE TABLE Addresses (
    id SERIAL PRIMARY KEY,
    domicilio TEXT NOT NULL,
    colonia VARCHAR(100),
    municipio VARCHAR(100),
    estado VARCHAR(100),
    address_type VARCHAR(20) -- 'FACTURACIÓN'/'ENVÍO'
);

CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50),
    base_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE SalesNotes (
    id SERIAL PRIMARY KEY,
    folio VARCHAR(50) UNIQUE NOT NULL,
    client_id INTEGER REFERENCES Clients(id),
    fac_address_id INTEGER REFERENCES Addresses(id), -- Store address
    send_address_id INTEGER REFERENCES Addresses(id), -- Client address
    total DECIMAL(10, 2) DEFAULT 0.00
);

CREATE TABLE NoteContent (
    id SERIAL PRIMARY KEY,
    note_id INTEGER REFERENCES SalesNotes(id),
    product_id INTEGER REFERENCES Products(id),
    unit_price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    total DECIMAL(10, 2) NOT NULL
);
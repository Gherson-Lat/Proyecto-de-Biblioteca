# Proyecto-de-Biblioteca
Arquitectura modular ,cada módulo es una unidad autónoma con sus propias dependencias

## 1. Clonar el repositorio
git clone https://github.com/Gherson-Lat/Proyecto-de-Biblioteca.git
cd Proyecto-de-Biblioteca

## 2. Obtener las ramas remotas
git fetch origin

## 3. Entrar a su rama específica

Alexis: git checkout dev/alexis

Achicaiza: git checkout dev/achicaiza

Pedro: git checkout dev/pedro

Slopez: git checkout dev/slopez

Camilo: git checkout dev/camilo

## 🐳 Ejecución con Docker (Recomendado)

Si prefieres no configurar un entorno virtual de Python ni instalar dependencias localmente, puedes levantar todo el proyecto con Docker.

### Requisitos previos
* Tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Pasos para iniciar el sistema

1. **Construir e iniciar los contenedores:**
   ```bash
   docker compose up --build


### Acceder a la aplicación:

Dashboard Principal: http://localhost:8000

Módulo de Préstamos: http://localhost:8000/loans/vista

Documentación interactiva (Swagger UI): http://localhost:8000/docs


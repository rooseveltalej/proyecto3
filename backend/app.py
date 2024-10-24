# Backend to insert professors and courses into SQLite using FastAPI
from fastapi import FastAPI, HTTPException, Query
from typing import List
import sqlite3
from pyswip import Prolog
import ast
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde el frontend
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)


db_file = 'scheduling.db'
prolog = Prolog()
prolog.consult('scheduling.pl')  # Ensure the Prolog file is loaded

# Helper function to execute queries from SQLite
def execute_query(query: str, params: tuple = ()): 
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Create tables if they do not exist
def create_tables():
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS professors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    id_number TEXT NOT NULL,
                    available_hours TEXT NOT NULL,
                    courses TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    credits INTEGER NOT NULL,
                    semester INTEGER NOT NULL
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Call the create_tables function to ensure tables are created
create_tables()

# Endpoint to insert professors into SQLite
@app.get("/insert_professors/")
def insert_professors():
    professors = [
    ("Quiros Oviedo Rocio", "12345678", "['monday_7_11', 'wednesday_12_4', 'friday_7_11']", "['elementos_de_computacion', 'introduccion_a_la_programacion', 'bases_de_datos_i']"),
    ("Solis Parajeles Jonathan", "23456789", "['tuesday_12_4', 'thursday_7_11', 'monday_7_11']", "['analisis_y_diseno_de_algoritmos', 'estructuras_de_datos', 'taller_de_programacion']"),
    ("Gomez Rodriguez Luis Diego", "34567890", "['monday_12_4', 'friday_7_11', 'wednesday_7_11']", "['fundamentos_de_organizacion_de_computadoras', 'arquitectura_de_computadores', 'redes']"),
    ("Valerio Solis Lorena", "45678901", "['wednesday_7_11', 'thursday_7_11', 'tuesday_12_4']", "['taller_de_programacion', 'programacion_orientada_a_objetos', 'analisis_de_algoritmos']"),
    ("Zamora Cardenas Willard", "56789012", "['monday_7_11', 'thursday_12_4', 'wednesday_12_4']", "['bases_de_datos_i', 'bases_de_datos_ii', 'introduccion_a_la_programacion']"),
    ("Viquez Acuna Leonardo", "67890123", "['tuesday_7_11', 'friday_7_11', 'wednesday_12_4']", "['lenguajes_de_programacion', 'compiladores_e_interpretes', 'proyecto_de_ingenieria_de_software']"),
    ("Solis Chacon Henry Emanuelle", "78901234", "['monday_7_11', 'wednesday_12_4', 'friday_12_4']", "['requerimientos_de_software', 'diseno_de_software', 'administracion_de_proyectos']"),
    ("Viquez Acuna Oscar Mario", "89012345", "['tuesday_12_4', 'thursday_12_4', 'monday_7_11']", "['inteligencia_artificial', 'investigacion_de_operaciones', 'aseguramiento_de_la_calidad_del_software']"),
    ("Alfaro Velasco Jorge", "90123456", "['wednesday_7_11', 'friday_12_4', 'tuesday_12_4']", "['principios_de_sistemas_operativos', 'administracion_de_proyectos', 'redes']"),
    ("Esquivel Vega Gaudy", "01234567", "['monday_12_4', 'friday_7_11', 'wednesday_12_4']", "['aseguramiento_de_la_calidad_del_software', 'redes', 'proyecto_de_ingenieria_de_software']"),
    ("Alfaro Quesada Alejandro", "11234567", "['tuesday_7_11', 'thursday_12_4', 'friday_12_4']", "['proyecto_de_ingenieria_de_software', 'bases_de_datos_ii', 'compiladores_e_interpretes']"),
    ("Jimenez Delgado Efren Antonio", "12234567", "['wednesday_7_11', 'friday_7_11', 'monday_12_4']", "['computacion_y_sociedad', 'introduccion_al_desarrollo_de_paginas_web', 'programacion_orientada_a_objetos']"),
    ("Ballestero Alfaro Esteban", "13234567", "['monday_12_4', 'thursday_7_11', 'friday_12_4']", "['introduccion_al_desarrollo_de_paginas_web', 'fundamentos_de_organizacion_de_computadoras', 'arquitectura_de_computadores']"),
    ("Campos Fuentes Marvin", "14234567", "['tuesday_12_4', 'wednesday_7_11', 'monday_7_11']", "['analisis_de_algoritmos', 'estrategias_de_solucion_de_problemas', 'introduccion_a_la_programacion']"),
    ("Gonzalez Quiros Rogelio", "15234567", "['monday_7_11', 'friday_12_4', 'wednesday_12_4']", "['bases_de_datos_i', 'compiladores_e_interpretes', 'fundamentos_de_organizacion_de_computadoras']"),
    ("Rojas Vega Diego", "16234567", "['tuesday_12_4', 'wednesday_12_4', 'thursday_7_11']", "['compiladores_e_interpretes', 'arquitectura_de_computadores', 'elementos_de_computacion']"),
    ("Cubillo Rojas Adalberto Jesus", "17234567", "['thursday_7_11', 'friday_7_11', 'monday_12_4']", "['inteligencia_artificial', 'investigacion_de_operaciones', 'proyecto_de_ingenieria_de_software']")
    ]

    try:
        for prof in professors:
            query = """
            INSERT INTO professors (name, id_number, available_hours, courses) VALUES (?, ?, ?, ?)
            """
            execute_query(query, prof)
        return {"message": "Professors inserted into SQLite successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to insert courses into SQLite
@app.get("/insert_courses/")
def insert_courses():
    courses = [
        ("elementos_de_computacion", "normal", 3, 1),
        ("analisis_y_diseno_de_algoritmos", "normal", 4, 3),
        ("fundamentos_de_organizacion_de_computadoras", "normal", 4, 1),
        ("introduccion_a_la_programacion", "normal", 4, 1),
        ("taller_de_programacion", "normal", 4, 1),
        ("estructuras_de_datos", "normal", 4, 2),
        ("programacion_orientada_a_objetos", "normal", 4, 2),
        ("analisis_de_algoritmos", "normal", 4, 3),
        ("arquitectura_de_computadores", "normal", 4, 2),
        ("bases_de_datos_i", "normal", 4, 3),
        ("bases_de_datos_ii", "normal", 4, 4),
        ("lenguajes_de_programacion", "normal", 4, 4),
        ("administracion_de_proyectos", "normal", 3, 5),
        ("compiladores_e_interpretes", "normal", 4, 5),
        ("requerimientos_de_software", "normal", 4, 3),
        ("inteligencia_artificial", "normal", 4, 7),
        ("investigacion_de_operaciones", "normal", 4, 6),
        ("principios_de_sistemas_operativos", "normal", 4, 6),
        ("diseno_de_software", "normal", 4, 4),
        ("aseguramiento_de_la_calidad_del_software", "normal", 3, 5),
        ("redes", "normal", 4, 7),
        ("proyecto_de_ingenieria_de_software", "normal", 4, 7),
        ("computacion_y_sociedad", "normal", 2, 7),
        ("introduccion_al_desarrollo_de_paginas_web", "normal", 3, 6)
    ]

    try:
        for course in courses:
            query = """
            INSERT INTO courses (name, type, credits, semester) VALUES (?, ?, ?, ?)
            """
            execute_query(query, course)
        return {"message": "Courses inserted into SQLite successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/load_professors_into_prolog/")
def load_professors_into_prolog():
    query = "SELECT name, available_hours, courses FROM professors"
    try:
        professors = execute_query(query)
        for prof in professors:
            name = prof[0].lower().replace(' ', '_')
            available_hours_list = ast.literal_eval(prof[1])
            courses_list = ast.literal_eval(prof[2])

            # Parse available_hours into ['day', Start, End]
            parsed_hours = []
            for hour in available_hours_list:
                parts = hour.split('_')
                if len(parts) == 3:
                    day, start, end = parts
                    # Asegurarse de que Start y End sean números
                    try:
                        start = int(start)
                        end = int(end)
                        day = day.lower()
                        parsed_hours.append(f"['{day}', {start}, {end}]")
                    except ValueError:
                        continue  # Ignorar entradas mal formateadas
                else:
                    continue  # Ignorar entradas mal formateadas

            available_hours_prolog = "[" + ", ".join(parsed_hours) + "]"

            # Parse courses as atoms
            courses_prolog = "[" + ", ".join([f"'{course.lower().replace(' ', '_')}'" for course in courses_list]) + "]"

            # Insertar hechos en Prolog
            prolog.assertz(f"professor('{name}', {available_hours_prolog}, {courses_prolog})")
        return {"message": "Professors loaded into Prolog successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/load_courses_into_prolog/")
def load_courses_into_prolog():
    query = "SELECT name, type, credits, semester FROM courses"
    try:
        courses = execute_query(query)
        for course in courses:
            name = course[0].lower().replace(' ', '_')
            room_type = course[1].lower().replace(' ', '_')
            credits = course[2]
            semester = course[3]
            
            # Insertar hechos en Prolog
            prolog.assertz(f"course('{name}', '{room_type}', {credits}, {semester})")
        return {"message": "Courses loaded into Prolog successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get all professors from SQLite
@app.get("/get_professors/")
def get_professors():
    query = "SELECT name, id_number, available_hours, courses FROM professors"
    try:
        professors = execute_query(query)
        return [
            {
                "name": prof[0],
                "id_number": prof[1],
                "available_hours": prof[2],
                "courses": prof[3]
            } for prof in professors
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get all courses from SQLite
@app.get("/get_courses/")
def get_courses():
    query = "SELECT name, type, credits, semester FROM courses"
    try:
        courses = execute_query(query)
        return [
            {
                "name": course[0],
                "type": course[1],
                "credits": course[2],
                "semester": course[3]
            } for course in courses
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to query Prolog for schedule generation
@app.get("/get_schedule/")
def get_schedule(courses: List[str] = Query(None)):
    if not courses:
        # Definir cursos predeterminados o manejar el caso en que no se proporcionen cursos
        courses = ['elementos_de_computacion', 'introduccion_a_la_programacion']

    # Formatear la lista de cursos para Prolog sin comillas alrededor de los nombres (átomos)
    courses_prolog = "[" + ", ".join([course.lower().replace(' ', '_') for course in courses]) + "]"

    # Construir la consulta Prolog
    query = f"find_schedule_for_courses({courses_prolog}, Schedule)"
    try:
        # Ejecutar la consulta Prolog y limitar a 3 resultados
        results = list(prolog.query(query, maxresult=3))
        schedules = []
        for result in results:
            sched = result['Schedule']
            schedule = []
            for item in sched:
                schedule.append({
                    "course": item[0],
                    "professor": item[1],
                    "room": item[2],
                    "day": item[3],
                    "start": item[4],
                    "end": item[5]
                })
            schedules.append(schedule)
        print(schedules)
        if not schedules:
            return {"message": "No schedule found for the given courses"}
        return schedules
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    

@app.get("/list_courses_in_prolog/")
def list_courses_in_prolog():
    try:
        results = list(prolog.query("course(Name, RoomType, Credits, Semester)"))
        courses = []
        for result in results:
            courses.append({
                "name": result['Name'],
                "room_type": result['RoomType'],
                "credits": result['Credits'],
                "semester": result['Semester']
            })
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint para generar horarios según paridad de semestre
@app.get("/generate_schedule/")
def generate_schedule(parity: str):
    if parity not in ['even', 'odd']:
        raise HTTPException(status_code=400, detail="Parity must be 'even' or 'odd'")

    try:
        # Construir la consulta Prolog
        # Utilizamos findall para obtener todas las soluciones posibles
        query = f"find_schedule_for_semester_parity('{parity}', Schedule)"
        prolog_query = list(prolog.query(query))

        if not prolog_query:
            return {"message": "No schedule found for the given parity"}

        # Extraer los horarios de la consulta
        schedules = []
        for result in prolog_query:
            schedule = result["Schedule"]
            formatted_schedule = []
            for item in schedule:
                course, professor, room, day, start, end = item
                # Convertir los datos a un diccionario
                formatted_schedule.append({
                    "course": course,
                    "professor": professor,
                    "room": room,
                    "day": day.strip("'"),
                    "start": start,
                    "end": end
                })
            schedules.append(formatted_schedule)
            if len(schedules) == 3:
                break  # Limitar a las primeras 3 opciones

        if not schedules:
            return {"message": "No schedule found for the given parity"}

        return {"schedules": schedules}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/clear_prolog_facts/")
def clear_prolog_facts():
    try:
        prolog.retractall("course(_, _, _, _)")
        prolog.retractall("professor(_, _, _)")
        return {"message": "All Prolog facts have been cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list_prolog_facts/")
def list_prolog_facts():
    try:
        professors = list(prolog.query("professor(Name, AvailableHours, Courses)"))
        courses = list(prolog.query("course(Name, RoomType, Credits, Semester)"))
        return {
            "professors": professors,
            "courses": courses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ENDPOINTS IMPORTANTES
# Se recomienda usar una herramienta como Postman para usar los enpoints o el navegador, hay otros endpoints que no se mencionan aquí pero que se usan en el frontend
# Run using uvicorn: `uvicorn main:app --reload`
# Endpoint para añadir a los profes en la base de datos (Nada más una vez, a no ser que borre la base de datos): http://127.0.0.1:8000/insert_professors/
# Endpoint para añadir los cursos en la base de datos (Nada más una vez, a no ser que borre la base de datos): http://127.0.0.1:8000/insert_courses/
# Para cargar los profes a Prolog (Siempre que se inicie el server): http://127.0.0.1:8000/load_professors_into_prolog/
# Para cargar los cursos a Prolog (Siempre que se inicie el server): http://127.0.0.1:8000/load_courses_into_prolog/
# Para ver si los profes están cargados en la base de datos (Siempre que se inicie el server): http://127.0.0.1:8000/get_professors/
# Para ver si los cursos están cargados en la base de datos (Siempre que se inicie el server): http://127.0.0.1:8000/get_courses/
# Access the endpoint at: http://127.0.0.1:8000/get_schedule/

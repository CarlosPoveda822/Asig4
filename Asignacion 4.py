import redis
import json
import uuid

client = redis.StrictRedis(host='localhost', port=6379, db=0)

def agregar_receta(nombre, ingredientes, pasos):
    nueva_receta = {
        "nombre": nombre,
        "ingredientes": ingredientes.split(', '),
        "pasos": pasos.split('. ')
    }
    receta_id = str(uuid.uuid4())
    try:
        client.set(receta_id, json.dumps(nueva_receta))
        print("Receta agregada exitosamente.")
    except Exception as e:
        print(f"Error al agregar la receta: {e}")

def actualizar_receta(id_receta, nombre, ingredientes, pasos):
    try:
        receta = client.get(id_receta)
        if receta:
            nueva_receta = {
                "nombre": nombre,
                "ingredientes": ingredientes.split(', '),
                "pasos": pasos.split('. ')
            }
            client.set(id_receta, json.dumps(nueva_receta))
            print("Receta actualizada exitosamente.")
        else:
            print("Receta no encontrada.")
    except Exception as e:
        print(f"Error al actualizar la receta: {e}")

def eliminar_receta(id_receta):
    try:
        result = client.delete(id_receta)
        if result:
            print("Receta eliminada exitosamente.")
        else:
            print("Receta no encontrada.")
    except Exception as e:
        print(f"Error al eliminar la receta: {e}")

def ver_listado_recetas():
    try:
        keys = client.keys()
        if keys:
            for key in keys:
                receta = json.loads(client.get(key).decode('utf-8'))
                print(f"ID: {key.decode('utf-8')}, Nombre: {receta['nombre']}")
        else:
            print("No hay recetas en la base de datos.")
    except Exception as e:
        print(f"Error al obtener el listado de recetas: {e}")

def buscar_receta_por_ingredientes(ingredientes):
    try:
        keys = client.keys()
        ingredientes_buscar = ingredientes.split(', ')
        if keys:
            found = False
            for key in keys:
                receta = json.loads(client.get(key).decode('utf-8'))
                if all(ingrediente in receta['ingredientes'] for ingrediente in ingredientes_buscar):
                    print(f"Nombre: {receta['nombre']}")
                    print(f"Ingredientes: {', '.join(receta['ingredientes'])}")
                    print(f"Pasos: {'. '.join(receta['pasos'])}")
                    print()
                    found = True
            if not found:
                print("No se encontraron recetas con esos ingredientes.")
        else:
            print("No hay recetas en la base de datos.")
    except Exception as e:
        print(f"Error al buscar recetas por ingredientes: {e}")

def buscar_receta_por_pasos(pasos):
    try:
        keys = client.keys()
        pasos_buscar = pasos.split('. ')
        if keys:
            found = False
            for key in keys:
                receta = json.loads(client.get(key).decode('utf-8'))
                if all(paso in receta['pasos'] for paso in pasos_buscar):
                    print(f"Nombre: {receta['nombre']}")
                    print(f"Ingredientes: {', '.join(receta['ingredientes'])}")
                    print(f"Pasos: {'. '.join(receta['pasos'])}")
                    print()
                    found = True
            if not found:
                print("No se encontraron recetas con esos pasos.")
        else:
            print("No hay recetas en la base de datos.")
    except Exception as e:
        print(f"Error al buscar recetas por pasos: {e}")

def main():
    while True:
        print("\n--- Menú ---")
        print("a) Agregar nueva receta")
        print("b) Actualizar receta existente")
        print("c) Eliminar receta existente")
        print("d) Ver listado de recetas")
        print("e) Buscar recetas por ingredientes")
        print("f) Buscar recetas por pasos")
        print("g) Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == 'a':
            nombre = input("Nombre de la receta: ")
            ingredientes = input("Ingredientes (separados por comas): ")
            pasos = input("Pasos de la receta (separados por puntos): ")
            agregar_receta(nombre, ingredientes, pasos)
        elif opcion == 'b':
            id_receta = input("ID de la receta a actualizar: ")
            nombre = input("Nuevo nombre de la receta: ")
            ingredientes = input("Nuevos ingredientes (separados por comas): ")
            pasos = input("Nuevos pasos de la receta (separados por puntos): ")
            actualizar_receta(id_receta, nombre, ingredientes, pasos)
        elif opcion == 'c':
            id_receta = input("ID de la receta a eliminar: ")
            eliminar_receta(id_receta)
        elif opcion == 'd':
            ver_listado_recetas()
        elif opcion == 'e':
            ingredientes = input("Ingrese los ingredientes a buscar (separados por comas): ")
            buscar_receta_por_ingredientes(ingredientes)
        elif opcion == 'f':
            pasos = input("Ingrese los pasos a buscar (separados por puntos): ")
            buscar_receta_por_pasos(pasos)
        elif opcion == 'g':
            print("Adios owo/")
            client.connection_pool.disconnect()
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()


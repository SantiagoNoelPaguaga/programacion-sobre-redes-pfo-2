import requests

BASE_URL = "http://127.0.0.1:5000"

session_cliente = requests.Session()

def menu():
    print("\n" + "="*30)
    print("GESTIÓN DE TAREAS")
    print("="*30)
    print("1. Registrarse")
    print("2. Iniciar Sesión")
    print("3. Ver Bienvenida (Requiere Login)")
    print("4. Salir")
    return input("\nSeleccione una opción: ")

def registrar_usuario():
    usuario = input("Nombre de usuario: ")
    password = input("Contraseña: ")
    
    payload = {"usuario": usuario, "contraseña": password} 
    
    try:
        response = session_cliente.post(f"{BASE_URL}/registro", json=payload)
        data = response.json()
        
        if response.ok:
            print(f"\nServidor: {data.get('mensaje')}")
        else:
            print(f"\nError: {data.get('error')}")
    except Exception as e:
        print(f"\nError de conexión: {e}")

def login_usuario():
    usuario = input("Usuario: ")
    password = input("Contraseña: ")
    payload = {"usuario": usuario, "contraseña": password}
    
    try:
        response = session_cliente.post(f"{BASE_URL}/login", json=payload)
        data = response.json()
        
        if response.ok:
            print("\nLogin exitoso. La sesión ahora está activa.")
        else:
            print(f"\nError: {data.get('error')}")
    except Exception as e:
        print(f"\nError de conexión: {e}")

def ver_tareas():
    url = f"{BASE_URL}/tareas"
    
    try:
        response = session_cliente.get(url)
        
        if response.status_code == 401:
            print("\nACCESO DENEGADO: Debes iniciar sesión primero.")
        elif response.ok:
            print("\n" + "—"*50)
            print("CÓDIGO HTML RECIBIDO:")
            print("—"*50)
            print(response.text)
            print("—"*50)
        else:
            print(f"\nError inesperado: Código {response.status_code}")
            
    except Exception as e:
        print(f"\nError de conexión: {e}")

if __name__ == "__main__":
    while True:
        opcion = menu()
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            login_usuario()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "4":
            print("\nSaliendo del sistema...")
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
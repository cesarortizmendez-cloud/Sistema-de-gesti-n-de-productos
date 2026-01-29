from modulos.ui_tkinter import App  # Importamos la clase principal de la interfaz (ventana Tkinter)

def main():  # Definimos la función principal (punto de inicio lógico del programa)
    app = App()  # Creamos la aplicación (ventana) usando nuestra clase App
    app.mainloop()  # Iniciamos el “bucle” de Tkinter (mantiene la ventana funcionando)

if __name__ == "__main__":  # Esto asegura que main() se ejecute solo si corremos este archivo directamente
    main()  # Llamamos a la función principal

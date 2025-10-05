def ejercicio_respiracion():
    print("\nVamos a hacer un ejercicio de respiración.")
    print("Inhala profundamente por la nariz durante 4 segundos...")
    print("Mantén el aire durante 4 segundos...")
    print("Exhala lentamente por la boca durante 4 segundos...")
    print("Repite este ciclo varias veces.\n")

def frase_apoyo():
    import random
    frases = [
        "Recuerda: esto también pasará.",
        "Eres más fuerte de lo que crees.",
        "Respira, todo estará bien.",
        "No estás solo/a, estoy aquí contigo."
    ]
    print("\n" + random.choice(frases) + "\n")

def registrar_emocion(nombre):
    emocion = input("¿Cómo te sientes hoy? (por ejemplo: tranquilo, ansioso, feliz, triste): ")
    with open("emociones.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{nombre}: {emocion}\n")
    print("¡Gracias por compartir cómo te sientes!\n")

def main():
    print("¡Hola, soy Serenity! Estoy aquí para ayudarte a manejar la ansiedad.")
    nombre = input("¿Cómo te llamas? ")
    print("¡Hola, " + nombre + "!")
    registrar_emocion(nombre)

    if nombre.lower() == "serenity":
        print("¡Qué bonito nombre! ¿Sabías que Serenity es un asistente para la ansiedad?")
    else:
        print("¡Encantado de conocerte, " + nombre + "!")

    while True:
        print("\n¿Qué te gustaría hacer ahora?")
        print("1. Hacer un ejercicio de respiración")
        print("2. Recibir una frase de apoyo")
        print("3. Registrar cómo te sientes")
        print("4. Salir")
        opcion = input("Escribe 1, 2, 3 o 4: ").strip()

        if opcion == "1":
            ejercicio_respiracion()
        elif opcion == "2":
            frase_apoyo()
        elif opcion == "3":
            registrar_emocion(nombre)
        elif opcion == "4":
            print("Gracias por hablar conmigo. ¡Cuídate!")
            break
        else:
            print("No entendí tu respuesta. Por favor, escribe 1, 2, 3 o 4.")

if __name__ == "__main__":
    main()
    import streamlit as st
import random

def ejercicio_respiracion():
    st.write("Vamos a hacer un ejercicio de respiración.")
    st.write("Inhala profundamente por la nariz durante 4 segundos...")
    st.write("Mantén el aire durante 4 segundos...")
    st.write("Exhala lentamente por la boca durante 4 segundos...")
    st.write("Repite este ciclo varias veces.")

def frase_apoyo():
    frases = [
        "Recuerda: esto también pasará.",
        "Eres más fuerte de lo que crees.",
        "Respira, todo estará bien.",
        "No estás solo/a, estoy aquí contigo."
    ]
    st.write(random.choice(frases))

def registrar_emocion(nombre, emocion):
    if emocion:
        with open("emociones.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"{nombre}: {emocion}\n")
        st.success("¡Gracias por compartir cómo te sientes!")

st.title("Serenity - Asistente para la ansiedad")

nombre = st.text_input("¿Cómo te llamas?")

if nombre:
    st.write(f"¡Hola, {nombre}!")
    emocion = st.text_input("¿Cómo te sientes hoy? (por ejemplo: tranquilo, ansioso, feliz, triste)")
    if st.button("Registrar emoción"):
        registrar_emocion(nombre, emocion)

    opcion = st.radio(
        "¿Qué te gustaría hacer ahora?",
        ("Hacer un ejercicio de respiración", "Recibir una frase de apoyo", "Nada más")
    )

    if opcion == "Hacer un ejercicio de respiración":
        ejercicio_respiracion()
    elif opcion == "Recibir una frase de apoyo":
        frase_apoyo()
    else:
        st.write("¡Gracias por hablar conmigo. Cuídate!")
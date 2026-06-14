"""
Punto de entrada de la aplicación Flask con sistema de agentes autónomos
"""
import atexit
from app import create_app
from planificador_agentes import iniciar_planificador, detener_planificador

app = create_app()

# Iniciar sistema de agentes autónomos
planificador = iniciar_planificador(app)

# Detener agentes al cerrar la aplicación
atexit.register(detener_planificador)

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n⏹️  Deteniendo aplicación...")
        detener_planificador()
        print("✅ Aplicación cerrada correctamente\n")

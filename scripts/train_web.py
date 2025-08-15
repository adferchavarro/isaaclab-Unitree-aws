import os
import subprocess
import threading
import time

# === Configuración de streaming para Isaac Sim (variables de entorno recomendadas) ===
os.environ["ISAAC_SIM_HEADLESS"] = "false"
os.environ["ENABLE_STREAMING"] = "true"
os.environ["STREAMING_WEBSOCKET_PORT"] = "8211"
os.environ["STREAMING_RTC_PORT"] = "9000"

# Ajusta estos nombres/rutas si cambias la estructura del repo
TRAIN_SCRIPT = "/workspace/scripts/train.py"
ISAAC_SIM_LAUNCH = "/isaac-sim/isaac-sim.sh"  # ruta típica en la imagen oficial

def run_training():
    if not os.path.exists(TRAIN_SCRIPT):
        print(f"[train_web] Entrenamiento: no se encontró {TRAIN_SCRIPT}")
        return
    print("[train_web] Iniciando entrenamiento (PPO)...")
    # Ejecuta el script de entrenamiento dentro del contenedor
    subprocess.run(["python3", TRAIN_SCRIPT])

def run_streaming():
    # Lanza Isaac Sim (kit) para habilitar el streaming WebRTC.
    # En la mayoría de imágenes de Isaac Sim está disponible el script isaac-sim.sh
    if os.path.exists(ISAAC_SIM_LAUNCH):
        print("[train_web] Lanzando Isaac Sim para streaming WebRTC...")
        # Ejecutamos en modo "normal" (no headless) para que el servidor de streaming se levante
        subprocess.run([ISAAC_SIM_LAUNCH, "--/app/window/visible=true"])
    else:
        print(f"[train_web] No se encontró el lanzador de Isaac Sim en {ISAAC_SIM_LAUNCH}. Si usas otra ruta, edita este script.")

if __name__ == '__main__':
    # Ejecuta entrenamiento en un hilo y streaming en el hilo principal para que se mantenga la app viva.
    t = threading.Thread(target=run_training, daemon=True)
    t.start()

    # Pequeña espera para que el entrenamiento inicialice antes de levantar la UI
    time.sleep(5.0)
    run_streaming()

    # Mantener el proceso principal vivo si el streaming se lanza como proceso externo
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("[train_web] Interrupción recibida, cerrando.")

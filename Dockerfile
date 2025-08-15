FROM nvcr.io/nvidia/isaac-sim:2023.1.1

# Instalar dependencias de Isaac Lab (asumiendo que ya están en la imagen base)
WORKDIR /workspace

# Copiar proyecto
COPY . /workspace

# Configuración de puertos
EXPOSE 8211
EXPOSE 9000

# Variable para streaming
ENV ISAAC_SIM_HEADLESS=false
ENV ENABLE_STREAMING=true
ENV STREAMING_WEBSOCKET_PORT=8211
ENV STREAMING_RTC_PORT=9000

# Comando por defecto: lanzar entrenamiento + streaming
CMD ["python3", "scripts/train_web.py"]

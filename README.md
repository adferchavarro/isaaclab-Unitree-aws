# Proyecto IsaacLab + IsaacSim en Azure con Streaming Web para Unitree G1

Este proyecto configura un entorno de **IsaacLab** y **IsaacSim** en un contenedor Docker ejecutado en Azure,
para entrenar un robot humanoide **Unitree G1** con aprendizaje por refuerzo (PPO) y visualizarlo en el navegador vía **WebRTC**.

## 📋 Requisitos previos

- Cuenta en **Microsoft Azure**
- **Azure Container Instances** o **Azure Web App for Containers**
- Imagen base de Isaac Sim con soporte de Isaac Lab (`isaac-sim:2023.1.1` u otra compatible)
- Puertos abiertos en Azure:
  - `8211` (WebSocket WebRTC)
  - `9000` (RTC media)
- **GitHub** o repositorio donde subir este proyecto

## 🚀 Pasos para desplegar en Azure

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tuusuario/azure_isaaclab_project.git
   cd azure_isaaclab_project
   ```

2. **Construir la imagen Docker localmente (opcional para pruebas)**
   ```bash
   docker build -t azure-isaaclab .
   ```

3. **Subir a Azure**
   - Empuja la imagen a **Azure Container Registry (ACR)**:
     ```bash
     az acr build --registry TU_ACR --image azure-isaaclab .
     ```
   - Crea una instancia de contenedor en Azure que use la imagen desde tu ACR.

4. **Configurar puertos en Azure**
   - WebSocket: `8211`
   - WebRTC: `9000`

5. **Acceder al streaming**
   - Abre tu navegador en:
     ```
     http://<IP_PUBLICA_AZURE>:8211
     ```

## 📂 Estructura del proyecto

```
.
├── Dockerfile
├── docker-compose.yml
├── README.md
├── scripts
│   ├── train.py
│   └── train_web.py
├── workspace
│   ├── configs
│   │   └── tasks
│   │       └── my_unitree_g1.yaml
│   └── tasks
│       └── my_unitree_g1.py
```

## 🏃 Ejecución local (opcional)

Para probar antes de desplegar:
```bash
docker-compose up
```
Luego abre en el navegador `http://localhost:8211`.

## 📌 Notas importantes

- `train_web.py` lanza **Isaac Sim** en modo visible para habilitar WebRTC y entrena simultáneamente el robot.
- Si usas otra ruta para `isaac-sim.sh` dentro del contenedor, actualiza la variable `ISAAC_SIM_LAUNCH` en `train_web.py`.
- Isaac Lab y Isaac Sim son intensivos en GPU. Este entorno requiere un **VM de Azure con GPU** (ej. `Standard_NC6s_v3`).

## 🤖 Robot soportado

Actualmente el proyecto incluye una tarea personalizada para el **Unitree G1** que permite entrenarlo para:
- Ponerse de pie
- Mantener el equilibrio
- Movimientos básicos

Puedes extender el archivo `my_unitree_g1.py` para definir nuevas recompensas y comportamientos.

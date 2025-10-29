from ultralytics import YOLO
import cv2

# 1️⃣ Carga el modelo preentrenado YOLOv8
model = YOLO("yolov8n.pt")

# 2️⃣ Función que detecta vehículos en cada cuadro (frame) de la cámara
def detect_vehicles(frame):
    results = model(frame)  # Pasa el frame al modelo
    for r in results[0].boxes.data.tolist():  # Recorre los objetos detectados
        x1, y1, x2, y2, score, class_id = r  # Coordenadas y tipo de objeto

        # 3️⃣ Filtra solo vehículos: 2=car, 3=motorcycle, 5=bus, 7=truck
        if int(class_id) in [2, 3, 5, 7]:
            # Dibuja el cuadro verde
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    return frame

# 4️⃣ Abre la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = detect_vehicles(frame)  # Detecta vehículos en tiempo real
    cv2.imshow("SmartPark AI - Detección de vehículos", frame)

    # 5️⃣ Presiona "q" para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 6️⃣ Libera recursos
cap.release()
cv2.destroyAllWindows()

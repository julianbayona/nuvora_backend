from ultralytics import YOLO
import cv2
import easyocr

# Cargar modelo YOLO
model = YOLO("yolov8n.pt")

# Inicializar OCR
ocr = easyocr.Reader(['en'])

def detect_vehicles_and_plates(frame):
    results = model(frame)
    for r in results[0].boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = r
        if int(class_id) in [2, 3, 5, 7]:
            # Dibuja el cuadro verde
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            # Extrae la región (ROI) para el OCR
            roi = frame[int(y1):int(y2), int(x1):int(x2)]

            # Aplica OCR
            text = ocr.readtext(roi)
            if text:
                # Muestra la placa detectada en consola
                print("📸 Placa detectada:", text[0][1])
    return frame

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = detect_vehicles_and_plates(frame)
    cv2.imshow("SmartPark AI - Detección de vehículos y placas", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

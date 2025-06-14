import pyrealsense2 as rs
import numpy as np
import cv2
from keras.models import load_model

# === Carrega modelo treinado e classes ===
model = load_model("converted/model.savedmodel", compile=False)
class_names = open("converted/labels.txt", "r").readlines()

# === Inicializa pipeline RealSense com alinhamento ===
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# Alinha depth com color
align = rs.align(rs.stream.color)

try:
    while True:
        # Captura e alinha os frames
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Converte para arrays do OpenCV
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Redimensiona para modelo Keras (224x224)
        input_image = cv2.resize(color_image, (224, 224), interpolation=cv2.INTER_AREA)
        input_image_np = np.asarray(input_image, dtype=np.float32).reshape(1, 224, 224, 3)
        input_image_np = (input_image_np / 127.5) - 1

        # Faz predição
        prediction = model.predict(input_image_np)
        index = np.argmax(prediction)
        class_name = class_names[index].strip()
        confidence_score = prediction[0][index]

        # Calcula distância no centro
        h, w, _ = color_image.shape
        cx, cy = w // 2, h // 2
        distance = depth_frame.get_distance(cx, cy)

        # Mensagem adaptada caso sem leitura de profundidade
        if distance == 0.0:
            distance_text = "Distância não detectada"
        else:
            distance_text = f"{distance:.2f} m"

        # Exibe informações na imagem
        display_text = f"{class_name}: {confidence_score*100:.1f}% | {distance_text}"
        cv2.circle(color_image, (cx, cy), 6, (0, 255, 255), -1)
        cv2.putText(color_image, display_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Exibe imagem RGB com detecção
        cv2.imshow("TensorFlow + RealSense", color_image)

        # (Opcional) Exibe mapa de profundidade em escala de cores
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03),
                                           cv2.COLORMAP_JET)
        cv2.imshow("Mapa de Profundidade", depth_colormap)

        # ESC para sair
        if cv2.waitKey(1) == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()

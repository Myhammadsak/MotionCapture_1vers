import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time
import json
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING
)
logger = logging.getLogger(__name__)


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
a = time.monotonic()
stop = 0

#Создаем список для хранения углов
list_angle_right_golen_right_camera = []
list_angle_right_kolen_right_camera = []
list_angle_right_bed_right_camera = []
list_angle_right_camera = []

# открываем json файл чтобы взять из него индекс пути камеры
with open('camera_index.json') as fcc_file:
    index_cam = json.load(fcc_file)

# Видео поток
cap = cv2.VideoCapture(index_cam['ri'])
# установка медипайп
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        res = cv2.resize(frame, (600, 500))

        # Обнаружение вещей и рендеринг
        # перекрашивание картинки
        image = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # детекция изображения
        results = pose.process(image)

        # обратно в bgr
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Извлечение ориентиров
        try:
            landmarks = results.pose_landmarks.landmark

            # Получение координат точек правой голени
            r_knee_golen = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            r_ankle_golen = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            r_foot_golen = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
            # Калькулятор углов
            a_r_knee_golen = np.array(r_knee_golen)  # First
            b_r_ankle_golen = np.array(r_ankle_golen)  # Mid
            c_r_foot_golen = np.array(r_foot_golen)  # End
            radians_right_golen = np.arctan2(c_r_foot_golen[1] - b_r_ankle_golen[1], c_r_foot_golen[0] - b_r_ankle_golen[0]) - np.arctan2(a_r_knee_golen[1] - b_r_ankle_golen[1], a_r_knee_golen[0] - b_r_ankle_golen[0])
            angle_right_golen = np.abs(radians_right_golen * 360 // np.pi)
            if angle_right_golen > 180:
                angle_right_golen = 360 - angle_right_golen
                angle_right_golen -= 35
            list_angle_right_golen_right_camera.append(angle_right_golen)

            # Визуализация
            cv2.putText(image, str(angle_right_golen),
                        tuple(np.multiply(r_ankle_golen, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )



            # Получение координат точек правой коленки
            r_hip_kolen = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            r_knee_kolen = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            r_ankle_kolen = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            # Калькулятор углов
            a_r_hip_kolen = np.array(r_hip_kolen)  # First
            b_r_knee_kolen = np.array(r_knee_kolen)  # Mid
            c_r_ankle_kolen = np.array(r_ankle_kolen)  # End
            radians_right_kolen = np.arctan2(c_r_ankle_kolen[1] - b_r_knee_kolen[1], c_r_ankle_kolen[0] - b_r_knee_kolen[0]) - np.arctan2(a_r_hip_kolen[1] - b_r_knee_kolen[1], a_r_hip_kolen[0] - b_r_knee_kolen[0])
            angle_right_kolen = np.abs(radians_right_kolen * 180 // np.pi)
            if 0 < angle_right_kolen > 150.0:
                angle_right_kolen = 360 - angle_right_kolen
                angle_right_kolen = 180 - angle_right_kolen
            list_angle_right_kolen_right_camera.append(angle_right_kolen)


            # Визуализация
            cv2.putText(image, str(angle_right_kolen),
                        tuple(np.multiply(r_knee_kolen, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )

            # Получение координат точек правого бедра
            r_shoulder_bed = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            r_hip_bed = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            r_knee_bed = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            # Калькулятор углов
            a_r_shoulder_bed = np.array(r_shoulder_bed)  # First
            b_r_hip_bed = np.array(r_hip_bed)  # Mid
            c_r_knee_bed = np.array(r_knee_bed)  # End
            radians_right_bed = np.arctan2(c_r_knee_bed[1] - b_r_hip_bed[1], c_r_knee_bed[0] - b_r_hip_bed[0]) - np.arctan2(a_r_shoulder_bed[1] - b_r_hip_bed[1], a_r_shoulder_bed[0] - b_r_hip_bed[0])
            angle_right_bed = np.abs(radians_right_bed * 360 // np.pi)
            if angle_right_bed > 180.0:
                angle_right_bed = 360 - angle_right_bed
            list_angle_right_bed_right_camera.append(angle_right_bed)


            # Визуализация
            cv2.putText(image, str(angle_right_bed),
                        tuple(np.multiply(r_hip_bed, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )


        except:
            pass
            # рендер детекции
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('right_camera', image)

        # Завершает процесс по истечении 30 секунд
        if cv2.waitKey(10) & 0xFF == ord('q') or time.monotonic() - a > 30:
            stop += 1
            break

    cap.release()
    cv2.destroyAllWindows()

# Создание таблицы с параметрами ключевых точек
dict1 = {
    'Правый голеностоп': list_angle_right_golen_right_camera,
    'Правая коленка': list_angle_right_kolen_right_camera,
    'Правый тазобедренный сустав':list_angle_right_bed_right_camera
}
df = pd.DataFrame(dict1)

globlist_right_camera = (df['Правый голеностоп'].mean(), df['Правый голеностоп'].min(), df['Правый голеностоп'].max(), df['Правая коленка'].mean(), df['Правая коленка'].min(), df['Правая коленка'].max(), df['Правый тазобедренный сустав'].mean(), df['Правый тазобедренный сустав'].min(), df['Правый тазобедренный сустав'].max())
# Запись полученных максимальных, минимальных, средних значений в текстовый файл
my_file1 = open(fr'C:\right_camera.txt', 'w+')
my_file1.write(f'{globlist_right_camera}')
my_file1.close()
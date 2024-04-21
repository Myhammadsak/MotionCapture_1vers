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
list_angle_left_golen_left_camera = []
list_angle_left_kolen_left_camera = []
list_angle_left_bed_left_camera = []

# открываем json файл чтобы взять из него индекс пути камеры
with open('camera_index.json') as fcc_file:
    index_cam = json.load(fcc_file)

# Видео поток
cap = cv2.VideoCapture(index_cam['le'])
# установка медипайп
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        res = cv2.resize(frame, (600, 500))

        # Обнаружение вещей и рендеринг
        # перекрашивание картинки
        image = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        #детекция изображения
        results = pose.process(image)

        # обратно в bgr
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Извлечение ориентиров
        try:
            landmarks = results.pose_landmarks.landmark

            # Получение координат точек левой голени
            l_knee_golen = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            l_ankle_golen = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            l_foot_golen = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
            # Калькулятор углов
            a_l_knee_golen = np.array(l_knee_golen)  # First
            b_l_ankle_golen = np.array(l_ankle_golen)  # Mid
            c_l_foot_golen = np.array(l_foot_golen)  # End
            radians_left_golen = np.arctan2(c_l_foot_golen[1] - b_l_ankle_golen[1], c_l_foot_golen[0] - b_l_ankle_golen[0]) - np.arctan2(a_l_knee_golen[1] - b_l_ankle_golen[1], a_l_knee_golen[0] - b_l_ankle_golen[0])
            angle_left_golen = np.abs(radians_left_golen * 360 // np.pi)
            if angle_left_golen > 180.0:
                angle_left_golen = 360 - angle_left_golen
                angle_left_golen += 215
            list_angle_left_golen_left_camera.append(angle_left_golen)

            # Визуализация
            cv2.putText(image, str(angle_left_golen),
                        tuple(np.multiply(l_ankle_golen, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )


            # Получение координат точек левой коленки
            l_hip_kolen = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            l_knee_kolen = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            l_ankle_kolen = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            # Калькулятор углов
            a_l_hip_kolen = np.array(l_hip_kolen)  # First
            b_l_knee_kolen = np.array(l_knee_kolen)  # Mid
            c_l_ankle_kolen = np.array(l_ankle_kolen)  # End
            radians_left_golen = np.arctan2(c_l_ankle_kolen[1] - b_l_knee_kolen[1], c_l_ankle_kolen[0] - b_l_knee_kolen[0]) - np.arctan2(a_l_hip_kolen[1] - b_l_knee_kolen[1], a_l_hip_kolen[0] - b_l_knee_kolen[0])
            angle_left_kolen = np.abs(radians_left_golen * 180 // np.pi)
            if 0 < angle_left_kolen > 180.0:
                angle_left_kolen = 360 - angle_left_kolen
                angle_left_kolen = 180 - angle_left_kolen
            angle_left_kolen -= 180
            angle_left_kolen *= -1
            list_angle_left_kolen_left_camera.append(angle_left_kolen)


            # Визуализация
            cv2.putText(image, str(angle_left_kolen),
                        tuple(np.multiply(l_knee_kolen, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )

            # Получение координат точек левого бедра
            l_shoulder_bed = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            l_hip_bed = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            l_knee_bed = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            # Калькулятор углов
            a_l_shoulder_bed = np.array(l_shoulder_bed)  # First
            b_l_hip_bed = np.array(l_hip_bed)  # Mid
            c_l_knee_bed = np.array(l_knee_bed)  # End
            radians_left_bed = np.arctan2(c_l_knee_bed[1] - b_l_hip_bed[1], c_l_knee_bed[0] - b_l_hip_bed[0]) - np.arctan2(a_l_shoulder_bed[1] - b_l_hip_bed[1], a_l_shoulder_bed[0] - b_l_hip_bed[0])
            angle_left_bed = np.abs(radians_left_bed * 360 // np.pi)
            if angle_left_bed > 180.0:
                angle_left_bed = 360 - angle_left_bed
            print(angle_left_bed)
            list_angle_left_bed_left_camera.append(angle_left_bed)

            # Визуализация
            cv2.putText(image, str(angle_left_bed),
                        tuple(np.multiply(l_hip_bed, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )


        except:
            pass
            # рендер детекции
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('left camera', image)

        # Завершает процесс qпо истечении 30 секунд
        if cv2.waitKey(10) & 0xFF == ord('q') or time.monotonic() - a > 30:
            stop += 1
            break

    cap.release()
    cv2.destroyAllWindows()

# Создание таблицы с параметрами ключевых точек
dict1 = {
    'Левый голеностоп': list_angle_left_golen_left_camera,
    'Левая коленка': list_angle_left_kolen_left_camera,
    'Левый тазобедренный сустав':list_angle_left_bed_left_camera
}
df = pd.DataFrame(dict1)

# Максимальное, минимальное, среднее значение для всех ключевых точек
globlist_left_camera = (df['Левый голеностоп'].mean(), df['Левый голеностоп'].min(), df['Левый голеностоп'].max(), df['Левая коленка'].mean(), df['Левая коленка'].min(), df['Левая коленка'].max(), df['Левый тазобедренный сустав'].mean(), df['Левый тазобедренный сустав'].min(), df['Левый тазобедренный сустав'].max())
# Запись полученных максимальных, минимальных, средних значений в текстовый файл
my_file1 = open(fr'C:\left_camera.txt', 'w+')
my_file1.write(f'{globlist_left_camera}')
my_file1.close()
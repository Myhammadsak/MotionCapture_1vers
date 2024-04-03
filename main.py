###библиотеки########################################
import asyncio
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import json
import easygui
import matplotlib.pyplot as plt
import numpy as np
from cv2_enumerate_cameras import enumerate_cameras
####################################################




###базовые переменные##############################
tit = 'STEP CARTOGRAPHER'
name_pap = 0
par_r = [0]*9
par_l = [0]*9
par_f = [0]*6
###################################################




###Главное окно####################################
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        ###Загрузка окна
        uic.loadUi('menu.ui', self)
        ###Название окна
        self.setWindowTitle(tit)

        ###Размеры окна
        self.setFixedWidth(820)
        self.setFixedHeight(550)

        ###Кнопки
        self.pushButton_3.clicked.connect(self.off)
        self.pushButton.clicked.connect(self.go)
        self.pushButton_4.clicked.connect(self.seti1)
        self.pushButton_5.clicked.connect(self.go_to_res)

    ### открывает класс запуска процесса
    def go(self):
        self.goo = Go()
        self.goo.show()
        Window.close(self)

    ### открывает класс настроек
    def seti1(self):
        self.seti = Seti()
        self.seti.show()
        Window.close(self)

    ### Переходит к результатам
    def go_to_res(self):
        self.res = Results()
        self.res.show()
        Window.close(self)

    ### завершает программу
    def off(self):
        sys.exit()
##################################################




###Класс настроек#################################
class Seti(QMainWindow):
    def __init__(self):
        super().__init__()
        ###Загрузка окна
        uic.loadUi('Seti.ui', self)
        ###Название окна
        self.setWindowTitle(tit)
        ###Размеры окна
        self.setFixedWidth(900)
        self.setFixedHeight(950)

        ###Добавление в список возможных камер
        cameras = []
        for camera_info in enumerate_cameras():
            cameras.append(f'{camera_info.index}: {camera_info.name}')
        for i in range(len(cameras)//2 - 1):
            self.listWidget.addItem(f'{cameras[i]}\n')
        self.num_index_prov = len(cameras)

        ###выбор камер
        ###читает json файл и устанваливаетв спинбоксы свои параметры
        with open('camera_index.json') as fcc_file:
            self.index_cam = json.load(fcc_file)
        self.spinBox.setValue(self.index_cam["ri"])
        self.spinBox_2.setValue(self.index_cam["le"])
        self.spinBox_3.setValue(self.index_cam["fr"])

        ###Кнопки
        self.pushButton_2.clicked.connect(self.boss_window)
        self.pushButton.clicked.connect(self.save_camera)



    ###Закрывает это окно и переходит в главное меню
    def boss_window(self):
        self.window = Window()
        self.window.show()
        Seti.close(self)

    ###Сохраняет выбранные индексы камер и выходит в меню
    def save_camera(self):
        if (self.spinBox.value() == self.spinBox_2.value() or self.spinBox_2.value() == self.spinBox_3.value()
                or self.spinBox.value() == self.spinBox_3.value()):
            QMessageBox.information(
                self,
                "Error",
                "Неверные индексы")
        else:
            #сохранят в json файл значения которые установил пользователь
            self.index_cam["ri"] = self.spinBox.value()
            self.index_cam["le"] = self.spinBox_2.value()
            self.index_cam["fr"] = self.spinBox_3.value()
            with open("camera_index.json", "wt", encoding="utf-8") as file:
                json.dump(self.index_cam, file, indent=1)

        self.window = Window()
        self.window.show()
        Seti.close(self)
##################################################




###Класс запуска процесса#########################
class Go(QMainWindow):
    def __init__(self):
        super().__init__()
        ###Загрузка окна
        uic.loadUi('go1.ui', self)
        ###Название окна
        self.setWindowTitle(tit)
        ###Раземры окна
        self.setFixedWidth(370)
        self.setFixedHeight(490)

        ###Изображение
        self.pixmap = QPixmap('nn.png')
        self.image = QLabel(self)
        self.image.move(40, 60)
        self.image.resize(300, 300)
        ###Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

        ###Кнопки
        self.go.clicked.connect(self.start1)

    ###Функция запуска главного процесса с mediapipe
    def start1(self):
        self.name_pap = self.lineEdit.text()
        global name_pap
        name_pap = self.name_pap
        a = []
        for i in range(len(self.name_pap)):
            if self.name_pap[i] == " ":
                pass
            else:
                a.append(1)
        if len(a) == 0:
            QMessageBox.information(
                self,
                "Error",
                "Название папки некорректно")

        else:
            os.mkdir(fr'C:\{self.name_pap}')

            self.go.hide()
            self.lineEdit.hide()

            try:
                SCRIPTS = [
                    'left_camera.py',
                    'right_camera.py',
                    'the_front_camera.py'
                ]

                async def waiter(sc, p):
                    "Функция которая вернет имя скрипта после ожидания"
                    await p.wait()
                    return sc, p

                async def main():
                    waiters = []

                    # Запуск
                    for sc in SCRIPTS:
                        p = await asyncio.create_subprocess_exec(sys.executable, sc)
                        print('Started', sc)
                        waiters.append(asyncio.create_task(waiter(sc, p)))

                    # Ожидание
                    while waiters:
                        done, waiters = await asyncio.wait(waiters, return_when=asyncio.FIRST_COMPLETED)
                        for w in done:
                            sc, p = await w
                            print('Done', sc)

                if __name__ == "__main__":
                    asyncio.run(main())

            except:
                pass
        self.go_2.clicked.connect(self.ggo)

    ###Функция перемещения текстовых файлов в персональную папку
    def ggo(self):
        ###Текстовые файлы
        os.rename(fr'C:\the_front_camera.txt', fr'C:\{self.name_pap}\the_front_camera.txt')
        os.rename(fr'C:\left_camera.txt', fr'C:\{self.name_pap}\left_camera.txt')
        os.rename(fr'C:\right_camera.txt', fr'C:\{self.name_pap}\right_camera.txt')

        self.res = Results()
        self.res.show()
        Go.close(self)
##########################################




###Класс конечного меню##########################
class Results(QMainWindow, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        ###Загрузка окна
        uic.loadUi('Results.ui', self)
        ###Название окна
        self.setWindowTitle(tit)
        ###Размеры окна
        self.setFixedWidth(1080)
        self.setFixedHeight(600)

        ###Кнопки
        self.Srav.clicked.connect(self.file_srav)
        self.Tabl.clicked.connect(self.table)
        self.resiltatbut.clicked.connect(self.resultab)
        self.pushButton.clicked.connect(self.go_to_menu)
        self.diag.clicked.connect(self.diagramm)

    def diagramm(self):
        ###Выносим списки из баззовых переменных
        global par_r, par_l, par_f

        if name_pap == 0:
            QMessageBox.information(
                self,
                "Error",
                "Вы не назначили персональную папку")
            return
        else:
            ###Переменные для таблицы
            #значения с правой камеры
            file = open(fr'C:\{name_pap}\right_camera.txt', 'r')
            c = file.read().strip('()').split(', ')
            #Проверяем список на пустоту
            if c[0] == 'nan':
                par_r = par_r
            else:
                par_r = (list(map(float, c)))

            #значения с передней камеры
            file = open(fr'C:\{name_pap}\the_front_camera.txt', 'r')
            c = file.read().strip('()').split(', ')
            #Проверяем список на пустоту
            if c[0] == 'nan':
                par_f = par_f
            else:
                par_f = (list(map(float, c)))

            #значения с левой камеры
            file = open(fr'C:\{name_pap}\left_camera.txt', 'r')
            c = file.read().strip('()').split(', ')
            # Проверяем список на пустоту
            if c[0] == 'nan':
                par_l = par_l
            else:
                par_l = (list(map(float, c)))

        cat_par = ['ПС.ТС', 'ЛС.ТС', 'ПС.КС',
                   'ЛС.КС', 'ПС.ГС', 'ЛС.ГС',
                   'ФП.ТС', 'ФЛ.ТС']
        g1 = [par_r[8], par_l[8], par_r[5], par_l[5], par_r[2], par_l[2], par_f[2], par_f[5]]
        g2 = [39, 39, 49, 49, 22, 22, 5, 5]
        width = 0.3
        x = np.arange(len(cat_par))
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width / 2, g1, width, label='Пациент')
        rects2 = ax.bar(x + width / 2, g2, width, label='Усл. здоровый')
        ax.set_title('Результаты в диаграмме')
        ax.set_xticks(x)
        ax.set_xticklabels(cat_par)
        ax.legend()
        plt.show()

    ###Выбор файла для сравнения
    def file_srav(self):
        input_file = easygui.diropenbox()
        global name_pap
        name_pap = input_file[3:]

    ###Переход в окно с таблицами
    def table(self):
        if name_pap == 0:
            QMessageBox.information(
                self,
                "Error",
                "Вы не назначили персональную папку")
            return
        self.table = Table()
        self.table.show()
        Results.close(self)

    ###Переход к окну с результатами
    def resultab(self):
        if name_pap == 0:
            QMessageBox.information(
                self,
                "Error",
                "Вы не назначили персональную папку")
            return
        self.retab = Restabe()
        self.retab.show()
        Results.close(self)

    ### Обратно в главное иеню
    def go_to_menu(self):
        #При выходе в главное меню обнуляем name_pap
        global name_pap
        name_pap = 0
        self.win = Window()
        self.win.show()
        Results.close(self)
######################################################




###Класс окна с таблицами#############################
class Table(QMainWindow):
    def __init__(self):
        super().__init__()
        ###Загрузка окна
        uic.loadUi('Table.ui', self)
        ###Название окна
        self.setWindowTitle(tit)
        ###Размеры окна
        self.setFixedWidth(950)
        self.setFixedHeight(500)
        ###Выносим списки из баззовых переменных
        global par_r, par_l, par_f

        ### Присваеваем значения сагитальной таблице пациента
        self.tableWidget.setItem(0, 0, QTableWidgetItem(f'{par_r[8]}')) # правый тазобедренный сустав
        self.tableWidget.setItem(0, 1, QTableWidgetItem(f'{par_l[8]}')) # левый тазобедренный сустав
        self.tableWidget.setItem(1, 0, QTableWidgetItem(f'{par_r[5]}')) # правый коленный сустав
        self.tableWidget.setItem(1, 1, QTableWidgetItem(f'{par_l[5]}')) # левый коленный сустав
        self.tableWidget.setItem(2, 0, QTableWidgetItem(f'{par_r[2]}')) # правый голнестопный сустав
        self.tableWidget.setItem(2, 1, QTableWidgetItem(f'{par_l[2]}')) # левый голеностопный сустав

        ### Присваеваем значения сагитальной таблице условно здорового
        self.tableWidget_3.setItem(0, 0, QTableWidgetItem(f'{39}')) # правый тазобедренный сустав
        self.tableWidget_3.setItem(0, 1, QTableWidgetItem(f'{39}')) # левый тазобедренный сустав
        self.tableWidget_3.setItem(1, 0, QTableWidgetItem(f'{49}')) # правый коленный сустав
        self.tableWidget_3.setItem(1, 1, QTableWidgetItem(f'{49}')) # левый коленный сустав
        self.tableWidget_3.setItem(2, 0, QTableWidgetItem(f'{22}')) # правый голнестопный сустав
        self.tableWidget_3.setItem(2, 1, QTableWidgetItem(f'{22}')) # левый голеностопный сустав

        ### Присваеваем значения фронтальной таблице пациента
        self.tableWidget_2.setItem(0, 0, QTableWidgetItem(f'{par_f[2]}')) # правый тазобедренный сустав
        self.tableWidget_2.setItem(0, 1, QTableWidgetItem(f'{par_f[5]}')) # левый тазобедренный сустав

        ### Присваеваем значения фронтальной таблице условно здорового
        self.tableWidget_4.setItem(0, 0, QTableWidgetItem(f'{5}')) # правый тазобедренный сустав
        self.tableWidget_4.setItem(0, 1, QTableWidgetItem(f'{5}')) # левый тазобедренный сустав

        ###Кнопки
        self.pushButton.clicked.connect(self.ex_res)
        self.pushButton_2.clicked.connect(self.tablr_srav)

    ###Выход обратно в конечное меню
    def ex_res(self):
        self.res = Results()
        self.res.show()
        Table.close(self)

    ###Открытие окна сравнения таблиц
    def tablr_srav(self):
        self.tsrav = Tsrav()
        self.tsrav.show()
        Table.close(self)
#############################################




###Окно результатов сравнения################
class Tsrav(QMainWindow):
    def __init__(self):
        super().__init__()
        ###Загрузка окна
        uic.loadUi('Table_srav.ui', self)
        ###Название окна
        self.setWindowTitle(tit)
        ###Размеры окна
        self.setFixedWidth(400)
        self.setFixedHeight(500)
        ###Выносим списки из баззовых переменных
        global par_r, par_l, par_f

        ### Присваеваем значения сагитальной сравнительной таблице
        self.tableWidget.setItem(0, 0, QTableWidgetItem(f'{par_r[8] - 39}'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(f'{par_l[8] - 39}'))
        self.tableWidget.setItem(1, 0, QTableWidgetItem(f'{par_r[5] - 49}'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem(f'{par_l[5] - 49}'))
        self.tableWidget.setItem(2, 0, QTableWidgetItem(f'{par_r[2] - 22}'))
        self.tableWidget.setItem(2, 1, QTableWidgetItem(f'{par_l[2] - 22}'))

        ### Присваеваем значения фронтальной сравнительной таблице
        self.tableWidget_2.setItem(0, 0, QTableWidgetItem(f'{par_f[2] - 5}'))
        self.tableWidget_2.setItem(0, 1, QTableWidgetItem(f'{par_f[5] - 5}'))

        ###Кнопки
        self.pushButton_2.clicked.connect(self.ex_res)
        self.pushButton.clicked.connect(self.table)

    ### Открывает прошлое окно с таблицами
    def table(self):
        self.table = Table()
        self.table.show()
        Tsrav.close(self)

    ### Открывает конечное меню
    def ex_res(self):
        self.res = Results()
        self.res.show()
        Tsrav.close(self)
#############################################





###окно с результатами в таблице#############
class Restabe(QMainWindow):
    def __init__(self):
        super().__init__()
        ###Загрузка окна
        uic.loadUi('Res_pac.ui', self)
        ###Название окна
        self.setWindowTitle(tit)
        ###Размеры окна
        self.setFixedWidth(600)
        self.setFixedHeight(450)
        ###Выносим базовые переменные
        global par_r, par_l, par_f

        ### Присваеваем значения фронтальной части таблицы
        self.tableWidget.setItem(0, 0, QTableWidgetItem(f'{par_f[0]}')) # правое среднее тазобедренного сустава
        self.tableWidget.setItem(0, 1, QTableWidgetItem(f'{par_f[2]}')) # правое максимальное тазобедренного сустава
        self.tableWidget.setItem(0, 2, QTableWidgetItem(f'{par_f[1]}')) # правое минимальное тазобедренного сустава
        self.tableWidget.setItem(1, 0, QTableWidgetItem(f'{par_f[3]}')) # левое среднее тазобедренного сустава
        self.tableWidget.setItem(1, 1, QTableWidgetItem(f'{par_f[5]}')) # левое максимальное тазобедренного сустава
        self.tableWidget.setItem(1, 2, QTableWidgetItem(f'{par_f[4]}')) # левое минимальное тазобедренного сустава

        ### Присваеваем значения сагитальной части таблицы
        self.tableWidget.setItem(2, 0, QTableWidgetItem(f'{par_r[6]}')) # правое среднее тазобедренного сустава
        self.tableWidget.setItem(2, 1, QTableWidgetItem(f'{par_r[8]}')) # правое максимальное тазобедренного сустава
        self.tableWidget.setItem(2, 2, QTableWidgetItem(f'{par_r[7]}')) # правое минимальное тазобедренного сустава
        self.tableWidget.setItem(3, 0, QTableWidgetItem(f'{par_l[6]}')) # левое среднее тазобедренного сустава
        self.tableWidget.setItem(3, 1, QTableWidgetItem(f'{par_l[8]}')) # левое максимальное тазобедренного сустава
        self.tableWidget.setItem(3, 2, QTableWidgetItem(f'{par_l[7]}')) # левое минимальное тазобедренного сустава
        self.tableWidget.setItem(4, 0, QTableWidgetItem(f'{par_r[3]}')) # правое среднее тазобедренного сустава
        self.tableWidget.setItem(4, 1, QTableWidgetItem(f'{par_r[5]}')) # правое максимальное тазобедренного сустава
        self.tableWidget.setItem(4, 2, QTableWidgetItem(f'{par_r[4]}')) # правое минимальное тазобедренного сустава
        self.tableWidget.setItem(5, 0, QTableWidgetItem(f'{par_l[3]}')) # левое среднее тазобедренного сустава
        self.tableWidget.setItem(5, 1, QTableWidgetItem(f'{par_l[5]}')) # левое максимальное тазобедренного сустава
        self.tableWidget.setItem(5, 2, QTableWidgetItem(f'{par_l[4]}')) # левое минимальное тазобедренного сустава
        self.tableWidget.setItem(6, 0, QTableWidgetItem(f'{par_r[0]}')) # правое среднее тазобедренного сустава
        self.tableWidget.setItem(6, 1, QTableWidgetItem(f'{par_r[2]}')) # правое максимальное тазобедренного сустава
        self.tableWidget.setItem(6, 2, QTableWidgetItem(f'{par_r[1]}')) # правое минимальное тазобедренного сустава
        self.tableWidget.setItem(7, 0, QTableWidgetItem(f'{par_l[0]}')) # левое среднее тазобедренного сустава
        self.tableWidget.setItem(7, 1, QTableWidgetItem(f'{par_l[2]}')) # левое максимальное тазобедренного сустава
        self.tableWidget.setItem(7, 2, QTableWidgetItem(f'{par_l[1]}')) # левое минимальное тазобедренного сустава

        ### Кнопка выхода
        self.pushButton.clicked.connect(self.ex_resq)

    ### Выход в меню результатов
    def ex_resq(self):
        self.res = Results()
        self.res.show()
        Restabe.close(self)
#############################################




###запуск программы##########################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
#############################################
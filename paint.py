from tkinter import *


class Paint(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setGUI()

    def setGUI(self):
        self.parent.title("Easy Paint")
        self.pack(fill=BOTH, expand=1)  # Размещаем активные элементы на родительском окне

        self.canv = Canvas(self, bg="white")  # Создаем поле для рисования, устанавливаем белый фон

        color_lab = Label(self, text="Color: ")  # Создаем метку для кнопок изменения цвета кисти
        red_btn = Button(self, text="Red", width=10)  # Создание кнопки:  Установка текста кнопки,
        # задание ширины кнопки (10 символов)
        green_btn = Button(self, text="Green", width=10)
        blue_btn = Button(self, text="Blue", width=10)
        black_btn = Button(self, text="Black", width=10)
        white_btn = Button(self, text="White", width=10)

        size_lab = Label(self, text="Brush size: ")  # Создаем метку для кнопок изменения размера кисти
        btn_1 = Button(self, text="Size 1", width=10)
        btn_2 = Button(self, text="Size 2", width=10)
        btn_3 = Button(self, text="Size 3", width=10)
        btn_4 = Button(self, text="Size 4", width=10)
        btn_5 = Button(self, text="Size 5", width=10)
        btn_6 = Button(self, text="Size 6", width=10)
        btn_7 = Button(self, text="Size 7", width=10)

        self.columnconfigure(8, weight=1)  # Даем седьмому столбцу возможность растягиваться,
        # благодаря чему кнопки не будут разъезжаться при ресайзе
        self.rowconfigure(2, weight=1)  # То же самое для третьего ряда
        self.canv.grid(row=2, column=0, columnspan=9,
                       padx=5, pady=5,
                       sticky=E + W + S + N)  # Прикрепляем канвас методом grid.
        # Он будет находится в 3м ряду, первой колонке, и будет занимать 7 колонок,
        # задаем отступы по X и Y в 5 пикселей, и заставляем растягиваться при
        # растягивании всего окна
        color_lab.grid(row=0, column=0, padx=6)  # Устанавливаем созданную метку в первый ряд и первую
        # колонку, задаем горизонтальный отступ в 6 пикселей
        red_btn.grid(row=0, column=1)  # Устанавливаем кнопку первый ряд, вторая колонка
        green_btn.grid(row=0, column=2)
        blue_btn.grid(row=0, column=3)
        black_btn.grid(row=0, column=4)
        white_btn.grid(row=0, column=5)
        size_lab.grid(row=1, column=0, padx=5)
        btn_1.grid(row=1, column=1)
        btn_2.grid(row=1, column=2)
        btn_3.grid(row=1, column=3)
        btn_4.grid(row=1, column=4)
        btn_5.grid(row=1, column=5)
        btn_6.grid(row=1, column=6)
        btn_7.grid(row=1, column=7, sticky=W)


def main():
    root = Tk()
    root.geometry("1920x1080+300+300")
    app = Paint(root)
    root.mainloop()

main()
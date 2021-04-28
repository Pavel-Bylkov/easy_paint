from tkinter import *
from tkinter import filedialog, colorchooser
import io
from PIL import ImageGrab, ImageTk, Image   # pip install pillow
from constants import COLORS

# ToDo Доделать открытие файла (Открытие для редактирования)


class MyEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class QueueActions:
    def __init__(self):
        self.actions = {}
        self.starts = []
        self.ends = []
        self.n_action = 0

    def add(self, action, value):
        self.actions[self.n_action] = (action, value)
        self.n_action += 1

    def add_start_draw(self, event):
        self.starts.append(self.n_action)

    def add_end_draw(self, event):
        self.ends.append(self.n_action - 1)

    def is_not_empty(self):
        return self.n_action > 0

    def remove_last(self):
        self.n_action -= 1
        action, value = self.actions[self.n_action] if self.n_action in self.actions else (None, None)
        if 'draw' == action:
            self.n_action = self.starts.pop()
            for n_do in range(self.n_action, self.ends.pop() + 1):
                del self.actions[n_do]
        else:
            del self.actions[self.n_action]

    def get_action_value(self, n_do):
        if n_do in self.actions:
            return self.actions[n_do]
        return None, None

    def len(self):
        return self.n_action


class Paint(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.queve = QueueActions()
        self.sv = StringVar()
        self.setGUI()
        self.start_size()
        self.connects()

    def save_image(self):
        filename = self.sv.get()
        if filename:
            filename += ".jpg"
        else:
            filename = "image.jpg"
        ps = self.canv.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save(filename, 'jpeg')

    def save_image_dialog(self):
        ftypes = [('Графичиские файлы', '*.jpg'), ('Все файлы', '*')]
        dlg = filedialog.SaveAs(self, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':
            ps = self.canv.postscript(colormode='color')
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            img.save(fl, 'jpeg')

    def start_size(self):
        self.brush_size = 10
        self.brush_color = "black"
        self.color_frame.config(bg="black")

    def connects(self):
        self.canv.bind("<Button-1>", self.queve.add_start_draw)
        self.canv.bind("<B1-Motion>", self.draw)
        self.canv.bind("<ButtonRelease-1>", self.queve.add_end_draw)
        self.set_any_color.bind('<Return>', self.callback)

    def setGUI(self):
        self.parent.title("Easy Paint")
        self.pack(fill=BOTH, expand=1)  # Размещаем активные элементы на родительском окне

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = Menu(menubar)
        file_menu.add_command(label="Открыть", command=self.onOpen)
        file_menu.add_command(label="Сохранить как", command=self.save_image_dialog)
        menubar.add_cascade(label="Файл", menu=file_menu)
        edit_menu = Menu(menubar)
        edit_menu.add_command(label="Выбрать цвет", command=self.onChoose)
        menubar.add_cascade(label="Редактировать", menu=edit_menu)

        self.canv = Canvas(self, bg="white")  # Создаем поле для рисования, устанавливаем белый фон

        color_lab = Label(self, text="Color: ")  # Создаем метку для кнопок изменения цвета кисти
        self.color_frame = Frame(self, border=1, relief=SUNKEN, width=30, height=30)
        red_btn = Button(self, text="Red", width=10, command=lambda: self.set_color("red"),  bg='red', fg='black')
        # Создание кнопки:  Установка текста кнопки, задание ширины кнопки (10 символов)
        green_btn = Button(self, text="Green", width=10, command=lambda: self.set_color("green"), bg='green', fg='black')
        blue_btn = Button(self, text="Blue", width=10, command=lambda: self.set_color("blue"), bg='blue', fg='black')
        black_btn = Button(self, text="Black", width=10, command=lambda: self.set_color("black"), bg='black', fg='white')
        white_btn = Button(self, text="White", width=10, command=lambda: self.set_color("white"), bg='white', fg='black')
        clear_btn = Button(self, text="Clear", width=10, command=lambda: self.clear())
        set_any_color_lb = Label(self, text="Enter your color: ")
        self.set_any_color = Entry(self, width=30, textvariable=self.sv)

        size_lab = Label(self, text="Brush size: ")  # Создаем метку для кнопок изменения размера кисти
        btn_1 = Button(self, text="Size 1", width=10, command=lambda: self.set_size(1))
        btn_2 = Button(self, text="Size 2", width=10, command=lambda: self.set_size(2))
        btn_3 = Button(self, text="Size 3", width=10, command=lambda: self.set_size(5))
        btn_4 = Button(self, text="Size 4", width=10, command=lambda: self.set_size(10))
        btn_5 = Button(self, text="Size 5", width=10, command=lambda: self.set_size(15))
        btn_6 = Button(self, text="Size 6", width=10, command=lambda: self.set_size(20))
        btn_7 = Button(self, text="Size 7", width=10, command=lambda: self.set_size(50))
        undo_btn = Button(self, text="Un do last action", width=20, command=lambda: self.undo())
        save_lab = Label(self, text="Save image as: ")
        self.set_filename = Entry(self, width=30, textvariable=self.sv)
        save_btn = Button(self, text="SAVE", width=20, command=lambda: self.save_image())

        self.columnconfigure(11, weight=1)  # Даем седьмому столбцу возможность растягиваться,
        # благодаря чему кнопки не будут разъезжаться при ресайзе
        self.rowconfigure(2, weight=1)  # То же самое для третьего ряда
        self.canv.grid(row=2, column=0, columnspan=12,
                       padx=5, pady=5,
                       sticky=E + W + S + N)  # Прикрепляем канвас методом grid.
        # Он будет находится в 3м ряду, первой колонке, и будет занимать 7 колонок,
        # задаем отступы по X и Y в 5 пикселей, и заставляем растягиваться при
        # растягивании всего окна
        color_lab.grid(row=0, column=0, padx=6)  # Устанавливаем созданную метку в первый ряд и первую
        # колонку, задаем горизонтальный отступ в 6 пикселей
        self.color_frame.grid(row=0, column=1)
        red_btn.grid(row=0, column=2)  # Устанавливаем кнопку первый ряд, вторая колонка
        green_btn.grid(row=0, column=3)
        blue_btn.grid(row=0, column=4)
        black_btn.grid(row=0, column=5)
        white_btn.grid(row=0, column=6)
        clear_btn.grid(row=0, column=7)
        set_any_color_lb.grid(row=0, column=8)
        self.set_any_color.grid(row=0, column=9, sticky=W)
        size_lab.grid(row=1, column=0, padx=5)
        btn_1.grid(row=1, column=1)
        btn_2.grid(row=1, column=2)
        btn_3.grid(row=1, column=3)
        btn_4.grid(row=1, column=4)
        btn_5.grid(row=1, column=5)
        btn_6.grid(row=1, column=6)
        btn_7.grid(row=1, column=7)
        undo_btn.grid(row=1, column=8)
        save_lab.grid(row=1, column=9)
        self.set_filename.grid(row=1, column=10)
        save_btn.grid(row=1, column=11, sticky=W)

    def draw(self, event):
        self.queve.add('draw', MyEvent(event.x, event.y))
        self.draw_copy(event)

    def set_color(self, new_color):
        self.queve.add('set_color', new_color)
        self.set_color_copy(new_color)

    def callback(self, event):
        text = self.sv.get()
        if text in COLORS:
            self.set_color(text)
        else:
            try:
                if ('#' == text[0] and len(text) == 7):
                    self.set_color(text)
            except:
                pass

    def set_size(self, new_size):
        self.queve.add('set_size', new_size)
        self.set_size_copy(new_size)

    def clear(self):
        self.queve.add('clear', 0)
        self.clear_copy()

    def undo(self):
        if self.queve.is_not_empty():
            self.queve.remove_last()
            self.start_size()
            self.canv.delete("all")
            for n_do in range(self.queve.len()):
                action, value = self.queve.get_action_value(n_do)
                if action == 'draw':
                    self.draw_copy(value)
                elif action == 'set_color':
                    self.set_color_copy(value)
                elif action == 'set_size':
                    self.set_size_copy(value)
                elif action == 'clear':
                    self.clear_copy()

    def draw_copy(self, event):
        self.canv.create_oval(event.x - self.brush_size,
                              event.y - self.brush_size,
                              event.x + self.brush_size,
                              event.y + self.brush_size,
                              fill=self.brush_color, outline=self.brush_color)

    def set_color_copy(self, new_color):
        self.brush_color = new_color
        self.color_frame.config(bg=new_color)

    def set_size_copy(self, new_size):
        self.brush_size = new_size

    def clear_copy(self):
        self.canv.delete("all")

    def onOpen(self):
        ftypes = [('Графичиские файлы', '*.jpg'), ('Все файлы', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':
            self.queve.add('load', 0)
            tmp_image = self.load_image(fl)
            self.image = self.canv.create_image(self.canv.winfo_width(), self.canv.winfo_height(), image=tmp_image)
            self.canv.grid(row=2, column=0, columnspan=12,
                           padx=5, pady=5,
                           sticky=E + W + S + N)

    def load_image(self, filename):  # https://www.c-sharpcorner.com/Blogs/basics-for-displaying-image-in-tkinter-python
        # https://stackoverflow.com/questions/49308962/how-to-insert-an-image-using-canvas-in-tkinter
        img = ImageTk.PhotoImage(Image.open(filename))
        return img

    def onChoose(self):
        (rgb, hx) = colorchooser.askcolor()
        self.set_color(hx)


def main():
    root = Tk()
    root.geometry("1920x1080+300+300")
    app = Paint(root)
    root.mainloop()

main()
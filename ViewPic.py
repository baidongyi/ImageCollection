import tkinter as tk
from PIL import Image
from PIL import ImageTk
import random
from src.lib_share import *


def clear_folder(folder: str):
    file_list = os.listdir(folder)
    for file in file_list:
        os.remove(os.path.join(folder, file))
    wl('clear folder => ' + folder, 1)


def is_folder_update_lately(folder_test: str) -> bool:
    days = os.stat(folder_test).st_mtime / 365 / 24
    return days > 18160


class PicLib:
    folder_list = []
    mark = False
    folder_count = 0
    isEmpty = False

    def refresh_folder_list(self):
        self.__init__(self.base_folder, self.keyword)

    def __init__(self, base_folder: str, keyword: str):
        self.base_folder = base_folder
        self.keyword = keyword
        self.folder_list = []

        for one_folder in os.listdir(self.base_folder):
            full_folder_path = os.path.join(self.base_folder, one_folder)
            if len(self.keyword) > 0:
                if one_folder.find(self.keyword) >= 0 and is_folder_update_lately(full_folder_path):
                    self.folder_list.append(full_folder_path)
            else:
                if is_folder_update_lately(full_folder_path):
                    self.folder_list.append(full_folder_path)

        self.folder_count = len(self.folder_list)
        self.isEmpty = (self.folder_count == 0)
        if self.isEmpty:
            print('isEmpty = True')
            return

        self.folder_index = random.randint(1, self.folder_count - 1)
        self.curr_folder = self.folder_list[self.folder_index]
        self.file_list = os.listdir(self.curr_folder)
        self.file_index = 1

    def get_next_folder(self) -> str:
        if not self.isEmpty:
            self.folder_index = (self.folder_index + 1) % self.folder_count
            self.curr_folder = self.folder_list[self.folder_index]
            return self.curr_folder

    def get_next_image(self, folder_offset: int, file_offset: int):
        if folder_offset > 0:
            self.refresh_folder_list()
            self.folder_index = random.randint(0, self.folder_count - 1)
            self.curr_folder = self.folder_list[self.folder_index]
            self.file_list = os.listdir(self.curr_folder)
            self.file_index = 1
            if len(self.file_list) == 0:
                return self.get_next_image(1, 0)

        self.file_index = (self.file_index + file_offset) % len(self.file_list)

        file_path = os.path.join(self.folder_list[self.folder_index], self.file_list[self.file_index - 1])
        try:
            my_image = Image.open(file_path)
        except:
            os.remove(file_path)
            wl('delete file => ' + file_path)
            my_image = self.get_next_image(0, 1)

        return my_image

    def get_photo_image(self, folder_offset: int, file_offset: int) -> tk.PhotoImage:
        img = self.get_next_image(folder_offset, file_offset)
        fix_height = 900

        [width, height] = img.size
        if height != fix_height:
            wl('before =' + str(width) + ' ' + str(height), 3)
            width = int(fix_height / height * width)
            height = fix_height
            img = img.resize((width, height))
            wl('after =' + str(width) + ' ' + str(height), 3)
        return ImageTk.PhotoImage(img)

    def remove_curr_folder(self):

        if self.curr_folder.find('pass') > 0:
            return

        if self.curr_folder[-1:] in ('+', '-'):
            new_name = self.curr_folder[:-1] + '-'
        else:
            new_name = self.curr_folder + '-'

        os.rename(self.curr_folder, new_name)
        wl('rename Bad=> ' + new_name, 1)
        clear_folder(new_name)

    def mark_good_curr_folder(self):
        if self.curr_folder[-1:] in ('+', '-'):
            new_name = self.curr_folder[:-1] + '+'
        else:
            new_name = self.curr_folder + '+'

        os.rename(self.curr_folder, new_name)
        wl('rename Good => ' + new_name, 1)


def set_image(cv: tk.Canvas, my_label: tk.Label, my_pic_lib: PicLib, folder_offset: int, file_offset: int):
    photo = my_pic_lib.get_photo_image(folder_offset, file_offset)
    cv.create_image(0, 0, image=photo, anchor='nw')
    cv.image = photo
    my_label.configure(text=my_pic_lib.curr_folder, justify='left')


def remove_image(cv: tk.Canvas, my_label: tk.Label, my_pic_lib: PicLib):
    my_pic_lib.remove_curr_folder()
    set_image(cv, my_label, my_pic_lib, 1, 0)


def mark_good_image(cv: tk.Canvas, my_label: tk.Label, my_pic_lib: PicLib):
    my_pic_lib.mark_good_curr_folder()
    set_image(cv, my_label, my_pic_lib, 1, 0)


def view_image(series: str, keyword: str):
    base_path = os.path.join(get_base_folder(), series)

    my_pic_lib = PicLib(base_path, keyword)

    root = tk.Tk()
    cv = tk.Canvas(root)
    my_label = tk.Label(root)

    frame = tk.Frame(root, width=100, height=100)

    set_image(cv, my_label, my_pic_lib, 1, 1)

    my_label.pack(side='top')

    cv.pack(side='top', fill='both', expand='yes')

    cv.bind('<Button-1>', lambda event: set_image(cv, my_label, my_pic_lib, 0, 1))
    cv.bind('<Button-2>', lambda event: set_image(cv, my_label, my_pic_lib, 1, 0))
    cv.bind('<Button-3>', lambda event: set_image(cv, my_label, my_pic_lib, 1, 0))

    cv.bind('<MouseWheel>', lambda event: set_image(cv, my_label, my_pic_lib, 0, 1))

    cv.bind('<Button-4>', lambda event: set_image(cv, my_label, my_pic_lib, 0, -1))
    cv.bind('<Button-5>', lambda event: set_image(cv, my_label, my_pic_lib, 0, 1))

    frame.bind('<Left>', lambda event: set_image(cv, my_label, my_pic_lib, 0, -1))
    frame.bind('<Right>', lambda event: set_image(cv, my_label, my_pic_lib, 0, 1))
    frame.bind('<Down>', lambda event: set_image(cv, my_label, my_pic_lib, 1, 1))

    frame.focus_set()
    frame.pack()

    root.mainloop()


if __name__ == '__main__':
    keyword = '245'

    series = '18av'

    view_image(series, keyword)

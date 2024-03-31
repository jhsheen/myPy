import os
import shutil
import time
import glob
from PIL import Image
import pyautogui
import keyboard

class BookData:
    def __init__(self, book_data, xy_coords):
        self.book_data = book_data
        self.xy_coords = xy_coords
        [self.book_name, self.book_total, self.book_author, self.book_pages, self.tmp_path, self.book_path] = self.book_data
        [self.xa, self.ya, self.xb, self.yb, self.xc, self.yc, self.xd, self.yd] = self.xy_coords
        self.pdf_file_path = self.tmp_path + 'P_' + self.book_name + '/'

    def get_book_data(self):
        print('=========Get Book Data===============')
        self.book_name = input("Book Name: ")
        self.book_pages = int(input("Pages Of Book: "))
        self.book_path = self.tmp_path + self.book_name + '/'
        self.pdf_file_path = self.tmp_path + 'P_' + self.book_name + '/'
        return

    def copy_one_page(self):
        print('==========Copy One Page==============')
        image_path = self.book_path + self.book_name + '.png'
        if os.path.exists(self.book_path):
            shutil.rmtree(self.book_path)
        os.makedirs(self.book_path)
        pyautogui.screenshot(image_path, region=(self.xa, self.ya, self.xd, self.yd))
        image = Image.open(image_path)
        image.show()
        print("PNG file is ==>  " + image_path)
        return

    def copy_multiple_pages(self):
        print('========Copy Multiple Pages================')
        if os.path.exists(self.book_path):
            shutil.rmtree(self.book_path)
        os.makedirs(self.book_path)
        pyautogui.moveTo(self.xc, self.yc)
        pyautogui.click()
        time.sleep(1.0)

        for i in range(1, self.book_pages + 1):
            current_time = time.strftime('%m%d %H%M%S', time.localtime())
            file_name = self.book_path + self.book_name + current_time + '.png'
            pyautogui.moveTo(self.xc, self.yc)
            time.sleep(0.5)
            pyautogui.screenshot(file_name, region=(self.xa, self.ya, self.xd, self.yd))
            pyautogui.moveTo(self.xc, self.yc)
            pyautogui.press('right')
            time.sleep(0.5)
        print(f"{self.book_pages} pages copied ==>  ", self.book_path)
        print(file_name)
        return

    def get_xy(self):
        print('=========Get XY===============')
        print('1:XYt,2:XYb,3:XYc,4:end')
        i = 1
        while True:
            i += 1
            key_input = keyboard.read_key()
            if i % 2 == 0:
                x, y = pyautogui.position()
                if key_input == '1':
                    self.xa, self.ya = x, y
                elif key_input == '2':
                    self.xb, self.yb = x, y
                elif key_input == '3':
                    self.xc, self.yc = x, y
                elif key_input == '4':
                    break
                self.xd, self.yd = self.xb - self.xa, self.yb - self.ya
                self.xy_coords = [self.xa, self.ya, self.xb, self.yb, self.xc, self.yc, self.xd, self.yd]
                print(self.xy_coords)
        return self.xy_coords

    def images_to_pdf(self):
        print('=========Images to PDF===============')
        png_file_pattern = self.book_path + '*.png'
        if os.path.exists(self.pdf_file_path):
            shutil.rmtree(self.pdf_file_path)
        os.makedirs(self.pdf_file_path)
        png_file_list = glob.glob(png_file_pattern)
        count = 1
        for png_file_name in png_file_list:
            img_1 = Image.open(png_file_name)
            img_2 = img_1.convert('RGB')
            pdf_file_name = self.pdf_file_path + self.book_name + str('%04d' % count) + '.pdf'
            img_2.save(pdf_file_name)
            count = count + 1
        return

def main():
    book_name = 'ex'
    book_total = 'ex1'
    book_author = 'sheen'
    book_pages = 3
    tmp_path = 'c:/_Temp/'
    book_path = tmp_path + book_name + '/'
    book_data = [book_name, book_total, book_author, book_pages, tmp_path, book_path]
    xy_coords = [12, 67, 561, 854, 147, 324, 549, 787]

    print(book_data)
    print(xy_coords)
    book = BookData(book_data, xy_coords)

    while True:
        print('====================')
        prompt =  "*Select No."
        prompt += "\n*1:Book Data"
        prompt += "\n*2:Page Size"
        prompt += "\n*3:Copy 1 Page"
        prompt += "\n*4:Copy Multiple Pages (PDF)"
        prompt += "\n*5:Images => PDF"
        prompt += "\n*6:End"
        print('====================')
        prompt += "\nNumber? :"
        number = int(input(prompt))
        print('====================')

        if number == 1:
            book.get_book_data()
            print(book_data)
            print('====================')
        elif number == 2:
            xy_coords = book.get_xy()
            print('====================')
        elif number == 3:
            book.copy_one_page()
            print('====================')
        elif number == 4:
            book.copy_multiple_pages()
            book.images_to_pdf()
            print('====================')
        elif number == 5:
            book.images_to_pdf()
            print('====================')            
        else:            
            print("Thank You for using this program!")
            print('==================================')
            break

if __name__ == "__main__":
    main()


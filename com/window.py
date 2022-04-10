import shutil
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import time


def save(file_path: str, tags: list):
    """
    保存新的物品，并返回该物品的名称
    :param file_path: 图片所在路径
    :param tags: 物品的标签
    :return: 物品的图片的文件名,保存失败则返回-1
    """
    extends = file_path.split(".")[-1]
    now_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    out_path = "./data/picture/" + now_time + "." + extends
    # print(out_path)
    try:
        shutil.copy(file_path, out_path)
    except IOError:
        with open("./log", "wt") as log:
            log.write("Error " + now_time + ": Copy failed.\n")
            log.write("old_path:" + file_path + ", new_path:" + out_path + "\n")
        return -1
    with open("./data/data.dat", "a", encoding="utf-8") as f:
        f.write(now_time + "." + extends + " ")
        for t in tags:
            f.write(t + " ")
        f.write("\n")
    return now_time + "." + extends


class Create:
    height = 400
    width = 900
    tag_list = []
    file = None

    picture_file_types = (("JPEG", "*.jpg;*.jpeg;*.jpe;*.jfif"), ("GIF", "*.gif"), ("PNG", "*.png"))

    def __init__(self):

        self.all_goods = dict()  # 所有的物品的字典
        # 读入所有物品
        self.read_all_goods()

        self.now_result_goods_file = list(self.all_goods.keys())  # 当前匹配到的所有的物品的文件列表

        # 创建倒排索引
        self.word_file = dict()
        self.reverse_index()

        self.window = Tk()
        self.window.geometry("{}x{}".format(self.width, self.height))
        self.window.title("失物招领登记与查询系统")
        self.window.resizable(width=False, height=False)

        # 初始界面
        # 控件：两个Frame，标题标签（存放于一个Frame中）；选择说明标签与两个按钮（存放于另一个Frame中）
        #      备注：两个Frame以X填满窗口
        self.title_frame = Frame(self.window)
        self.title1 = Label(self.title_frame, text="欢迎来到失物招领登记与查询系统！", font=("黑体", 25))
        self.select_frame = Frame(self.window)
        self.title2 = Label(self.select_frame, text="请选择你的操作：", font=("黑体", 25))
        self.search = Button(self.select_frame, text="查找", font=("黑体", 15), command=self.search_clicked)
        self.save = Button(self.select_frame, text="登记", font=("黑体", 15), command=self.save_clicked)
        self.welcome_page()

        # 共用返回按钮
        self.back_frame = Frame(self.window, height=self.height)
        self.back = Button(self.back_frame, text="返回", font=("黑体", 15), command=self.back_clicked)

        # 登记界面
        # 控件：三个Frame。
        #      一个Frame放：一个返回按钮
        #      一个Frame放：一个选择文件按钮，一个用于显示已选文件的标签，一个用于展示已选文件图片的标签
        #      一个Frame放：一个用于输入tag的文本框，一个用于获取输入的tag的按钮
        #      备注：三个Frame以Y填满窗口
        self.file_select_frame = Frame(self.window, height=self.height)
        self.tag_frame = Frame(self.window, height=self.height)
        self.select_file = Button(self.file_select_frame, text="选择文件", font=("黑体", 15), command=self.selected_clicked)
        self.selected = Label(self.file_select_frame, width=50)
        self.show = Label(self.file_select_frame, width=350)
        self.tag_describe = Label(self.tag_frame, text="请输入描述标签（可输入多个，按回车存入）", font=("黑体", 13))
        self.tags = Entry(self.tag_frame, width=30, font=("黑体", 13))
        self.tags.bind("<Return>", self.return_pressed)
        self.recall = Button(self.tag_frame, text="撤销", font=("黑体", 13), command=self.recall_clicked)
        # self.tags_show = Label(self.tag_frame, bg="blue", width=50, height=10)
        self.tags_show = scrolledtext.ScrolledText(self.tag_frame, width=50, height=15, state=DISABLED)
        self.get_tags = Button(self.tag_frame, text="完成", font=("黑体", 15), command=self.get_clicked)

        # 查询界面
        # 控件：四个Frame。
        #      一个Frame放：一个返回按钮
        #      一个Frame放：一个用于输入关键词的文本框，一个接收关键词的按钮
        #      一个Frame放：展示的图片（一页六个）
        #      一个Frame放：换页按钮，当前页数与总页数的标签

        self.now_page = 0
        self.type_in_frame = Frame(self.window, width=self.width - 80)
        self.show_frame = Frame(self.window, width=self.width - 80)
        self.page_frame = Frame(self.window, width=self.width - 80)
        self.type_in_describe = Label(self.type_in_frame, text="输入关键词查找：", font=("黑体", 15))
        self.type_in = Entry(self.type_in_frame, width=60, font=("黑体", 13))

        self.done = Button(self.type_in_frame, text="搜索", font=("黑体", 15), command=self.search_goods_by_tag)
        self.pictures = [Label(self.show_frame, width=240, height=150, text="1") for i in
                         range(6)]  # 展示用label列表
        self.var_pages = IntVar()
        self.var_pages.set(1)
        self.up_page = Button(self.page_frame, text="上一页", font=("黑体", 11), command=self.pre_page)
        self.down_page = Button(self.page_frame, text="下一页", font=("黑体", 11), command=self.next_page)
        self.pages = Label(self.page_frame, textvariable=self.var_pages, font=("Times New Roman", 11))

        # 主循环
        self.window.mainloop()

    def welcome_page(self):
        """
        显示初始界面
        :return:
        """
        self.title_frame.pack(fill=X)
        self.title1.pack()
        self.select_frame.pack(fill=X)
        self.title2.grid(row=1, column=0)
        self.search.grid(row=1, column=1)
        Label(self.select_frame, width=40).grid(row=1, column=2)
        self.save.grid(row=1, column=3)

    def welcome_page_invisible(self):
        """
        隐形初始界面
        :return:
        """
        self.title_frame.pack_forget()
        self.select_frame.pack_forget()

    def show_back(self):
        """
        显示返回按钮
        :return:
        """
        self.back_frame.place(x=0, y=0)
        self.back.grid()

    def save_page_invisible(self):
        """
        隐藏登记界面
        :return:
        """
        self.back_frame.place_forget()
        self.file_select_frame.place_forget()
        self.tag_frame.place_forget()

    def search_page_invisible(self):
        """
        隐藏搜索界面
        :return:
        """
        self.type_in_frame.place_forget()
        self.show_frame.place_forget()
        self.page_frame.place_forget()

    def return_pressed(self, event):
        """
        添加tag
        :return:
        """
        tmp = self.tags.get()
        self.tags.delete(0, END)
        # print(tmp)
        self.tags_show.config(state=NORMAL)
        self.tags_show.insert(INSERT, "{}\n".format(tmp))
        self.tags_show.config(state=DISABLED)
        self.tag_list.append(tmp)

    def recall_clicked(self):
        """
        从tag中删掉最后一个
        :return:
        """
        total_len = len(self.tags_show.get(1.0, END).strip().split("\n"))
        print(total_len)
        self.tags_show.config(state=NORMAL)
        self.tags_show.delete(total_len * 1.0, END)
        self.tags_show.insert(INSERT, "\n")
        self.tags_show.config(state=DISABLED)
        self.tag_list = self.tag_list[:-1]

    def selected_clicked(self):
        """
        选择图片
        :return:
        """
        self.file = filedialog.askopenfilename(initialdir=os.path.dirname(__file__), filetypes=self.picture_file_types)
        # print(self.file)
        self.selected.config(text=self.file.split("/")[-1])
        try:
            photo = Image.open(self.file)
            photo = photo.resize((350, 210))
            img = ImageTk.PhotoImage(photo)
            self.show.config(image=img)
            self.show.image = img
            self.show.grid()
        except AttributeError:
            # print(183)
            pass

    def get_clicked(self):
        """
        完成并存储
        :return:
        """
        if not self.file:
            messagebox.showerror("错误", "未选择任何文件！")
            return
        if not self.tag_list:
            messagebox.showerror("错误", "未输入任何标签！")
            return

        file_name = save(self.file, self.tag_list)
        if file_name != -1:
            # 动态更新字典和倒排索引的内容
            self.update(file_name)
            messagebox.showinfo("消息", "保存成功！")
        else:
            messagebox.showinfo("消息", "保存失败！")

        # 清空当前所选所填项目
        self.file = None
        self.show.image = None
        self.tag_list = []
        self.selected.config(text="")
        self.tags_show.config(state=NORMAL)
        self.tags_show.delete(1.0, END)
        self.tags_show.config(state=DISABLED)

    def update(self, file_name: str):
        """
        动态更新字典和倒排索引的内容
        :return:
        """
        self.all_goods[file_name] = self.tag_list  # 将保存的消息存入字典

        # 更新倒排索引
        for i in self.tag_list:
            if not self.word_file.get(i):
                self.word_file[i] = [file_name]
            else:
                self.word_file[i].append(file_name)

    def search_clicked(self):
        """
        显示查询界面
        :return:
        """
        self.welcome_page_invisible()

        self.show_back()

        self.type_in_frame.place(x=80, y=0)
        self.type_in_describe.grid(row=0, column=0)
        self.type_in.grid(row=0, column=1)
        self.done.grid(row=0, column=2)

        self.now_result_goods_file = list(self.all_goods.keys())
        self.show_search_result()

        self.page_frame.place(x=80, y=self.height - 50)
        self.up_page.grid(row=0, column=0, padx=100)
        self.pages.grid(row=0, column=1, padx=100)
        self.down_page.grid(row=0, column=2, padx=100)

        self.type_in.delete(0, END)
        self.type_in.focus()

    def save_clicked(self):
        """
        显示登记界面
        :return:
        """
        self.welcome_page_invisible()

        self.show_back()

        self.file_select_frame.place(x=100, y=0)
        Label(self.file_select_frame, width=50).grid(row=0)
        self.select_file.grid(row=1)
        self.selected.grid(row=2)

        self.tag_frame.place(x=500, y=0)
        Label(self.tag_frame).grid(row=0)
        self.tag_describe.grid(row=1, column=0, columnspan=2)
        self.tags.grid(row=2, column=0)
        self.recall.grid(row=2, column=1, sticky=W)
        self.tags_show.grid(row=3, columnspan=2)
        self.get_tags.grid()

    def back_clicked(self):
        """
        返回初始界面（即隐藏登记界面或查找界面，显示初始界面）
        :return:
        """
        self.save_page_invisible()
        self.search_page_invisible()
        self.welcome_page()

    def read_all_goods(self):
        """
        读入所有的物品信息
        :return:
        """
        with open("data/data.dat", "r", encoding="utf-8-sig") as fin:
            s = fin.readline()
            while s:
                s = s.split()
                self.all_goods[s[0]] = s[1:]
                s = fin.readline()

    def reverse_index(self):
        """
        建立倒排索引
        :return:
        """
        for file in self.all_goods.keys():
            for word in self.all_goods[file]:
                if not self.word_file.get(word):
                    self.word_file[word] = [file]
                else:
                    self.word_file[word].append(file)

    def search_goods_by_tag(self):
        """
        搜索所有含有关键词的物品，物品按照符合的关键词的数量进行排序
        :return:
        """
        key_words = self.type_in.get().split()
        file_has_word_num = dict()
        s = set()
        try:
            for i in key_words:
                s.update(self.word_file[i])
                for j in self.word_file[i]:
                    if not file_has_word_num.get(j):
                        file_has_word_num[j] = 1
                    else:
                        file_has_word_num[j] += 1
            self.now_result_goods_file = list(s)
            self.now_result_goods_file.sort(key=lambda x: file_has_word_num[x], reverse=True)
            if not key_words:
                self.now_result_goods_file = list(self.all_goods.keys())
            self.show_search_result()
        except KeyError:
            # 未找到相关结果
            messagebox.showinfo("注意", "未找到相关结果！")
            self.show_frame.place_forget()

    def show_search_result(self):
        """
        展示当前页码的所有物品
        :return:
        """
        for i in self.pictures:
            i.grid_forget()

        for i in range(6):
            j = i + self.now_page * 6
            if j >= len(self.now_result_goods_file):
                break
            photo = Image.open('data/picture/' + self.now_result_goods_file[j])
            photo = photo.resize((200, 150))
            img = ImageTk.PhotoImage(photo)
            self.pictures[i].config(image=img)
            self.pictures[i].image = img

        self.show_frame.place(x=80, y=50)
        for i in range(2):
            for j in range(3):
                k = self.now_page * 6 + i * 3 + j
                if k >= len(self.now_result_goods_file):
                    break
                self.pictures[i * 3 + j].grid(row=i, column=j)

    def next_page(self):
        """
        下一页
        :return:
        """
        if (self.now_page + 1) * 6 < len(self.now_result_goods_file):
            self.now_page += 1
        self.var_pages.set(self.now_page + 1)
        self.show_search_result()

    def pre_page(self):
        """
        上一页
        :return:
        """
        if self.now_page:
            self.now_page -= 1
        self.var_pages.set(self.now_page + 1)
        self.show_search_result()


if __name__ == '__main__':
    Create()

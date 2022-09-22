import database as db
import helpers
from tkinter import *
from tkinter import filedialog as FileDialog
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING


class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)

        self.geometry(f'{w}x{h}+{x}+{y}')
        self.resizable(width=0, height=0)


class AddingVideoWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Add Song')
        self.iconbitmap('yt_icon.ico')
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        self.geometry('320x110')
        frame = Frame(self)
        frame.pack(padx=20, pady=5)

        Label(frame, text='Copy & Paste Youtube Link').pack()

        entry = Entry(frame)
        entry.pack()
        entry.config(width=70)
        entry.bind('<KeyRelease>', lambda event: self.validate(event))

        label_con = Label(frame, text='', pady=5)
        label_con.pack()

        frame = Frame(self)
        frame.pack(pady=5)

        add_s = Button(frame, text='Add Song', command=self.adding_song)
        add_s.configure(state=DISABLED)
        add_s.grid(row=0, column=0)
        add_v = Button(frame, text='Add Video', command=self.adding_video)
        add_v.configure(state=DISABLED)
        add_v.grid(row=0, column=1)
        Button(frame, text='Cancel', command=self.close).grid(row=0, column=2)

        self.add_s = add_s
        self.add_v = add_v
        self.entry = entry
        self.label_con = label_con

    def adding_song(self):
        data = helpers.data_video(self.entry.get(), 'Song')

        self.master.treeview.insert(
            parent='',
            index='end',
            iid=self.entry.get(),
            values=(
                self.entry.get(),
                data[1],
                data[2],
                data[3],
                data[4],
                'Song'))

        db.Videos.adding(
            self.entry.get(),
            data[1],
            data[2],
            data[3],
            data[4],
            'Song')

        self.close()

    def adding_video(self):
        data = helpers.data_video(self.entry.get(), 'Video')

        self.master.treeview.insert(
            parent='',
            index='end',
            iid=self.entry.get(),
            values=(
                self.entry.get(),
                data[1],
                data[2],
                data[3],
                data[4],
                'Video')
                )

        db.Videos.adding(
            self.entry.get(),
            data[1],
            data[2],
            data[3],
            data[4],
            'Video')

        self.close()

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event):
        url = event.widget.get()
        valid = helpers.video_validation(url)
        event.widget.configure({'bg': 'Green' if valid[0] else 'Red'})
        self.add_s.config(state=NORMAL if valid[0] else DISABLED)
        self.add_v.config(state=NORMAL if valid[0] else DISABLED)
        self.label_con.config(
            text=f'{valid[1]}!'
            )


class ChangeResolutionWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Select Resolution')
        self.iconbitmap('yt_icon.ico')
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        video = self.master.treeview.focus()
        data = self.master.treeview.item(video, 'values')
        url = data[0]
        data_res = helpers.data_resolution(url)

        self.geometry(f'120x{len(data_res)*20+65}')
        self.configure(bg='firebrick2')

        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame,  height=len(data_res))
        treeview['columns'] = ('RESOLUTION')

        treeview.column('#0', width=0, stretch=NO)
        treeview.column('RESOLUTION', anchor=CENTER, width=120)

        treeview.heading('RESOLUTION', text='RESOLUTION', anchor=CENTER)

        for res in data_res:
            treeview.insert(
                parent='', index='end', values=(res)
            )

        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=10)

        chg_res = Button(frame, text='Select', command=self.select_resolution)
        chg_res.grid(row=0, column=1)
        Button(frame, text='Cancel', command=self.close).grid(row=0, column=2)

        self.treeview = treeview
        self.url = url

    def select_resolution(self):
        selected = self.treeview.focus()
        res = self.treeview.item(selected, 'values')
        new_size = helpers.new_resolution_size(self.url, res[0])
        data = helpers.data_video(self.url, 'Video')
        video = self.master.treeview.focus()
        self.master.treeview.item(
            video,
            values=(data[0], data[1], data[2], new_size, res[0], 'Video')
            )
        db.Videos.change_data_res(self.url, new_size, res[0])
        self.close()

    def close(self):
        self.destroy()
        self.update()


class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title('Youtube Download')
        self.iconbitmap('yt_icon.ico')
        self.configure(bg='firebrick2')
        self.build()
        self.center()

    def build(self):
        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame)
        treeview['columns'] = (
            'LINK',
            'NAME',
            'LENGTH',
            'SIZE',
            'RESOLUTION',
            'TYPE'
            )

        treeview.column('#0', width=0, stretch=NO)
        treeview.column('LINK', anchor=CENTER, width=300)
        treeview.column('NAME', anchor=CENTER, width=330)
        treeview.column('LENGTH', anchor=CENTER, width=60)
        treeview.column('SIZE', anchor=CENTER, width=60)
        treeview.column('RESOLUTION', anchor=CENTER, width=90)
        treeview.column('TYPE', anchor=CENTER, width=60)

        treeview.heading('LINK', text='LINK', anchor=CENTER)
        treeview.heading('NAME', text='NAME', anchor=CENTER)
        treeview.heading('LENGTH', text='LENGTH', anchor=CENTER)
        treeview.heading('SIZE', text='SIZE', anchor=CENTER)
        treeview.heading('RESOLUTION', text='RESOLUTION', anchor=CENTER)
        treeview.heading('TYPE', text='TYPE', anchor=CENTER)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        treeview['yscrollcommand'] = scrollbar.set

        for video in db.Videos.lis:
            treeview.insert(
                parent='',
                index='end',
                iid=video.link,
                values=(
                    video.link,
                    video.name,
                    video.length,
                    video.size,
                    video.resolution,
                    video.type
                    )
                )

        treeview.pack()
        treeview.bind(
            '<<TreeviewSelect>>',
            lambda event: self.validate_type(event)
            )
        frame = Frame(self)
        frame.pack(pady=10)

        Button(
            frame,
            text='Add',
            command=self.adding,
            padx=15).grid(row=0, column=0)

        Button(
            frame,
            text='Remove',
            command=self.delete,
            padx=15).grid(row=0, column=1)

        chg_res = Button(
            frame,
            text='Resolution',
            command=self.change_resolution,
            padx=15)

        chg_res.configure(state=DISABLED)
        chg_res.grid(row=0, column=2)

        Button(
            frame,
            text='Download',
            command=self.download,
            padx=15).grid(row=0, column=3)

        self.treeview = treeview
        self.chg_res = chg_res

    def adding(self):
        AddingVideoWindow(self)

    def delete(self):
        video = self.treeview.focus()
        if video:
            data = self.treeview.item(video, 'values')
            confirm = askokcancel(
                title='Remove?',
                message=f'Do you want to remove {data[1]}?',
                icon=WARNING
                )
            if confirm:
                self.treeview.delete(video)
                db.Videos.removing(data[0])

    def change_resolution(self):
        video = self.treeview.focus()
        if video:
            ChangeResolutionWindow(self)

    def validate_type(self, event):
        type = event.widget.item(self.treeview.focus(), 'values')[5]
        valid = helpers.type_validation(type)
        self.chg_res.config(state=NORMAL if valid else DISABLED)

    def download(self):
        d = FileDialog.askdirectory()
        helpers.download(d)


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()

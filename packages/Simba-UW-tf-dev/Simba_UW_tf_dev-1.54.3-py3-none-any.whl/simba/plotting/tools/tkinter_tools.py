from tkinter import *

PADDING = 5


class InteractivePlotterWindowCreator(object):
    def __init__(self):
        self.main_frm = Toplevel()
        self.current_frm_number, self.jump_size = 0, 0
        img_frm = Frame(self.main_frm)
        img_frm.grid(row=0, column=1, sticky=NW)
        self.button_frame = Frame( self.main_frm, bd=2, width=700, height=300)
        self.button_frame.grid(row=1, column=0, sticky=NW)

        self.frame_id_lbl = Label(self.button_frame, text="FRAME NUMBER")
        self.frame_id_lbl.grid(row=0, column=1, sticky=NW, padx=PADDING)
        self.forward_next_frm_btn = Button(self.button_frame, text=">", command=lambda: self.load_new_frame())
        self.forward_next_frm_btn.grid(row=1, column=3, sticky=E, padx=PADDING)

        self.forward_last_frm_btn = Button(self.button_frame, text=">>", command=lambda: self.load_new_frame())
        self.forward_last_frm_btn.grid(row=1, column=4, sticky=E, padx=PADDING)
        self.back_one_frm_btn = Button(self.button_frame, text="<", command=lambda: self.load_new_frame())
        self.back_one_frm_btn.grid(row=1, column=1, sticky=W, padx=PADDING)

        self.back_first_frm = Button(self.button_frame, text="<<", command=lambda: self.load_new_frame())
        self.back_first_frm.grid(row=1, column=0, sticky=W)

        self.frame_entry_var = StringVar(self.main_frm, value=self.current_frm_number)
        self.frame_entry_box = Entry(self.button_frame, width=7, textvariable=self.frame_entry_var)
        self.frame_entry_box.grid(row=1, column=1)
        self.select_frm_btn = Button(self.button_frame, text="Jump to selected frame", command=lambda: self.load_new_frame())
        self.select_frm_btn.grid(row=2, column=1, sticky=N)

        self.jump_frm = Frame(self.window)
        self.jump_frm.grid(row=2, column=0)
        self.jump_lbl = Label(self.jump_frm, text="Jump Size:")
        self.jump_lbl.grid(row=0, column=0, sticky=NW)
        self.jump_size_scale = Scale(self.jump_frm, from_=0, to=100, orient=HORIZONTAL, length=200)
        self.jump_size_scale.set(self.jump_size)
        self.jump_size_scale.grid(row=0, column=1, sticky=NW)
        self.jump_forward_btn = Button(self.jump_frm, text="<<", command=lambda: self.load_new_frame())
        self.jump_forward_btn.grid(row=0, column=2, sticky=E)
        self.jump_back_btn = Button(self.jump_frm, text=">>", command=lambda: self.load_new_frame())
        self.jump_back_btn.grid(row=0, column=3, sticky=W)

        self.load_new_frame()

        instructions_frm = Frame(self.main_frm, width=100, height=100)
        instructions_frm.grid(row=0, column=2, sticky=N)
        key_presses = Label(instructions_frm, text='\n\n Keyboard shortcuts for frame navigation: \n Right Arrow = +1 frame'
                                             '\n Left Arrow = -1 frame'
                                             '\n Ctrl + s = Save and +1 frame'
                                             '\n Ctrl + l = Last frame'
                                             '\n Ctrl + o = First frame')
        key_presses.grid(sticky=S)
        self.bind_keys()


    def bind_keys(self):
        self.window.bind('<Control-s>', lambda x: self.save_checkboxes(self.window))
        self.window.bind('<Right>', lambda x: load_frame(current_frame_number+1, self.window, self.fbox))
        self.window.bind('<Left>', lambda x: load_frame(current_frame_number-1, self.window, self.fbox))
        self.window.bind('<Control-q>', lambda x: save_video(self.window))
        self.window.bind('<Control-l>', lambda x: load_frame(len(frames_in) - 1, self.window, self.fbox))
        self.window.bind('<Control-o>', lambda x: load_frame(0, self.window, self.fbox))

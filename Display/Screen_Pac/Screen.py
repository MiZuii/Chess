import tkinter as tk
import time
from Game.MainLoop import restart, input_get
from Game.Settings import GameSet
from Game.Register import GameRegister


class View:

    # fps counter -------------
    start = time.time()
    buffer = []
    # ------------------------

    def __init__(self, dimensions, title, frame_rate, update, custom_setup, board, *engines):
        self.dimensions = dimensions
        self.title = title
        self.custom_update = update
        self.custom_setup = custom_setup
        self.board = board
        self.reg = GameRegister(self)
        for en in range(len(engines)):
            setattr(self, "engine_" + str(en + 1), engines[en])
            engines[en].reg = self.reg
        self.engine = self.engine_1
        self.settings = GameSet(self)
        self.active_piece = False

        self.alive = True
        self.sub_alive = False
        self.mode = 0
        self.starting_pos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"
        self.fps_state = True
        self.cords_state = False

        self.frame_rate = int(1000 / frame_rate)
        self._window = None
        self.canvas = None
        self.label = None
        self._setup()

    def _setup(self):
        self._window = tk.Tk()      # Sets window as Tk object window
        self._window.title(self.title)          # Sets title of the window
        self._window.geometry(str(self.dimensions) + "x" + str(self.dimensions + 25))
        self._window.resizable(False, False)        # Window not resizable

        # --------- mode ------------
        # 0 - manual
        # 1 - auto evaluate for white
        # 2 - auto evaluate for black
        # -----------------------------
        self.button_1 = tk.Button(self._window, text="Restart", command=lambda: self.button_1_action(False))
        self.button_2 = tk.Button(self._window, text="Exit", command=lambda: self.quit())
        self.button_3 = tk.Button(self._window, text="FPS: on", command=lambda: self.button_3_action())
        self.button_4 = tk.Button(self._window, text="cords", command=lambda: self.button_4_action())
        self.entry_1 = tk.Entry(self._window)
        self.fps_counter = tk.Label(self._window, text="...")

        self.engine_options = []
        count = 0
        while True:
            count += 1
            try:
                en = getattr(self, "engine_" + str(count))
                self.engine_options.append(en.name)
            except AttributeError:
                break
        mode_options = ["PvE Pl.White",  "PvE Pl.Black", "PvP", "EvE"]
        self.engine_str = tk.StringVar()
        self.engine_str.set(self.engine_options[0])
        self.mode = tk.StringVar()
        self.mode.set(mode_options[2])
        self.menu_1 = tk.OptionMenu(self._window, self.engine_str, *self.engine_options)
        self.menu_2 = tk.OptionMenu(self._window, self.mode, *mode_options)

        self.button_1.place(x=0,  y=0,   anchor=tk.NW, height="25", width="50")
        self.button_2.place(x=50,  y=0,   anchor=tk.NW, height="25", width="50")
        self.button_3.place(x=100,  y=0,   anchor=tk.NW, height="25", width="50")
        self.button_4.place(x=618, y=0, anchor=tk.NW, height="25", width="50")
        self.entry_1.place(x=350,  y=0,   anchor=tk.NW, height="25", width="200")
        self.menu_1.place(x=150,  y=0,   anchor=tk.NW, height="25", width="100")
        self.menu_2.place(x=250,  y=0,   anchor=tk.NW, height="25", width="100")
        self.fps_counter.place(x=668,  y=0,   anchor=tk.NW, height="25", width="52")

        self.canvas = tk.Canvas(self._window, width=self.dimensions, height=self.dimensions)
        self.canvas.focus_set()            # Sets the focus to the canvas
        self.canvas.bind("<Button-1>", self.mouse_callback)
        self.canvas.place(x=0,  y=25, anchor=tk.NW)

        # -------- importing images -----------

        self.image_1 = tk.PhotoImage(file="Display\\Images\\board.png")
        self.image_2 = tk.PhotoImage(file="Display\\Images\\Wking.png")
        self.image_3 = tk.PhotoImage(file="Display\\Images\\Wqueen.png")
        self.image_4 = tk.PhotoImage(file="Display\\Images\\Wbishop.png")
        self.image_5 = tk.PhotoImage(file="Display\\Images\\Wknight.png")
        self.image_6 = tk.PhotoImage(file="Display\\Images\\Wrook.png")
        self.image_7 = tk.PhotoImage(file="Display\\Images\\Wpawn.png")
        self.image_8 = tk.PhotoImage(file="Display\\Images\\Bking.png")
        self.image_9 = tk.PhotoImage(file="Display\\Images\\Bqueen.png")
        self.image_10 = tk.PhotoImage(file="Display\\Images\\Bbishop.png")
        self.image_11 = tk.PhotoImage(file="Display\\Images\\Bknight.png")
        self.image_12 = tk.PhotoImage(file="Display\\Images\\Brook.png")
        self.image_13 = tk.PhotoImage(file="Display\\Images\\Bpawn.png")
        self.image_14 = tk.PhotoImage(file="Display\\Images\\cordinates.png")
        self.image_15 = tk.PhotoImage(file="Display\\Images\\click_grid.png")
        self.image_16 = tk.PhotoImage(file="Display\\Images\\dot.png")

        # -------- importing images -----------

        # self.canvas.pack_propagate(False)      # Doesn't allow widgets inside to determine the frames dimensions

        self.custom_setup(self)
        self._update()
        self._window.mainloop()

    def _update(self):

        # ----- fps counter
        buffer_length = 400

        if self.fps_state:
            if len(self.buffer) <= buffer_length:
                if time.time()-self.start:
                    self.buffer.append(1/(time.time()-self.start))
            else:
                self.buffer.pop(0)
        self.fps_counter.config(text="Fps: " + str(int(sum(self.buffer)/buffer_length)))
        # ---------------

        if not self.alive:
            self._window.destroy()
        self.start = time.time()
        self.custom_update(self)        # after creates a custom_update arg where a custom function can
        interval = time.time() - self.start
        if interval < self.frame_rate:
            self._window.after(int(self.frame_rate - interval), self._update)    # After the frame rate run again
        else:
            self._window.after(1, self._update)

    def promotion(self, white):
        sub_window = tk.Toplevel()
        sub_window.title("")
        sub_window.geometry("360x90")
        sub_window.resizable(False, False)
        sub_window.grab_set()
        self.sub_alive = True

        if white:
            # its white promotion
            knight = tk.Button(sub_window, image=self.image_5,
                               command=lambda: self.promotion_return_knight(sub_window, white))
            bishop = tk.Button(sub_window, image=self.image_4,
                               command=lambda: self.promotion_return_bishop(sub_window, white))
            rook = tk.Button(sub_window, image=self.image_6,
                             command=lambda: self.promotion_return_rook(sub_window, white))
            queen = tk.Button(sub_window, image=self.image_3,
                              command=lambda: self.promotion_return_queen(sub_window, white))
        else:
            # its black promotion
            knight = tk.Button(sub_window, image=self.image_11,
                               command=lambda: self.promotion_return_knight(sub_window, white))
            bishop = tk.Button(sub_window, image=self.image_10,
                               command=lambda: self.promotion_return_bishop(sub_window, white))
            rook = tk.Button(sub_window, image=self.image_12,
                             command=lambda: self.promotion_return_rook(sub_window, white))
            queen = tk.Button(sub_window, image=self.image_9,
                              command=lambda: self.promotion_return_queen(sub_window, white))

        knight.place(x=0, y=0, anchor=tk.NW, height="90", width="90")
        bishop.place(x=90, y=0, anchor=tk.NW, height="90", width="90")
        rook.place(x=180, y=0, anchor=tk.NW, height="90", width="90")
        queen.place(x=270, y=0, anchor=tk.NW, height="90", width="90")

    def game_end(self, msg):
        end_window = tk.Toplevel()
        end_window.title("")
        end_window.geometry("360x135")
        end_window.resizable(False, True)
        end_window.grab_set()

        game_string = ""
        for move in self.reg.game:
            game_string += "(" + str(move[0]) + "," + str(move[1]) + ")"

        info = tk.Label(end_window, text=msg)
        game_seq = tk.Label(end_window, text=game_string)
        restart_b = tk.Button(end_window, text="Restart", command=lambda: self.button_1_action(end_window))

        info.place(x=0, y=0, anchor=tk.NW, height="45", width="360")
        restart_b.place(x=0, y=45, anchor=tk.NW, height="45", width="360")
        game_seq.place(x=0, y=90, anchor=tk.NW, height="45", width="360")

    def promotion_return_knight(self, window, white):
        if white:
            self.reg.current_promotion = 3
        else:
            self.reg.current_promotion = 9
        self.sub_alive = False
        window.destroy()

    def promotion_return_bishop(self, window, white):
        if white:
            self.reg.current_promotion = 4
        else:
            self.reg.current_promotion = 10
        self.sub_alive = False
        window.destroy()

    def promotion_return_rook(self, window, white):
        if white:
            self.reg.current_promotion = 2
        else:
            self.reg.current_promotion = 8
        self.sub_alive = False
        window.destroy()

    def promotion_return_queen(self, window, white):
        if white:
            self.reg.current_promotion = 5
        else:
            self.reg.current_promotion = 11
        self.sub_alive = False
        window.destroy()

    def mouse_callback(self, event):
        field = self.canvas.gettags(self.canvas.find_closest(event.x, event.y))[0]
        input_get(int(field), self.reg.current_moves, self)
        # field is a str with the field clicked coordinates
        # run a function managing the given field and making a move

    # exit button code
    def quit(self):
        self.alive = False

    # restart button code
    def button_1_action(self, sub_window):

        if sub_window:
            sub_window.destroy()

        # starting position set
        self.starting_pos = self.entry_1.get()
        if self.starting_pos == "":
            self.starting_pos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"
        self.entry_1.delete(0, len(self.starting_pos))
        # ----------------------

        # engine set
        count = 0
        while True:
            count += 1
            try:
                en = getattr(self, "engine_" + str(count))
                if en.name == self.engine_str.get():
                    self.engine = en
            except AttributeError:
                break
        # -----------

        restart(self)

    def button_3_action(self):
        if self.fps_state is True:
            self.fps_state = False
            self.button_3.config(text="FPS: off")
        else:
            self.fps_state = True
            self.button_3.config(text="FPS: on")

    def button_4_action(self):
        if self.cords_state is True:
            self.cords_state = False
            self.canvas.itemconfigure("cords", state=tk.HIDDEN)
        else:
            self.cords_state = True
            self.canvas.itemconfigure("cords", state=tk.NORMAL)

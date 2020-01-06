import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


class GridOptions(tk.Tk):
    # Controls the generation of other frames(windows)
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(False, False)
        self.title("Python Pathfinder")
        self.title_font = tkfont.Font(family="Helvetica", size=14, weight="bold")

        # Centers the tkinter window
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry("+%d+%d" % (x, y))

        # Dictionary to store choices of user in other frames so the information is accessible
        # outside this module
        self.shared_data = {
            "game_size": tk.StringVar(),
            "algorithm": tk.StringVar(),
            "s_row": tk.IntVar(),
            "s_col": tk.IntVar(),
            "g_row": tk.IntVar(),
            "g_col": tk.IntVar(),
        }
        # Main frame that all the other frames will sit on top of
        main_frame = tk.Frame(self)
        main_frame.grid(column=0, row=0)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Generate an instance of each class and store in frames dic. Now we can move
        # between these frames and share data between them
        self.frames = {}
        for F in (SizePage, SGPage, ConfirmPage):
            pg_name = F.__name__
            frame = F(parent=main_frame, controller=self)
            self.frames[pg_name] = frame
            frame.grid(column=0, row=0, sticky="nsew")

        # Show first frame after creation of window
        self.show_frame("SizePage")

    def show_frame(self, pg_name):
        """Brings the frame "pg_name" to the forefront and generates that frame's event"""
        frame = self.frames[pg_name]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

    def quit_win(self):
        """Quit tkinter window"""
        self.destroy()

    def get_size(self):
        """Returns size stored in shared_data dic"""
        return self.shared_data["game_size"].get()


class SizePage(ttk.Frame):
    def __init__(self, parent, controller):
        # This frame holds options for gameboard size and search algorithm
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        title = ttk.Label(
            self, text="Search Options", font=controller.title_font, anchor="center"
        )
        size_label = ttk.Label(self, text="Select a size for the grid: ")
        size_box = ttk.Combobox(
            self,
            state="readonly",
            textvariable=self.controller.shared_data["game_size"],
            values=("Small", "Medium", "Large"),
        )
        size_box.current(0)
        alg_label = ttk.Label(self, text="Select a search algorithm: ")
        alg_box = ttk.Combobox(
            self,
            state="readonly",
            textvariable=self.controller.shared_data["algorithm"],
            values=("BFS", "DFS", "A-Star"),
        )
        alg_box.current(0)
        size_qbtn = ttk.Button(self, text="Quit", command=lambda: controller.quit_win())
        size_nextbtn = ttk.Button(
            self, text="Next", command=lambda: controller.show_frame("SGPage")
        )
        title.grid(column=0, row=0, columnspan=2)
        size_label.grid(column=0, row=1, sticky=("nw"))
        size_box.grid(column=1, row=1, sticky=("nw"))
        alg_label.grid(column=0, row=2)
        alg_box.grid(column=1, row=2)
        size_qbtn.grid(column=0, row=3, pady=10)
        size_nextbtn.grid(column=1, row=3, pady=10)


class SGPage(ttk.Frame):
    def __init__(self, parent, controller):
        # This frame holds goal and start indices
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)

        startLabel = ttk.Label(self, text="Select a start location, (row, col): ")
        goalLabel = ttk.Label(self, text="Select a goal location, (row, col): ")

        # Class members so on_show_frame function can set available values after class has been instantiated
        self.start_row = ttk.Combobox(
            self,
            state="readonly",
            textvariable=self.controller.shared_data["s_row"],
            width="5",
        )
        self.start_col = ttk.Combobox(
            self,
            state="readonly",
            textvariable=self.controller.shared_data["s_col"],
            width="5",
        )
        self.goal_row = ttk.Combobox(
            self,
            state="readonly",
            textvariable=self.controller.shared_data["g_row"],
            width="5",
        )
        self.goal_col = ttk.Combobox(
            self,
            state="readyonly",
            textvariable=self.controller.shared_data["g_col"],
            width="5",
        )

        sg_backbtn = ttk.Button(
            self, text="Back", command=lambda: controller.show_frame("SizePage")
        )
        sg_nextbtn = ttk.Button(
            self, text="Next", command=lambda: controller.show_frame("ConfirmPage")
        )
        startLabel.grid(column=0, row=0, sticky=("nw"))
        goalLabel.grid(column=0, row=1, sticky=("nw"))
        self.start_row.grid(column=1, row=0)
        self.start_col.grid(column=2, row=0)
        self.goal_row.grid(column=1, row=1)
        self.goal_col.grid(column=2, row=1)
        sg_backbtn.grid(column=0, row=3, pady=30)
        sg_nextbtn.grid(column=1, row=3, pady=30)

    def on_show_frame(self, event):
        # Once user selects a size for the game board, generate the available
        # indexes they can choose from for start/goal
        dimensions = []
        size_selection = self.controller.shared_data["game_size"].get()
        if size_selection == "Small":
            dimensions = [i for i in range(10)]
        elif size_selection == "Medium":
            dimensions = [i for i in range(25)]
        elif size_selection == "Large":
            dimensions = [i for i in range(40)]

        self.start_col["values"] = dimensions
        self.start_row["values"] = dimensions
        self.goal_col["values"] = dimensions
        self.goal_row["values"] = dimensions
        self.goal_col.current(len(dimensions) - 1)
        self.goal_row.current(len(dimensions) - 1)


class ConfirmPage(ttk.Frame):
    # Final frame with a confirm button that loads the gameboard with options selected
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        confirmLabel = ttk.Label(
            self,
            text="""
            Once you confirm, the grid will appear and 
            you can create barriers by holding down the mouse. 
            Press spacebar to begin the algorithm""",
            anchor="center",
        )
        confirm_frame_startbtn = ttk.Button(
            self, text="Start", command=lambda: controller.quit_win()
        )
        confirm_frame_backbtn = ttk.Button(
            self, text="Back", command=lambda: controller.show_frame("SGPage")
        )
        confirmLabel.grid(column=0, row=0, columnspan=3, rowspan=2)
        confirm_frame_backbtn.grid(column=0, row=2)
        confirm_frame_startbtn.grid(column=1, row=2)


import tkinter as tk
from queue import PriorityQueue, Queue
import time

ROWS = 20
CELL_SIZE = 30

# Colors
COLORS = {
    "normal": "white",
    "wall": "black",
    "start": "green",
    "end": "red",
    "visited": "light blue",
    "path": "yellow",
    "traffic": "orange",
    "heavy": "brown"
}

COST = {"normal": 1, "traffic": 5, "heavy": 10}

class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.type = "normal"
        self.rect = None

    def __lt__(self, other):
        return False

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Navigation Simulator")

        # Canvas
        self.canvas = tk.Canvas(root, width=ROWS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.grid(row=0, column=0, columnspan=4)

        # Grid
        self.grid = [[Cell(i,j) for j in range(ROWS)] for i in range(ROWS)]
        self.start = None
        self.end = None
        self.mode = "start"

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.click)

        # Controls
        tk.Button(root, text="Start", command=lambda: self.set_mode("start")).grid(row=1, column=0)
        tk.Button(root, text="End", command=lambda: self.set_mode("end")).grid(row=1, column=1)
        tk.Button(root, text="Wall", command=lambda: self.set_mode("wall")).grid(row=1, column=2)
        tk.Button(root, text="Traffic", command=lambda: self.set_mode("traffic")).grid(row=1, column=3)
        tk.Button(root, text="Heavy", command=lambda: self.set_mode("heavy")).grid(row=2, column=0)

        # Algorithm selection
        self.algo_var = tk.StringVar(value="BFS")
        tk.OptionMenu(root, self.algo_var, "BFS", "DFS", "A*", "Greedy").grid(row=2, column=1)

        tk.Button(root, text="Run", command=self.run).grid(row=2, column=2)
        tk.Button(root, text="Clear", command=self.clear).grid(row=2, column=3)

        # Stats
        self.stats = tk.Label(root, text="Stats: ", font=("Arial", 10))
        self.stats.grid(row=3, column=0, columnspan=4)

        # Legend
        legend = "Green=Start  Red=End  Black=Wall  Orange=Traffic  Brown=Heavy  Blue=Visited  Yellow=Path"
        tk.Label(root, text=legend, wraplength=400).grid(row=4, column=0, columnspan=4)

    def draw_grid(self):
        for i in range(ROWS):
            for j in range(ROWS):
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE
                rect = self.canvas.create_rectangle(x1,y1,x2,y2,fill="white",outline="gray")
                self.grid[i][j].rect = rect

    def set_mode(self, mode):
        self.mode = mode

    def click(self, event):
        r, c = event.y//CELL_SIZE, event.x//CELL_SIZE
        cell = self.grid[r][c]

        if self.mode == "start":
            self.start = cell
            self.canvas.itemconfig(cell.rect, fill=COLORS["start"])

        elif self.mode == "end":
            self.end = cell
            self.canvas.itemconfig(cell.rect, fill=COLORS["end"])

        else:
            cell.type = self.mode
            self.canvas.itemconfig(cell.rect, fill=COLORS[self.mode])

    def neighbors(self, cell):
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        res = []
        for d in dirs:
            r, c = cell.r+d[0], cell.c+d[1]
            if 0<=r<ROWS and 0<=c<ROWS:
                if self.grid[r][c].type != "wall":
                    res.append(self.grid[r][c])
        return res

    def heuristic(self,a,b):
        return abs(a.r-b.r)+abs(a.c-b.c)

    def reconstruct(self, came):
        path_len = 0
        cur = self.end
        while cur in came:
            cur = came[cur]
            path_len += 1
            if cur != self.start:
                self.canvas.itemconfig(cur.rect, fill=COLORS["path"])
            self.root.update()
        return path_len

    def run(self):
        algo = self.algo_var.get()
        start_time = time.time()
        nodes = 0

        if algo == "BFS":
            q = Queue()
            q.put(self.start)
            visited = {self.start}
            came = {}

            while not q.empty():
                cur = q.get(); nodes+=1
                if cur == self.end: break
                for n in self.neighbors(cur):
                    if n not in visited:
                        visited.add(n)
                        came[n]=cur
                        q.put(n)
                        self.canvas.itemconfig(n.rect, fill=COLORS["visited"])
                self.root.update()

        elif algo == "DFS":
            stack=[self.start]
            visited={self.start}
            came={}
            while stack:
                cur=stack.pop(); nodes+=1
                if cur==self.end: break
                for n in self.neighbors(cur):
                    if n not in visited:
                        visited.add(n)
                        came[n]=cur
                        stack.append(n)
                        self.canvas.itemconfig(n.rect, fill=COLORS["visited"])
                self.root.update()

        elif algo == "A*":
            pq=PriorityQueue()
            pq.put((0,self.start))
            came={}
            g={cell:float("inf") for row in self.grid for cell in row}
            g[self.start]=0
            while not pq.empty():
                cur=pq.get()[1]; nodes+=1
                if cur==self.end: break
                for n in self.neighbors(cur):
                    cost=COST.get(n.type,1)
                    temp=g[cur]+cost
                    if temp<g[n]:
                        came[n]=cur
                        g[n]=temp
                        f=temp+self.heuristic(n,self.end)
                        pq.put((f,n))
                        self.canvas.itemconfig(n.rect, fill=COLORS["visited"])
                self.root.update()

        elif algo == "Greedy":
            pq=PriorityQueue()
            pq.put((0,self.start))
            came={}
            visited={self.start}
            while not pq.empty():
                cur=pq.get()[1]; nodes+=1
                if cur==self.end: break
                for n in self.neighbors(cur):
                    if n not in visited:
                        visited.add(n)
                        came[n]=cur
                        pq.put((self.heuristic(n,self.end),n))
                        self.canvas.itemconfig(n.rect, fill=COLORS["visited"])
                self.root.update()

        end_time = time.time()
        path_len = self.reconstruct(came)

        self.stats.config(
            text=f"Algorithm: {algo} | Time: {round(end_time-start_time,4)}s | Nodes: {nodes} | Path Length: {path_len}"
        )

    def clear(self):
        for row in self.grid:
            for cell in row:
                cell.type="normal"
                self.canvas.itemconfig(cell.rect, fill="white")
        self.start=None
        self.end=None
        self.stats.config(text="Stats: ")

root = tk.Tk()
app = App(root)
root.mainloop()
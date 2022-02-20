from tkinter import *
import tkinter as tk
import random

class Problem:

    def __init__(self, size_of_array=80, min_value_of_elems=-100, max_value_of_elems=1000, target=0):

        self.x = []
        self.y = []
        self.size_of_array  =size_of_array
        l1 = list(range(min_value_of_elems,max_value_of_elems))
        while len(self.x)< size_of_array:
            v1 = l1.pop(random.randint(0,len(l1)-1))
            self.x.append(v1)

        l2 = list(range(min_value_of_elems,max_value_of_elems))
        while len(self.y)< size_of_array:
            v2 = l2.pop(random.randint(0,len(l2)-1))
            self.y.append(v2)

        self.target = target


class Combo:
    def __init__(self, x,y, xval, yval):
        self.x = x
        self.y = y
        self.xval = xval
        self.yval = yval
    def sum(self):
        return self.xval+self.yval


        
class TwoListAddToTarget(tk.Frame):

    def __init__(self, parent, problem, canvas_width=1000, canvas_height=1000, text_on =True, interval = 10):
        self.parent = parent
        self.problem = problem
        self.maxYperX = [-1]*self.problem.size_of_array #E.G in index i in array, representing xi, for all yj [i,max], what is max where xi+yj < target
        self.minXperY = [-1]*self.problem.size_of_array  #E.G in index i in array, representing yi, for all xj [0,i], what is min where xi+yj > target
        self.solutions = []
        self.path_red=[] #path of x+y > T
        self.path_blue=[] # path of x+y < t
        self.path_XPYET=[] #path of x+y == t
        #visualisation
        self.xsize = canvas_width
        self.ysize = canvas_height
        #part of solution, not part of visualisation
        self.problem.x= sorted(self.problem.x)
        self.problem.y= sorted(self.problem.y)
        #
        self.i = 0
        self.j = self.problem.size_of_array-1
        self.interval =interval
        self.text_on = text_on
        self.best = Combo(self.i, self.j, self.problem.x[self.i], self.problem.y[self.j])
        self.best_diff = 100000000;

       # self.x_j = 0
       # self.y_j = self.problem.size_of_array-1

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

        self.red = 'red'
        self.blue = 'blue'
        self.white = 'white'
        self.green = 'green'
        self.grey = 'grey'
        self.yellow = 'yellow'

    # def run2(self):

    #     if self.i < self.problem.size_of_array:


    #         while self.y_j>-1 and self.y_j < self.problem.size_of_array and self.problem.x[self.i] + self.problem.y[self.y_j] > self.problem.target :
    #             print("i={0}, y_j={1}, self.problem.x[self.i]={2}, self.problem.y[self.y_j]={3}, self.problem.x[self.i] + self.problem.y[self.y_j] ={4}, target={5}\n".format(self.i, self.y_j, self.problem.x[self.i],self.problem.y[self.y_j], self.problem.x[self.i] + self.problem.y[self.y_j], self.problem.target))
    #             if self.problem.x[self.i] + self.problem.y[self.y_j] == self.problem.target:
    #                 self.solutions.append(Solution(self.i,self.y_j))
    #             self.y_j=self.y_j-1
    #         self.maxYperX[self.i] = self.y_j
    #         self.i = self.i +1
    #     if self.j >= 0:
            
    #         while self.x_j>-1 and self.x_j < self.problem.size_of_array and self.problem.y[self.j] + self.problem.x[self.x_j] < self.problem.target:
    #             print("j={0}, x_j={1}, self.problem.y[self.j] ={2}, self.problem.x[self.x_j]={3}, self.problem.x[self.i] + self.problem.y[self.y_j] ={4}, target={5}\n".format(self.j, self.x_j, self.problem.y[self.j],self.problem.x[self.x_j], self.problem.y[self.j] + self.problem.x[self.x_j] , self.problem.target))
    #             if self.problem.x[self.j] + self.problem.y[self.x_j] == self.problem.target:
    #                 self.solutions.append(Solution(self.x_j,self.i))
    #             self.x_j=self.x_j+1
    #         self.minXperY[self.j] = self.x_j
    #         self.j = self.j - 1

    #     self.visualise();   
    #     self.parent.after(10, self.run)
  

    def run(self):

        #three cases;
        #x_i + y_j < target => move down i++
        #x_i + y_j > target => move left j-- 
        #x_i + y_j == target => arbitrary move down (could be left)

        if self.i < self.problem.size_of_array and self.i >= 0 and self.j < self.problem.size_of_array and self.j >= 0:
            sum = self.problem.x[self.i] + self.problem.y[self.j] 
            if sum > self.problem.target :
          #      print("i={0}, j={1}, self.problem.x[self.i]={2}, self.problem.y[self.j]={3}, self.problem.x[self.i] + self.problem.y[self.j] ={4}, target={5}\n".format(self.i, self.j, self.problem.x[self.i],self.problem.y[self.j], self.problem.x[self.i] + self.problem.y[self.j], self.problem.target))
           #     self.maxYperX[self.i] = self.j
                self.path_red.append(Combo(self.i, self.j, self.problem.x[self.i] ,self.problem.y[self.j]))
                self.j=self.j-1 #if sum > T then add point to red path and move current point to left j-1 for next iteration
            elif sum < self.problem.target :
                self.path_blue.append(Combo(self.i, self.j, self.problem.x[self.i] ,self.problem.y[self.j]))
                self.i = self.i+1 #if sum < T then add point to blue path and move current point down i+1 for next iteration
            if abs(self.problem.target-sum) < self.best_diff:
                self.best = Combo(self.i, self.j, self.problem.x[self.i], self.problem.y[self.j])
                self.best_diff = abs(self.problem.target-sum)

            self.visualise();   
            if sum == self.problem.target:
                self.solutions.append(Combo(self.i, self.j, self.problem.x[self.i] ,self.problem.y[self.j]))
                self.visualise();   
            else:
                self.parent.after(self.interval, self.run)
            


    def refresh(self, event):
        self.xsize = int((event.width-1) / self.problem.size_of_array)
        self.ysize = int((event.height-1) / self.problem.size_of_array)
        self.visualise()



    def visualise(self):
        '''Redraw the board, possibly in response to window being resized'''
        self.canvas.delete("all")
        self.size = min(self.xsize, self.ysize)-2
        

        for blue_point in self.path_blue:           
            for col_i in range(0, blue_point.y+1):
                x1 = (col_i * self.size)
                y1 = (blue_point.x * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                color = self.blue
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square") 
        if self.text_on:
            for blue_point in self.path_blue:   
                self.canvas.create_text(blue_point.y* self.size+20, blue_point.x* self.size +20, text =str(blue_point.sum()), fill="black", font=('Helvetica 10 bold'));   

        for red_point in self.path_red:    
           
            for row_i in range(red_point.x, self.problem.size_of_array):
                x1 = (red_point.y * self.size)
                y1 = (row_i* self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                color = self.red
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square") 
        if self.text_on:
            for red_point in self.path_red:   
                self.canvas.create_text(red_point.y* self.size+20, red_point.x* self.size +20, text =str(red_point.sum()), fill="black", font=('Helvetica 10 bold'));    


        x1 = (self.best.y * self.size)
        y1 = (self.best.x* self.size)
        x2 = x1 + self.size
        y2 = y1 + self.size
        color = self.red
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.yellow, tags="square")
        if self.text_on:     
            self.canvas.create_text(self.best.y* self.size+20, self.best.x* self.size +20, text =str(self.best.sum()), fill="black", font=('Helvetica 10 bold'));    

        for sol in self.solutions:
            x1 = (sol.y * self.size)
            y1 = (sol.x* self.size)
            x2 = x1 + self.size
            y2 = y1 + self.size
            color = self.red
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.green, tags="square")
            if self.text_on:      
                self.canvas.create_text(sol.y* self.size+20, sol.x* self.size +20, text =str(self.best.sum()), fill="black", font=('Helvetica 10 bold'));    

        #text output
        target = "Target: {0}".format(self.problem.target)
        current = "Current: X={0} Y={1}, X+Y={2}".format(self.problem.x[self.i], self.problem.y[self.j], self.problem.x[self.i] + self.problem.y[self.j])
        best = "Best: X={0} Y={1}, X+Y={2}".format(self.best.xval, self.best.yval, self.best.xval + self.best.yval)
        self.canvas.create_text(self.size*self.problem.size_of_array -75 ,self.size*self.problem.size_of_array+20, text =target ,fill="black", font=('Helvetica 15 bold'));    
        self.canvas.create_text(self.size*self.problem.size_of_array -75,self.size*self.problem.size_of_array+40, text =current ,fill="black", font=('Helvetica 15 bold'));    
        self.canvas.create_text(self.size*self.problem.size_of_array -75,self.size*self.problem.size_of_array+60, text =best ,fill="black", font=('Helvetica 15 bold'));    


        
#         for row in range(self.problem.size_of_array):
# ##            if self.numQueens%2==0:
# ##                color = self.color1 if color == self.color2 else self.color2
#             col = self.maxYperX[row]
#             if col > -1:
#                 for row_i in range(row, self.problem.size_of_array):
#                     #if self.numQueens%2==1:
#                     #check if row has been determ
#                     x1 = (col * self.size)
#                     y1 = (row_i * self.size)
#                     x2 = x1 + self.size
#                     y2 = y1 + self.size
#                     color = self.red
#                     self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square") 
        
#         for col in range(self.problem.size_of_array):
# ##            if self.numQueens%2==0:
# ##                color = self.color1 if color == self.color2 else self.color2
#             row = self.minXperY[col]
#             if row > -1:
#                 for col_j in range(col, self.problem.size_of_array):
#                     #if self.numQueens%2==1:
#                     #check if row has been determ
#                     x1 = (col_j * self.size)
#                     y1 = (row * self.size)
#                     x2 = x1 + self.size
#                     y2 = y1 + self.size
#                     color = self.blue
#                     self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square") 

                # if col <= self.j:
                #     if col> self.maxYperX[row] and row >=self.minXperY[col]:
                #         color = self.red

                
""" 
     for col in range(self.problem.size_of_array):
##            if self.numQueens%2==0:
##                color = self.color1 if color == self.color2 else self.color2
            for row in range(self.problem.size_of_array):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                if col >= self.j:
                    if row >= self.minXperY[col]:
                        color = self.red
                        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square") """
        

if __name__ == '__main__':

    root = tk.Tk()
    p = Problem(size_of_array=120, min_value_of_elems=-100, max_value_of_elems=10000, target=5000)
    print(p.x)
    print(p.y)
    print(p.target)

    solution =  TwoListAddToTarget(root, p,text_on=False, interval = 10)
  #  solution.run()
    solution.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    root.wm_title("Solving Two Lists Add Target")

    root.after(1000, solution.run)
   # print('entering mainloop')
    root.mainloop()
    
    
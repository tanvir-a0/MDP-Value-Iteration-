import customtkinter as ctk
import copy

class Grid:
    number_of_columns = 0
    number_of_rows = 0
    def __init__(self, number_of_rows, number_of_columns, terminal_index):
        self.terminal_index = terminal_index
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.grid = [[0 for i in range(number_of_columns)] for j in range(number_of_rows)]

    def add_row(self, row_index, row_li):
        for i in range(0, len(row_li)):
            if row_li[i] == None:
                pass
            else:
                row_li[i] = float(row_li[i])

        if row_index < 0 or row_index >= self.number_of_rows:
            raise ValueError("Row index is out of range.")
        
        if len(row_li) != self.number_of_columns:
            raise ValueError("This row doesn't have the same length as the number of columns.")
        
        self.grid[row_index] = row_li

    def add_column(self, column_index, column_li):
        for i in range(0, len(column_li)):
            if column_li[i] == None:
                pass
            else:
                column_li[i] = float(column_li[i])

        if column_index < 0 or column_index >= self.number_of_columns:
            raise ValueError("Column index is out of range")

        if len(column_li) != self.number_of_rows:
            raise ValueError("This column doesn't have the same length as the number of rows.")

        for i in range(0, self.number_of_rows):
            self.grid[i][column_index] = column_li[i]

    def get_direction_value(self, row_index, column_index, direction):
        if direction == "up":
            if row_index-1 < 0:
                return float(self.grid[row_index][column_index] )
            
            if self.grid[row_index-1][column_index] == None:
                return float(self.grid[row_index][column_index] )
            
            return float(self.grid[row_index-1][column_index] )
            
        if direction == "down":
            if row_index+1 >= self.number_of_rows:
                return float(self.grid[row_index][column_index] )
            
            if self.grid[row_index+1][column_index] == None:
                return float(self.grid[row_index][column_index])
            
            return float(self.grid[row_index+1][column_index] )


        if direction == "left":
            if column_index-1 < 0:
                return float(self.grid[row_index][column_index] )
            
            if self.grid[row_index][column_index-1] == None:
                return float(self.grid[row_index][column_index])
            
            return float(self.grid[row_index][column_index-1] )

        if direction == "right":
            if column_index+1 >= self.number_of_columns:
                return float(self.grid[row_index][column_index] )
            
            if self.grid[row_index][column_index+1] == None:
                return float(self.grid[row_index][column_index])
            
            return float(self.grid[row_index][column_index+1] )

def calculate_mdp(grid, noise, discount, living_reward, k):   
    if k == 0:
        tmp_grid = Grid(grid.number_of_rows, grid.number_of_columns, [])
        for row_no in range(0, grid.number_of_rows):
            for column_no in range(0, grid.number_of_columns):
                if grid.grid[row_no][column_no] == None :
                    tmp_grid.grid[row_no][column_no] = None
        return grid
    elif k == 1:
        calculate_mdp(grid, noise, discount, living_reward, k-1)
        return grid
    else:
        old_grid_v0 = calculate_mdp(copy.deepcopy(grid), noise, discount, living_reward, k-1)
        new_grid_v1 = copy.deepcopy(grid)

        for row_no in range(0, old_grid_v0.number_of_rows):
            for column_no in range(0, old_grid_v0.number_of_columns):
                if old_grid_v0.grid[row_no][column_no] == None :
                    new_grid_v1.grid[row_no][column_no] = None
                    continue
                
                if [row_no,column_no] in old_grid_v0.terminal_index:
                    continue

                up = ((1 - noise)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "up"))
                      +(noise/2)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "left"))
                      +(noise/2)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "right")))

                down = ((1 - noise)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "down"))
                      +(noise/2)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "left"))
                      +(noise/2)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "right")))

                left = ((1 - noise)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "left"))
                      +(noise/2)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "up"))
                      +(noise/2)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "down")))

                right = ((1 - noise)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "right"))
                      +(noise/2)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "up"))
                      +(noise/2)*(living_reward + discount * old_grid_v0.get_direction_value(row_no, column_no, "down")))
                
                new_grid_v1.grid[row_no][column_no] = max(up, down, left, right)

        return new_grid_v1
                    
def color_to_hex(value):
    # If value is negative, interpret as "bright red"
    if value < 0:
        # Set red component to maximum (255), green and blue to 0
        red_hex = 'FF'
        green_hex = '00'
        blue_hex = '00'
    else:
        # Ensure value is within the valid range (0 to 1)
        value = max(0.0, min(1.0, value))
        # Convert value to integer range (0 to 255)
        value_int = int(value * 200)
        # Convert value to hexadecimal representation
        value_hex = format(value_int, '02X')
        # Set red component to the hexadecimal value, green and blue to 0
        red_hex = "00"
        green_hex = value_hex
        blue_hex = '00'
    # Construct the hexadecimal color value
    color_hex = '#' + red_hex + green_hex + blue_hex
    return color_hex

def update_gui_values(grid, k):
    xgap = 0.8 / grid.number_of_rows
    ygap = 0.9 / grid.number_of_columns
    x = 0.1
    y = 0.05
    for i in range(grid.number_of_rows):
        for j in range(grid.number_of_columns):
            cell_value = grid.grid[i][j]
            if cell_value is not None:
                label = ctk.CTkLabel(app, text=f'{cell_value:.2f}', fg_color=color_to_hex(cell_value), width = 100 , height= 40, corner_radius= 10 )
                label.cget("font").configure(size=30)
                label.place(relx=x, rely=y, anchor=ctk.CENTER)
            else:
                label = ctk.CTkLabel(app, text='None', fg_color="grey" , width = 100, height= 40, corner_radius= 10)
                label.cget("font").configure(size=30)
                label.place(relx=x, rely=y, anchor=ctk.CENTER)
            print(x,y)
            x = x + xgap
        x = 0.1
        y = y + ygap
    label = ctk.CTkLabel(app, text='K = ' + str(k), fg_color="grey" , width = 100, height= 40, corner_radius= 10)
    label.cget("font").configure(size=30)
    label.place(relx=0.9, rely=0.9, anchor=ctk.CENTER)


k = 0
def update_values():
    global k
    k += 1
    updated_grid = calculate_mdp(copy.deepcopy(grid1), noise=0.2, discount=0.9, living_reward=0, k=k)
    update_gui_values(updated_grid, k)


grid1 = Grid(number_of_rows=3, number_of_columns=4, terminal_index=[[0,3],[1,3]])
grid1.add_column(0, [0, 0, 0])
grid1.add_column(1, [0, None, 0])
grid1.add_column(2, [0, 0, 0])
grid1.add_column(3, [+1, -1, 0])

app =  ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("600x600")
app.title("MDP")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



def button_function():
    print("button pressed")
    update_values()

# Use CTkButton instead of tkinter Button
button =  ctk.CTkButton(master=app, text="Increase the value of K", command=button_function)
button.place(relx=0.5, rely=0.8, anchor= ctk.CENTER)

app.mainloop()

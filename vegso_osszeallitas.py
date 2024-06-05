import threading
import time
import math
from functools import partial
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
import tkinter as tk
from tkinter.font import Font
import customtkinter
from PIL import Image, ImageTk


# Create a Tkinter window
root = tk.Tk()
root.title("Interaktiv")
root.attributes("-fullscreen", True)

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
center=width/2
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width_max=root.winfo_screenwidth()
height_max=root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")

def x_gomb(root,bg_color_here):
    end_button=customtkinter.CTkButton(
        root,
        width=50,
        height=50,
        text= "x",
        text_color="white",
        command=lambda:root.destroy(),
        font=("Helvetic",30,"bold"),
        fg_color=bg_color_here,
        bg_color=bg_color_here,
        hover_color="red",
        )
    end_button.place(x=root.winfo_screenwidth()-50)

def vissza_gomb(root,bg_color_here,tohere):
    vissza_button=customtkinter.CTkButton(
        root,
        width=50,
        height=50,
        text= "<-",
        text_color="white",
        command=tohere,
        font=("Arial",30,"bold"),
        fg_color=bg_color_here,
        bg_color=bg_color_here,
        hover_color="red",
        )
    vissza_button.place(x=0,y=0)

def clear_window():
    # Destroy all widgets in the window
    for widget in root.winfo_children():
        widget.destroy()

#
### Interaktiv
#

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
center=width/2

global path_points
second_live=2
second=1

def vissza_gomb(root,bg_color_here,tohere):
    vissza_button=customtkinter.CTkButton(
        root,
        width=50,
        height=50,
        text= "<-",
        text_color="white",
        command=tohere,
        font=("Arial",30,"bold"),
        fg_color=bg_color_here,
        bg_color=bg_color_here,
        hover_color="red",
        )
    vissza_button.place(x=0,y=0)

    #button = tk.Button(root, text="<--", command=home)
    #button.place(x=10, y=10)

def x_gomb(root,bg_color_here):
    end_button=customtkinter.CTkButton(
        root,
        width=50,
        height=50,
        text= "x",
        text_color="white",
        command=lambda:root.destroy(),
        font=("Helvetic",30,"bold"),
        fg_color=bg_color_here,
        bg_color=bg_color_here,
        hover_color="red",
        )
    end_button.place(x=root.winfo_screenwidth()-50)

class TimerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.seconds = 0
        
        self.running = True

    def run(self):
        while self.running:
            time.sleep(1)
            self.seconds += 1

            #print(f"Elapsed time: {second_live} seconds")

    def stop(self):
        self.running = False


# Global variables
car_speed = 60
car_weight = 30
ok_ramp=0
ramp=400
road_cords_number=0
road_x="X :"
road_y="Y :"
path_points=[(30,400)]
path_points_x=0
road_cords_ok=1
display_speed=None
ok_entry=[0,0,0]

def start_appear(root,canvas,start_button):
    #DESTROY
    text_box.destroy()
    text_box2.destroy()
    text_road.destroy()
    display_rules.destroy()
    display_speed.place(x=root.winfo_screenwidth()/2-55, y=40)

    car_window=canvas.create_rectangle(20,260,root.winfo_screenwidth()-20,root.winfo_screenheight()-30, fill="lightblue")
    path_points.pop(0)
    start_button.configure(
        state=tk.NORMAL,
        text= "START", 
        fg_color="#57b066",   
        font=("Helvetica", 30, "bold"),
        
        )

def add_widgets_to_window(window,canvas,center,height,start_button):
    global text_box, text_box2,text_road,display_rules

    def add_kg(event):
        if " kg" or "Error" in text_box2.get():
            text_box2.delete(0, tk.END)

    def check_weight(event=None):
        global car_weight,ok_entry
        try:
            weight = float(text_box2.get())
            car_weight = weight
            text_box2.delete(0, tk.END)
            text_box2.insert(tk.END, f"{weight} kg")
            ok_entry[0]=1
            if ok_entry[0]+ok_entry[1]+ok_entry[2]==3:
                start_appear(window,canvas,start_button)
        except ValueError:
            text_box2.delete(0, tk.END)
            text_box2.insert(0, "Error")
            ok_entry[0]=0

    def add_km_per_hour(event):
        if " KM/H" or "Error" in text_box.get():
            text_box.delete(0, tk.END)

    def check_entry(event=None):
        global car_speed,ok_entry
        try:
            number = float(text_box.get())
            car_speed = number
            text_box.delete(0, tk.END)
            text_box.insert(tk.END, f"{number} km/h")
            ok_entry[1]=1
            
            if ok_entry[0]+ok_entry[1]+ok_entry[2]==3:
                start_appear(window,canvas,start_button)
        except ValueError:
            text_box.delete(0, tk.END)
            text_box.insert(0, "Error")
            ok_entry[1]=0

    def add_cords(event):
        if "Koordináták" or "Error" in text_road.get():
            text_road.delete(0, tk.END)

    def check_cords(event=None):
        
        global ramp,road_x,road_y,road_cords_number,path_points,path_points_x,road_cords_ok,ok_entry
        try:
            
            cords = int(text_road.get())
            if ((road_cords_number%2==0 and cords>=50 and cords<=window.winfo_screenwidth()-50) or (road_cords_number%2==1 and cords>=290 and cords<=window.winfo_screenheight()-50)) and road_cords_ok==1:
                text_road.delete(0, tk.END)
                
                #Display the road
                if road_cords_number%2==0:
                    path_points_x=cords
                    
                    road_x+=str(cords)+", "
                else:
                    path_points.insert(road_cords_number,(path_points_x,cords))
                    road_y+=str(cords)+", "
                    
                road_cords_number+=1
                if road_cords_number==8:
                    road_cords_ok=0
                    ok_entry[2]=1
                if ok_entry[0]+ok_entry[1]+ok_entry[2]==3:
                    start_appear(window,canvas,start_button)
                
                display_x.configure(text=road_x,)
                display_y.configure(text=road_y)
                
                
                    
        except ValueError:
            text_road.delete(0, tk.END)
            text_road.insert(0, "Error")

    
    global display_speed
    #FONT
    text_font = ("Helvetica", 24,"bold")

    #Speed_enter
    text_box = customtkinter.CTkEntry(
        window, 
        width=290,
        height=50, 
        font=text_font,
        fg_color="#57b066", 
        text_color="White",
        corner_radius=20,
        bg_color="#aceca2",   
        border_width=0,
        border_color="white",
        
        )
    text_box.place(x=center+20, y=80)
    text_box.insert(0, "Sebesség (KM/H)")
    #Mass_enter
    text_box2 = customtkinter.CTkEntry(
        window, 
        width=290,
        height=50, 
        font=text_font,
        fg_color="#57b066",
        text_color="White",
        corner_radius=20,
        bg_color="#aceca2",   
        border_width=0
        
        )
    text_box2.place(x=center-300, y=80)
    text_box2.insert(0, "Suly (kg)")
    #Cords_enter
    text_road =customtkinter.CTkEntry(
        window, 
        width=300,
        height=50, 
        font=text_font,
        fg_color="#57b066", 
        text_color="White",
        corner_radius=20,
        bg_color="#aceca2",   
        border_width=0
        
        )
    text_road.place(x=center-140, y=135)
    text_road.insert(0, "Koordináták")

    #Display rules
    display_rules = customtkinter.CTkLabel(
        window,
        width=290, 
        height=50, 
        text="Írj be 4x és 4y koordinátát felváltva, egyessével",
        text_color="#57b066",
        corner_radius=20,
        bg_color="#aceca2",   
        font=("Helvetica", 20, "bold"),

        )
    display_rules.place(x=center-230, y=30)
    

    #Display cords
    display_x = customtkinter.CTkLabel(
        window, 
        width=200, 
        height=20, 
        font=("Helvetica", 15,"bold"), 
        fg_color="#aceca2", 
        text_color="#57b066", 
        text=road_x
        )
    display_x.place(x=center-95, y=200)
    display_y = customtkinter.CTkLabel(
        window, 
        width=200,
        height=20,
        font=("Helvetica", 15,"bold"),
        fg_color="#aceca2", 
        text_color="#57b066", 
        text=road_y
        )
    display_y.place(x=center-95, y=230)

    #Display speed
    display_speed=customtkinter.CTkLabel(
        window,
        text="",
        width=10,
        height=2,
        fg_color="#aceca2",
        text_color="#aceca2",
        bg_color="#aceca2",
        font=("Helvetica", 30,"bold"),

        )
    


    #Bind of the buttons
    text_box2.bind("<FocusIn>", add_kg)
    text_box2.bind("<Return>", check_weight)

    text_box.bind("<FocusIn>", add_km_per_hour)
    text_box.bind("<Return>", check_entry)

    text_road.bind("<FocusIn>",add_cords)
    text_road.bind("<Return>", check_cords)

class PathFollower:
    def __init__(self, canvas, path_points):
        self.canvas = canvas
        self.car = None
        self.path = None
        self.path_points = path_points
        self.speed = car_speed*0.27778
        self.weight = car_weight
        self.friction = 0.05*9.81 #gurulo szurlódási együttható * g == 0.49m/s^2

    def draw_car(self, x, y):
        # Correct way to load the image using Pillow (PIL)
        self.image_path = r"Kepek\kek_car.png"  # Use a raw string to handle backslashes
        self.image = Image.open(self.image_path)

        # Resize the image to fit within the 200x300 rectangle
        self.image = self.image.resize((90, 80)) 
        self.rotated_image = self.image.rotate(0)
        self.photo = ImageTk.PhotoImage(self.rotated_image)

        # Place the image inside the rectangle
        self.car=self.canvas.create_image(x, y, image=self.photo)    

    def draw_path(self):
        self.path = self.canvas.create_line(self.path_points,fill="#57b066")

    def calculate_acceleration(self, theta_deg):

        g=9.81
        mu=0.05
        theta_rad=math.radians(theta_deg)
        acceleration=g*(math.sin(theta_rad)+math.cos(theta_rad)*mu)
        return acceleration
    
    def move_car_along_path(self,root):
        self.weight = car_weight
        display_speed.configure(text_color="#57b066")
        ok = 0 
        for i in range(len(self.path_points) - 1):
            
            start_x, start_y = self.path_points[i]
            end_x, end_y = self.path_points[i + 1]
            distance = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
            steps = int(distance)
            degree = -math.degrees(math.atan2(end_y - start_y, end_x - start_x))
            acceleration = -self.calculate_acceleration(degree) 
            second=0
            #Timer start
            timer_thread = TimerThread()
            timer_thread.start() 

            for step in range(steps):
                interp_x = start_x + (end_x - start_x) * (step / steps)
                interp_y = start_y + (end_y - start_y) * (step / steps)
                self.canvas.coords(self.car, interp_x, interp_y)

                
                #draw car
                # Resize the image to fit within the 200x300 rectangle
                self.rotated_image = self.image.rotate(degree)
                self.photo = ImageTk.PhotoImage(self.rotated_image)
                # Place the image inside the rectangle
                self.car=self.canvas.create_image(interp_x, interp_y, image=self.photo) 
                self.canvas.update()
                
                if timer_thread.seconds > second:
                    self.speed = self.speed + acceleration
                    
                    second=timer_thread.seconds
                    
                delay = int(100 / self.speed)
                if self.speed <= 1:
                    ok = 1
                    break
                display_speed.configure(text=f"{str(int(self.speed/0.27778))} km/h")
                self.canvas.after(delay)
            if ok == 1:
                break
        timer_thread.stop()
        if self.speed<0 or ok==1:
           self.speed=0
        display_speed.configure(text=f"{str(int(self.speed/0.27778))} km/h")

def start_car(canvas,root):

    #Path follower
    
    x,y=path_points[0]
    x_end,y_end=path_points[-1]
    path_points.insert(road_cords_number,(root.winfo_screenwidth()-71,y_end))
    x,y=path_points[0]
    ground=[(root.winfo_screenwidth()-21,y_end),(root.winfo_screenwidth()-21,root.winfo_screenheight()-31),(22,root.winfo_screenheight()-31),(21,y)]+path_points
    canvas.create_polygon(ground,fill='#57b066')
    path_follower = PathFollower(canvas, path_points)
    path_follower.draw_car(x,y)
    path_follower.draw_path()
    path_follower.move_car_along_path(root)
    #path_follower.draw_car(x_end,y_end)
    
    root.mainloop()

def interaktiv():
    clear_window()
    vissza_gomb(root,"#aceca2",home)
    canvas = tk.Canvas(root, width=width, height=height, bg="#aceca2")
    canvas.pack()
    #start button
    start_button=customtkinter.CTkButton(
        root,
        width=290, 
        height=100,
        text= "", 
        command=lambda:start_car(canvas,root), 
        state=tk.DISABLED,
        fg_color="#aceca2",
        corner_radius=20,
        bg_color="#aceca2",   
        font=("Helvetica", 30, "bold"),
        )
    start_button.place(x=center-145, y=90)
    #end button
    vissza_gomb(root,"#aceca2",home)
    x_gomb(root,"#aceca2")
    add_widgets_to_window(root,canvas,center,height,start_button)

def hatter_home():
    # Create a frame widget that spans the entire window
    frame = tk.Frame(root, bg="#dfcaae")
    frame.place(relwidth=1, relheight=1)

#
### Surlodas
#
def hatter_box_cim():
    clear_window()
    hatter_home()
    #cim frame
    main_frame = customtkinter.CTkFrame(root, fg_color="white")
    main_frame.pack(pady=0, padx=0)
    bottom_border = customtkinter.CTkFrame(main_frame, fg_color="white", height=2)
    bottom_border.pack(side="bottom", fill="x")
    return main_frame
def hatter_box_left():
    box_frame_left=customtkinter.CTkFrame(
        root,
        width=int(width_max/2.2),
        height=int(height_max/1.4),
        fg_color="#a28656",
        bg_color="#dfcaae",
        border_color="white",
        border_width=2,
        corner_radius=10

    )
    box_frame_left.place(x=int(width_max/45),y=int(height_max/4))
    return box_frame_left
def hatter_box_right():
    box_frame_right=customtkinter.CTkFrame(
        root,
        width=int(width_max/2.2),
        height=int(height_max/1.4),
        fg_color="#a28656",
        bg_color="#dfcaae",
        border_color="white",
        border_width=2,
        corner_radius=10

    )
    box_frame_right.place(x=int(width_max/1.9),y=int(height_max/4))

    return box_frame_right
def csusz_kep(content,link):
    image_path = link  # Use a raw string to handle backslashes
    image = Image.open(image_path)

    # Resize the image to fit within the desired dimensions
    image = image.resize((150, 130)) 
    photo = ImageTk.PhotoImage(image)

    # Insert the image at the end of the Text widget
    content.image_create(tk.END, image=photo)
    content.insert(tk.END,"\n","small_font")

    # Keep a reference to the image to prevent it from being garbage collected
    content.photo = photo
def csusz():

    main_frame=hatter_box_cim()
    #main_frame.pack_propagate(False)
    box_right=hatter_box_right()
    box_right.pack_propagate(False)
    box_left=hatter_box_left()
    box_left.pack_propagate(False)

    custom_font1 = ("Helvetica", 24,"bold")
    custom_font2 = ("Arial CE", 18,"bold")
    
    font_cim = Font(family="Helvetica", size=40, weight="bold")
    cim = customtkinter.CTkLabel(
        main_frame,

        width=root.winfo_screenwidth()+100,
        font=("Helvetica", 40,"bold"),
        height= font_cim.metrics("linespace")+screen_height/14,
        text="SÚRLODAS",
        fg_color="#a28656",
        corner_radius=0,
        text_color="white",
        
        
    )
    cim.pack(pady=0, padx=0)
    
    #text_content = 
    #cim.insert("1.0",  "\n\n"+text_content.center(110))  # Adjust the number of '\n' and width for proper centering

    vissza_gomb(root,"#a28656",oktato_home)
    x_gomb(root,"#a28656")

    
    content_left = tk.Text(
        box_left, 
        width=int(width_max/22)-30,
        height=int(height_max/1.4)-20,
        fg="white",
        bg="#a28656",
        font=custom_font1,
        border=0,
        )
    content_left.pack(padx=10,pady=10)

    #Tags
    content_left.tag_config('large_font', font=custom_font1)
    content_left.tag_config('small_font', font=custom_font2)

    #main content
    content_left.insert(tk.END,"Meghatározás:\n\n","large_font")
    content_left.insert(tk.END,"    Akkor jelentkezik, ha két test érintkezik és egymáshoz képest elmozdulnak. Ez az erő mindig ellentétes irányú az elmozdulással és akadályozza a mozgást.\n","small_font")
    content_left.insert(tk.END,"1. Statikus súrlódási erő \n","large_font")
    content_left.insert(tk.END,"    Lejtő:\n   A test lejtőn van egyensúlyi helyzetben. A testre ható erők: \n\n       - Súly \n       - Súrlódási erő                ","small_font")
    csusz_kep(content_left,r"kepek\Remove_2.png")
    content_left.insert(tk.END,"       - Normális erő \n\n\n\n\n","small_font")
    content_left.insert(tk.END,"Magyarázat \n","large_font")
    content_left.insert(tk.END,"A súlyerőt felbontjuk egy a lejtőre merőleges és a lejtővel párhuzamos összetevőre. A lejtőre merőleges összetevővel nyomja a test a lejtőt, amely az N normális erővel hat vissza a testre.\n","small_font")
    
    #End editing
    content_left.configure(state=tk.DISABLED)  

    content_right = tk.Text(
        box_right, 
        width=int(width_max/22)-30,
        height=int(height_max/1.4)-20,
        fg="white",
        bg="#a28656",
        font=custom_font1,
        border=0,
        )
    content_right.pack(padx=10,pady=10)
    #Tags
    content_right.tag_config('large_font', font=custom_font1)
    content_right.tag_config('small_font', font=custom_font2)
    content_right.tag_config('rly_small_font', font=("Arial",13,"bold"))

    #main content
    content_right.insert(tk.END,"   A súrlódási erő nyugalomban tartja a testet, \nkiegyenlítve a súlyerő párhuzamos összetevőjét.\n   A súrlódási erő növekedésének viszont felső \nhatára van. \n","small_font")
    content_right.insert(tk.END,"\nHa a súlyerő párhuzamos összetevője meghaladja a súrlódási erő felső határát, akkor a test lecsúszik a lejtőn\n            Fs = µs ⋅ N\n\n","rly_small_font")
    
    content_right.insert(tk.END,"  Ha a test már mozgásban van, akkor csúszó súrlódásról beszélünk.\n            Fs = µ  ⋅  N\n","rly_small_font")
    content_right.insert(tk.END,"\n2. Gördülési súrlódás \n","large_font")
    content_right.insert(tk.END,"   Az együtthato a száraz betonon 0.01 - 0.05\n\n","small_font")
    content_right.insert(tk.END,"A lassulás a következőképpen számítható:\n"
                         "\n        Fs=μ⋅N                N=Gmer                Gmer=m⋅g                Fs=m⋅a" 
                         "\na=Fs/m -> a= μ⋅N/m ->  a= μ* Gmer /m ->  a= μ* m*g /m -> a= μ* g","rly_small_font")
    content_right.insert(tk.END,"\n\n\nGyorsulás lejtőn felfele:","Large_font")
    
    content_right.insert(tk.END,"\nF1=G ⋅cosα          F2=G⋅sinα          T=Fe","rly_small_font")
    
    csusz_kep(content_right,r"Kepek\gyorsulaslejtonfelfele.png")
    content_right.insert(tk.END,"T=F1-Fs\nFe=F1-F2⋅μ\nm⋅a = G⋅sinα - G⋅cos  α⋅μ\nm⋅a =m⋅g⋅sinα - m⋅g⋅cosα⋅μ\na=g(sin α - cosα⋅μ)",
                         "rly_small_font")
    #content_right.insert(tk.END,"    Akkor jelentkezik, ha két test érintkezik és egymáshoz képest elmozdulnak. Ez az erő mindig ellentétes irányú az elmozdulással és akadályozza a mozgást.\n","small_font")
    #content_right.insert(tk.END,"    1. Csúszó súrlódási erő: \n","small_font")
    #content_right.insert(tk.END,"    2. Lejtőn lévő test: A testre ható erők","small_font")


     #End editing
    content_right.configure(state=tk.DISABLED) 

#
### Sebesseg
#
def sebesseg():

    main_frame=hatter_box_cim()
    #main_frame.pack_propagate(False)
    box_right=hatter_box_right()
    box_right.pack_propagate(False)
    box_left=hatter_box_left()
    box_left.pack_propagate(False)

    custom_font1 = ("Helvetica", 24,"bold")
    custom_font2 = ("Arial CE", 18,"bold")
    
    font_cim = Font(family="Helvetica", size=40, weight="bold")
    cim = customtkinter.CTkLabel(
        main_frame,

        width=root.winfo_screenwidth()+100,
        font=("Helvetica", 40,"bold"),
        height= font_cim.metrics("linespace")+screen_height/14,
        text="SEBESSÉG",
        fg_color="#a28656",
        corner_radius=0,
        text_color="white",
        
        
    )
    cim.pack(pady=0, padx=0)
    
    vissza_gomb(root,"#a28656",oktato_home)
    x_gomb(root,"#a28656")

    content_left = tk.Text(
        box_left, 
        width=int(width_max/22)-30,
        height=int(height_max/1.4)-20,
        fg="white",
        bg="#a28656",
        font=custom_font1,
        border=0,
        )
    content_left.pack(pady=5)

    #Tags
    content_left.tag_config('large_font', font=custom_font1)
    content_left.tag_config('small_font', font=custom_font2)

    #main content
    content_left.insert(tk.END,"    Meghatározás:\n","large_font")
    content_left.insert(tk.END,"     A sebesség egy pontszerű test (vagy egy kiterjedt test \n     egyik pontja) egy kitüntetett (másik) ponthoz viszonyított       mozgásának jellemzésére szolgáló fizikai \n     vektormennyiség.\n\n","small_font")
    content_left.insert(tk.END,"    Jele: v \n\n","large_font")
    content_left.insert(tk.END,"    Képlet: v=Δd/Δt\n    Δd - távolság\n    Δt - eltelt idő","")


    #End editing
    content_left.configure(state=tk.DISABLED)

    content_right = tk.Text(
        box_right, 
        width=int(width_max/22)-30,
        height=int(height_max/1.4)-20,
        fg="white",
        bg="#a28656",
        font=custom_font1,
        border=0,
        )
    content_right.pack(pady=5)
    #Tags
    content_right.tag_config('large_font', font=custom_font1)
    content_right.tag_config('small_font', font=custom_font2)

    #main content
    content_right.insert(tk.END,"   Feladat:\n","large_font")
    content_right.insert(tk.END,"    Egy autó nyugalmi állapotból indul és 3 óra alatt \n    180 km-t tesz meg. Számítsd ki az autó sebességét \n    gyorsulását!\n\n","small_font")
    content_right.insert(tk.END,"    Megoldás:\n","large_font")
    content_right.insert(tk.END,"     A sebességét úgy számíthatjuk ki, hogy a \n     a megtett távolságot elosztjuk az eltelt idővel.\n      A feladat megoldása, így 60 km/h.","small_font")

     #End editing
    content_right.configure(state=tk.DISABLED) 
#
### gyorsulas
#
def gyorsulas():

    
    main_frame=hatter_box_cim()
    #main_frame.pack_propagate(False)
    box_right=hatter_box_right()
    box_right.pack_propagate(False)
    box_left=hatter_box_left()
    box_left.pack_propagate(False)

    custom_font1 = ("Helvetica", 24,"bold")
    custom_font2 = ("Arial CE", 18,"bold")
    
    font_cim = Font(family="Helvetica", size=40, weight="bold")
    cim = customtkinter.CTkLabel(
        main_frame,

        width=root.winfo_screenwidth()+100,
        font=("Helvetica", 40,"bold"),
        height= font_cim.metrics("linespace")+screen_height/14,
        text="GYORSULÁS",
        fg_color="#a28656",
        corner_radius=0,
        text_color="white",
        
        
    )
    cim.pack(pady=0, padx=0)
    
    vissza_gomb(root,"#a28656",oktato_home)
    x_gomb(root,"#a28656")

    content_left = tk.Text(
        box_left, 
        width=int(width_max/22)-30,
        height=int(height_max/1.4)-20,
        fg="white",
        bg="#a28656",
        font=custom_font1,
        border=0,
        )
    content_left.pack(pady=5)

    #Tags
    content_left.tag_config('large_font', font=custom_font1)
    content_left.tag_config('small_font', font=custom_font2)

    #main content
    content_left.insert(tk.END,"    Meghatározás:\n","large_font")
    content_left.insert(tk.END,"     A gyorsulás az a fizikai mennyiség, amely megmutatja,\n     hogy egy testnek milyen gyorsan változik a sebessége.\n\n","small_font")
    content_left.insert(tk.END,"    Jele: a \n\n","large_font")
    content_left.insert(tk.END,"    Képlet: a=Δv/Δt\n    Δv - átlag sebesség\n    Δt - eltelt idő","")


    #End editing
    content_left.configure(state=tk.DISABLED)

    content_right = tk.Text(
        box_right, 
        width=int(width_max/22)-30,
        height=int(height_max/1.4)-20,
        fg="white",
        bg="#a28656",
        font=custom_font1,
        border=0,
        )
    content_right.pack(pady=5)
    #Tags
    content_right.tag_config('large_font', font=custom_font1)
    content_right.tag_config('small_font', font=custom_font2)

    #main content
    content_right.insert(tk.END,"   Feladat:\n","large_font")
    content_right.insert(tk.END,"    Egy autó nyugalmi állapotból indul és 5 másodperc alatt \n    éri el a 25 m/s sebességet. Számítsd ki az autó átlagos \n    gyorsulását!\n\n","small_font")
    content_right.insert(tk.END,"    Megoldás:\n","large_font")
    content_right.insert(tk.END,"     A gyorsulást úgy számíthatjuk ki, hogy a \n     sebességváltozást elosztjuk az eltelt idővel.\n      A gyorsulás képletét a következőképpen írhatjuk fel:","small_font")

     #End editing
    content_right.configure(state=tk.DISABLED)
    
    #csuszkep()
#
### gravitacio
#
def gravitacio():

    
    main_frame=hatter_box_cim()
    #main_frame.pack_propagate(False)
    box_right=hatter_box_right()
    box_right.pack_propagate(False)
    box_left=hatter_box_left()
    box_left.pack_propagate(False)

    custom_font1 = ("Helvetica", 24,"bold")
    custom_font2 = ("Arial CE", 18,"bold")
    
    font_cim = Font(family="Helvetica", size=40, weight="bold")
    cim = customtkinter.CTkLabel(
        main_frame,

        width=root.winfo_screenwidth()+100,
        font=("Helvetica", 40,"bold"),
        height= font_cim.metrics("linespace")+screen_height/14,
        text="GRAVITÁCIÓ",
        fg_color="#a28656",
        corner_radius=0,
        text_color="white",
        
        
    )
    cim.pack(pady=0, padx=0)
    

    vissza_gomb(root,"#a28656",oktato_home)
    x_gomb(root,"#a28656")

    content_left = tk.Text(
        box_left, 
        width=int(width_max/22)-30,
        height=int(height_max/1.4)-20,
        fg="white",
        bg="#a28656",
        font=custom_font1,
        border=0,
        )
    content_left.pack(pady=5)

    #Tags
    content_left.tag_config('large_font', font=custom_font1)
    content_left.tag_config('small_font', font=custom_font2)

    #main content
    content_left.insert(tk.END,"    Meghatározás:\n","large_font")
    content_left.insert(tk.END,"     A gravitáció az a természetes erő, amely vonzást\n     gyakorol minden tömeggel rendelkező objektum között.\n\n","small_font")
    content_left.insert(tk.END,"    Jele: F \n\n","large_font")
    content_left.insert(tk.END,"    Newton gravitációs törvénye:\n    F=(G*m1*m2)/r*r\n    F - gravitációs erő\n    G - gravitációs állandó\n    m1, m2 - két test tömege\n    r - a köztük lévő távolság","")


    #End editing
    content_left.configure(state=tk.DISABLED)

    content_right = tk.Text(
        box_right, 
        width=int(width_max/22)-30,
        height=int(height_max/1.4)-20,
        fg="white",
        bg="#a28656",
        font=custom_font1,
        border=0,
        )
    content_right.pack(pady=5)
    #Tags
    content_right.tag_config('large_font', font=custom_font1)
    content_right.tag_config('small_font', font=custom_font2)

    #main content
    content_right.insert(tk.END,"   Gravitációs hullámok:\n","large_font")
    content_right.insert(tk.END,"    A gravitációs hullámok a téridő görbületének hullámai,\n    amelyeket nagy tömegű objektumok gyorsulása hoz létre,      például összeütköző fekete lyukak. Ezeket először \n    2015-ben detektálták.\n\n","small_font")
    content_right.insert(tk.END,"   Gravitációs hatások a mindennapi életben:\n","large_font")
    content_right.insert(tk.END,"     A gravitáció felelős a földfelszínen tapasztalt súlyért, a \n     bolygók mozgásáért a Nap körül, valamint a dagályért. ","small_font")

     #End editing
    content_right.configure(state=tk.DISABLED)
    
    #csuszkep()
#
### Oktato_library 
#
def hatter_oktato():
    frame = tk.Frame(root, bg="#dfcaae")
    frame.place(relwidth=1, relheight=1) 

def sebesseg_gomb():
    bam=customtkinter.CTkButton(root,text = "Sebesseg",command=sebesseg,width=screen_width/4,height=screen_height/4,font=("Helvetica", 30, "bold"),bg_color="#dfcaae",fg_color="#a28656",hover_color="RED")
    bam.place(x=screen_width*2/8-20,y=screen_height/4-20)

def gyorsulas_gomb():
    bam=customtkinter.CTkButton(
        root,
        text = "Gyorsulás",
        command=gyorsulas,
        width=screen_width/4,
        height=screen_height/4,
        bg_color="#dfcaae",
        font=("Helvetica", 30, "bold"),
        fg_color="#a28656"
        )
    bam.place(x=screen_width*4/8+20,y=screen_height/4-20)

def grav_gomb():
    bam=customtkinter.CTkButton(root,text = "Gravitáció",command=gravitacio,width=screen_width/4,height=screen_height/4,font=("Helvetica", 30, "bold"),bg_color="#dfcaae",fg_color="#a28656")
    bam.place(x=screen_width*2/8-20,y=screen_height*2/4+20)

def csusz_gomb():
    bam=customtkinter.CTkButton(root,text = "Súrlódás",command=csusz,width=screen_width/4,height=screen_height/4,font=("Helvetica", 30, "bold"),bg_color="#dfcaae",fg_color="#a28656",hover_color="REd")
    bam.place(x=screen_width*4/8+20,y=screen_height*2/4+20)

def oktato_home():
    clear_window()
    hatter_oktato()
    vissza_gomb(root,"#dfcaae",home)
    sebesseg_gomb()
    grav_gomb()
    gyorsulas_gomb()
    csusz_gomb()
    x_gomb(root,"#dfcaae")
    Oktato_cim=customtkinter.CTkLabel(root,text="Oktató",font=("Helvetica", 50,"bold"),width=30,height=10,fg_color="#dfcaae",text_color="#a28656")
    Oktato_cim.place(x=screen_width/2-80,y=100) 

#
### Home
#
photo = tk.PhotoImage(file=r"Kepek\player.png")
photoimage = photo.subsample(8, 8)
photo1 = tk.PhotoImage(file=r"Kepek\learning_1.png")
photoimage1 = photo1.subsample(3, 3)
photo2 = tk.PhotoImage(file=r"Kepek\player.png")
photoimage2 = photo2.subsample(3, 3)
oktato_image = tk.PhotoImage(file=r'Kepek\player.png')

def labjegyzek():
    width=root.winfo_screenwidth()
    height=root.winfo_screenheight()
    labjegyzekunk = tk.Label(root, text = "Fekete Krisztián | Török Gábriel | Kovács Jázmán-Mónika | Koncz Nimród-Kálmán", fg="#a28656", font = "Arial 15 bold", background="#dfcaae")
    labjegyzekunk.place(x=width/2-385, y=height-50)

def home_box_cim():
    #cim frame
    coregde=customtkinter.CTkFrame(
        root,
        width=int(width_max/3),
        height=int(height_max/6),
        fg_color="#a28656",
        bg_color="#dfcaae",
        border_width=2,
        border_color="Black",
        corner_radius=10

    )
    coregde.pack()
    return coregde

def cim_home():
    main_frame=home_box_cim()
    cim = customtkinter.CTkTextbox(
        main_frame,
        width=int(width_max/6.2),
        height=int(height_max/6)-30,
        font=("Arial", 40,"bold"),
        fg_color="#a28656",
        bg_color="#a28656",
        text_color="white",

        
    )    
    cim.insert(tk.END,"DINAMIKA")
    cim.configure(state=tk.DISABLED)
    cim.place(x=screen_width/11,y=10)
def gombok():


    oktato_button = customtkinter.CTkButton(
        root, 
        text=None,
        bg_color ="#dfcaae", 
        command=oktato_home,
        width=screen_width/4,
        height=screen_height/4,
        font=("Helvetica", 30, "bold"),
        fg_color="#a28656",
        image=photoimage1, 
        compound="bottom", 
        cursor = "hand2",
        border_width=2,
        border_color="black",
         hover_color="#A71606"
        )
    oktato_button.place(x=screen_width/4-10, y=screen_height/3)


    button = customtkinter.CTkButton(
        root, 
        text=None,
        bg_color ="#dfcaae", 
        image=photoimage2, 
        command=interaktiv, 
        width=screen_width/4,
        height=screen_height/4,
        fg_color="#a28656", 
        font=("Helvetica", 30, "bold"),
        compound="bottom",
        cursor = "hand2",
        border_width=2,
        border_color="black",
        hover_color="#A71606"
        
        )
    
    button.place(x=screen_width/2+10, y=screen_height/3)
def home():
    clear_window()
    hatter_home()
    cim_home()
    labjegyzek()
    gombok()
    x_gomb(root,"#dfcaae")

home()
# Run the Tkinter event loop
root.mainloop()


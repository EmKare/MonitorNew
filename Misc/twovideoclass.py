import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
import time

# widgets with canvas and camera

class App:

    def __init__(self, window, window_title, video_source1=None, video_source2=None,video_source3=None, video_source4=None,):
        self.window = window

        self.window.title(window_title)
        self.window.geometry("1200x800+10+0")
        
        # open video source (by default this will try to open the computer webcam)
        self.canvas1 = tkinter.LabelFrame(self.window, text="Vid 1")
        self.canvas1.place(x = 0, y = 0, width=500, height=400)
        if video_source1 is not None:            
            self.vid1 = tkCamera(self.canvas1, video_source1)
            self.vid1.place(x = 0, y = 0)
        
        self.canvas2 = tkinter.LabelFrame(self.window, text="Vid 2")
        self.canvas2.place(x = 550, y = 0, width=500, height=400)
        if video_source2 is not None:
            self.vid2 = tkCamera(self.canvas2, video_source2)
            self.vid2.pack()
        
        self.canvas3 = tkinter.LabelFrame(self.window, text="Vid 3")
        self.canvas3.place(x = 0, y = 400, width=500, height=400)
        if video_source3 is not None:
            self.vid3 = tkCamera(self.canvas3, video_source3)
            self.vid3.pack()
            
        self.canvas4 = tkinter.LabelFrame(self.window, text="Vid 4")
        self.canvas4.place(x = 550, y = 400, width=500, height=400)
        if video_source4 is not None:
            self.vid4 = tkCamera(self.canvas4, video_source4)
            self.vid4.pack()
        
        # Create a canvas that can fit the above video source size
         
        self.window.mainloop()
        
class tkCamera(tkinter.LabelFrame):
    
    def __init__(self, window, video_source=0):
        super().__init__(window)
        
        self.window = window
        
        #self.window.title(window_title)
        self.video_source = video_source

        self.setVid()

        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.place(x = 0, y = 0)
         
        # Button that lets the user take a snapshot
        self.btn_start = tkinter.Button(window, text="Start", command=self.update_widget)
        self.btn_start.place(x = 0, y = 310, width=100)
        
        self.btn_snapshot = tkinter.Button(window, text="Stop", command=self.remove)
        self.btn_snapshot.place(x = 130, y = 310,  width=100)
        
        self.btn_stop = tkinter.Button(window, text="Snapshot", command=self.snapshot)
        self.btn_stop.place(x = 260, y = 310,  width=100)
        
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
    
    def setVid(self):
        self.vid = MyVideoCapture(self.video_source)

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    
    def update_widget(self):
        # Get a frame from the video source
        if self.vid is None:
            self.setVid()
        ret, frame = self.vid.get_frame()
        
        if ret:
            self.image = PIL.Image.fromarray(frame)
            self.photo = PIL.ImageTk.PhotoImage(image=self.image)
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW,)
        
        self._job = self.window.after(self.delay, self.update_widget)
            
    def cancel(self):
        if self._job:
            self.window.after_cancel(self._job)
            self._job = False
        
    def remove(self):
        self.photo = tkinter.PhotoImage(width = self.canvas.winfo_reqwidth(), height = self.canvas.winfo_reqheight())
        self.vid.remove()        
        self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.cancel()
        self.vid = None
        
     
class MyVideoCapture:
    def __init__(self, video_source=None):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
    
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
        self.width = 400
        self.height = 350
    
    def get_frame(self):
    
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.resize(frame, (400, 300))
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
    
    # Release the video source when the object is destroyed
    def remove(self):
        if self.vid.isOpened():
            self.vid.release()
            cv2.destroyAllWindows()


v1 = r"C:/Users/DELL/Desktop/MyJourney/Python/Parking/New folder/carPark.mp4"
v2 = r"C:\Users\DELL\Desktop\MyJourney\Python\OpenCV Course\Resources\Videos\kitten.mp4"
v3 = r"C:\Users\DELL\Desktop\MyJourney\Python\Parking\parking-space-counter-master\data\parking_1920_1080_loop.mp4"
v4 = r"C:\Users\DELL\Desktop\MyJourney\Python\Parking\parking-space-counter-master\data\parking_crop_loop.mp4"
# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV", v1, v2, v3, v4)





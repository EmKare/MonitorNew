from tkinter import LabelFrame, Canvas, Button, PhotoImage, NW
from PIL import Image, ImageTk
from time import strftime, localtime
import cv2 as cv

class Camera(LabelFrame):
    
    def __init__(self, window, display, title = "", video_source = None):
        super().__init__(window)
        
        self.window = window
        self.width, self.height = window.winfo_reqwidth(), window.winfo_reqheight()
        self.title = title
        self.video_source = video_source
        self.active_playing = False
        
        self.startFeedSymbol = "\u25B6"
        self.stopFeedSymbol = "\u25A0"        
        self.recordingSymbol = "\u26AB"        
        self.snapshotSymbol = "\U0001F4F7"

        if display == 1:
            self.setSingle_DoubleViewDisplay()
        if display == 2:
            self.setQuadViewDisplay()
        
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
    
    def setVid(self):
        try:
            self.vid = MyVideoCapture(video_source = self.video_source, width = self.width, height = self.height)
            self.active_playing = True
        except Exception:
            pass

    def snapshot(self):
        # Get a frame from the video source
        try:
            ret, frame = self.vid.get_frame()
            if ret:
                cv.imwrite("frame-" + strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv.cvtColor(frame, cv.COLOR_RGB2BGR))
        except Exception:
            pass
        
    def config_startButton(self):
        self.setVid()
        self.btn_startstop.config(text = f"{self.stopFeedSymbol}", command = lambda : self.remove(), fg = "black")
        self.update_widget()
    
    def update_widget(self):
        # Get a frame from the video source
        if self.vid is None:
            self.setVid()
        ret, frame = self.vid.get_frame()
        
        if ret:
            frame = self.rescale(frame, self.width, self.height)
            cv.putText(frame, self.title, (10,20), cv.FONT_HERSHEY_TRIPLEX, 0.4, (0,0,0), thickness = 1)
            if self.vid.recording:
                self.vid.record(frame)
                cv.putText(frame, "Recording", (10,30), cv.FONT_HERSHEY_TRIPLEX, 0.4, (255,0,0), thickness = 1)         
            self.image = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=self.image)
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW,)
        
        self._job = self.window.after(self.delay, self.update_widget)
            
    def cancel(self):
        if self._job:
            self.window.after_cancel(self._job)
            self._job = False
        
    def remove(self):
        self.photo = PhotoImage(width = self.canvas.winfo_reqwidth(), height = self.canvas.winfo_reqheight())
        self.vid.remove()        
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
        self.cancel()
        self.vid = None
        try:
            self.stopRecording()
        except Exception:
            pass
        self.btn_startstop.config(text = f"{self.startFeedSymbol}", command = lambda : self.config_startButton(), fg = "green")
        self.active_playing = False
        
    def rescale(self, frame, width, height):
        dimensions = (width, height)
        return cv.resize(frame, dimensions, interpolation = cv.INTER_AREA)
    
    def startRecording(self):
        try:
            if self.vid:
                self.btn_startstop_record.config(text = f"{self.recordingSymbol}", command = lambda : self.stopRecording(), fg = "red")
                self.vid.start_recording()
        except Exception:
            pass
            
    def stopRecording(self):
        if self.vid:            
            self.vid.stop_recording()
        self.btn_startstop_record.config(text = f"{self.recordingSymbol}", command = lambda : self.startRecording(), fg = "black") 
    
    def setSingle_DoubleViewDisplay(self):
        self.canvas = Canvas(self.window, width=self.width-19, height=self.height-60, bg = "white", border = 5,  bd = 5, highlightbackground = "black", highlightcolor= "black",  )
        self.canvas.place(x = 0, y = 0)
         
        # Buttons     
        self.btn_startstop = Button(self.window, text = f"{self.startFeedSymbol}", font = ('bold', 25), fg = "green", relief = "flat", command = lambda : self.config_startButton())        
        self.btn_startstop.place(x = 0, y = self.height - 45, width = int(self.width / 3) - 2, height = 40)
        
        self.btn_startstop_record = Button(self.window, text = f"{self.recordingSymbol}", font = ('bold', 10), fg = "black", relief = "flat", command = lambda : self.startRecording())
        self.btn_startstop_record.place(x = int(self.width / 3) , y = self.height - 45, width = int(self.width / 3) - 2, height = 40)
        
        self.btn_snapshot = Button(self.window, text = f"{self.snapshotSymbol}", font = ('bold', 15), fg = "blue", relief = "flat", command = lambda : self.snapshot())
        self.btn_snapshot.place(x = (int(self.width / 3) * 2) , y = self.height - 45, width = int(self.width / 3) - 2, height = 40)
        
    def setQuadViewDisplay(self):
        self.canvas = Canvas(self.window, width = self.width-80, height = self.height-11, bg = "white",   bd = 1, highlightbackground = "black", highlightcolor= "black",  )
        self.canvas.place(x = 0, y = 0)
        self.btn_startstop = Button(self.window, text = f"{self.startFeedSymbol}", font = ('bold', 25), fg = "green", relief = "flat", command = lambda : self.config_startButton(),)
        self.btn_startstop.place(x = self.canvas.winfo_reqwidth(), 
                                       y = 0, 
                                       width = 72,
                                       height = int(self.height / 3) - 2)
        self.btn_startstop_record = Button(self.window, text = f"{self.recordingSymbol}", font = ('bold', 10), fg = "black", relief = "flat", command = lambda : self.startRecording())
        self.btn_startstop_record.place(x = self.canvas.winfo_reqwidth(), 
                                       y = int(self.height / 3) - 1, 
                                       width = 72,
                                       height = int(self.height / 3) - 2)
        self.btn_snapshot = Button(self.window, text = f"{self.snapshotSymbol}", font = ('bold', 15), fg = "blue", relief = "flat", command = lambda : self.snapshot(),)
        self.btn_snapshot.place(x = self.canvas.winfo_reqwidth(), 
                                       y = (int(self.height / 3) * 2) - 2, 
                                       width = 72,
                                       height = int(self.height / 3) - 2)


class MyVideoCapture:
    def __init__(self, video_source=None, width = 0, height = 0, fps = None):
        # Open the video source
        self.video_source = video_source
        self.vid = cv.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.fps = int(self.vid.get(cv.CAP_PROP_FPS))  # convert float to int
        
        # Get video source width and height
        self.width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)
    
        self.width = width
        self.height = height
        if not self.fps:
            self.fps = int(self.vid.get(cv.CAP_PROP_FPS))  # convert float to int
        
        # default values for recording        
        self.recording = False
        self.recording_filename = 'output.mp4'
        self.recording_writer = None
    
    def get_frame(self):
    
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame = cv.resize(frame, (400, 300))

                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
    
    # Release the video source when the object is destroyed
    def remove(self):
        if self.vid.isOpened():
            self.vid.release()
            cv.destroyAllWindows()
                
    def start_recording(self, filename=None):
        if self.recording:
            print('[MyVideoCapture] already recording:', self.recording_filename)
        else:
            # VideoWriter constructors
            #.mp4 = codec id 2
            if filename:
                self.recording_filename = filename
            else:
                self.recording_filename = strftime("%Y.%m.%d %H.%M.%S", localtime()) + ".avi"
            #fourcc = cv.VideoWriter_fourcc(*'I420') # .avi
            #fourcc = cv.VideoWriter_fourcc(*'MP4V') # .avi
            fourcc = cv.VideoWriter_fourcc(*'MP42') # .avi
            #fourcc = cv.VideoWriter_fourcc(*'AVC1') # error libx264
            #fourcc = cv.VideoWriter_fourcc(*'H264') # error libx264
            #fourcc = cv.VideoWriter_fourcc(*'WRAW') # error --- no information ---
            #fourcc = cv.VideoWriter_fourcc(*'MPEG') # .avi 30fps
            #fourcc = cv.VideoWriter_fourcc(*'MJPG') # .avi
            #fourcc = cv.VideoWriter_fourcc(*'XVID') # .avi
            #fourcc = cv.VideoWriter_fourcc(*'H265') # error 
            self.recording_writer = cv.VideoWriter(self.recording_filename, fourcc, self.fps, (self.width, self.height))
            self.recording = True
            print('[MyVideoCapture] started recording:', self.recording_filename)        
    
    def stop_recording(self):
        if not self.recording:
            print('[MyVideoCapture] not recording')
        else:
            self.recording = False
            self.recording_writer.release() 
            print('[MyVideoCapture] stop recording:', self.recording_filename)
               
    def record(self, frame):
        # write frame to file         
        if self.recording_writer and self.recording_writer.isOpened():
            self.recording_writer.write(frame)
 
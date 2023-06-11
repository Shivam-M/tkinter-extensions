from tkinter import Tk, Frame, Label
from threading import Thread
from PIL import Image, ImageTk
import imageio, time

class VideoPlayer(Frame):
    def __init__(self, master, file_path, **kwargs):
        super().__init__(master, **kwargs)
        self.been_loaded = False
        self.video_playing = False
        self.video_object = None
        self.video_path = file_path
        self.video_settings = {}
        self.video_progress = 0.00
        self.target_fps = 20
        self.content = Label(self, bg=kwargs.get("bg", "#FFFFFF"))
        self.content.place(x=0, y=0)
        self.progress_bar = Frame(self, bg=kwargs.get("bg", "#FFFFFF"), width=self.cget("width"), height=5)
        self.progress_fill = Frame(self, bg=kwargs.get("fg", "#1abc9c"), width=1, height=5)

    def settings(self, **kwargs):
        self.video_settings = kwargs
        self.target_fps = self.video_settings.get("fps", 20)
        self.progress_fill.config(bg=kwargs.get("colour", "#1abc9c"))
        if self.video_settings.get("progress_bar", False):
            self.progress_bar.place(x=0, y=0.99)
            self.progress_fill.place(relx=0.0, rely=0.99)
        else:
            self.progress_bar.place_forget()
            self.progress_fill.place_forget()

    def _load(self):
        self.video_object = imageio.get_reader(self.video_path)
        self.target_fps = self.video_settings.get("fps", self.video_object.get_meta_data()["fps"])
        self.been_loaded = True

    def load_threaded(self):
        Thread(target=self._load).start()

    def load(self):
        self._load()

    def _play(self):
        if not self.been_loaded: self._load()
        frame_counter = 0
        frame_rate = self.video_object.get_meta_data()["fps"]
        for frame in self.video_object.iter_data():
            start_time = time.time()
            frame_counter += 1
            if frame_counter % (frame_rate / self.target_fps) != 0: continue
            image = Image.fromarray(frame).resize((self.cget("width") - 4, self.cget("height") - 4), Image.ANTIALIAS)
            frame_image = ImageTk.PhotoImage(image)
            self.content.config(image=frame_image)
            self.content.image = frame_image
            self.video_progress = frame_counter / (self.video_object.get_meta_data()["duration"] * self.video_object.get_meta_data()["fps"])
            if self.video_settings.get("progress_bar", False): self.progress_fill.config(width=self.video_progress * self.cget("width"))
            if not self.video_playing: break
            time.sleep(1.0 / frame_rate - (time.time() - start_time))
        self.video_playing = False
        if self.video_settings.get("auto_replay", False): self.play()
        if self.video_settings.get("hide_after_play", False):
            self.place_forget()
            self.pack_forget()

    def play(self):
        if not self.video_playing:
            self.video_playing = True
            Thread(target=self._play).start()

    def stop(self):
        self.video_settings["auto_replay"] = False
        self.video_playing = False

import tkinter as tk
import datetime
from tkinter import ttk

from tkVideoPlayer import TkinterVideo

class TkinterVideoPlayer:
    def __init__(self, root, video_location):           
        self.video_player_frame = ttk.Frame(root, padding=10)
        self.video_player_frame.columnconfigure(100, weight=1)
        self.video_player_frame.rowconfigure(100, weight=1)
        
        try:
            self.video_player = TkinterVideo(scaled=True, master=self.video_player_frame)
            self.video_player.load(video_location)
            self.video_player.pack(fill="both", expand=True, padx=10, pady=10)
        except Exception as e:
            raise Exception(f'Could not find {video_location}: {str(e)}')
        
        self.duration = self.video_player.video_info()['duration']
        self.is_paused = True
        
        self.play_pause_btn = tk.Button(self.video_player_frame, text="Play", command=self.play_pause)
        self.start_time = tk.Label(self.video_player_frame, text=str(datetime.timedelta(seconds=0)))
        self.end_time = tk.Label(self.video_player_frame, text= str(datetime.timedelta(seconds=self.duration)))
        self.skip_minus_10sec = tk.Button(self.video_player_frame, text="Skip -10 sec", command=lambda: self.skip(-10))
        self.skip_plus_10sec = tk.Button(self.video_player_frame, text="Skip +10 sec", command=lambda: self.skip(10))
        self.progress_slider = tk.Scale(self.video_player_frame, from_=0, to=0, orient="horizontal")
        self.progress_slider['to'] = self.duration
        self.progress_slider.bind("<ButtonRelease-1>", self.seek)
        
        
        self.play_pause_btn.pack()
        self.skip_minus_10sec.pack(side="left")
        self.start_time.pack(side="left")
        self.progress_slider.pack(side="left", fill="x", expand=True)
        self.end_time.pack(side="left")
        self.skip_plus_10sec.pack(side="left")
        
        self.video_player.bind("<<SecondChanged>>", self.update_scale)
        self.video_player.bind("<<Duration>>", self.update_duration)
        self.video_player.bind("<<Ended>>", self.video_ended)
    
    def play_pause(self):
        if self.is_paused:
            self.video_player.play()
            self.play_pause_btn['text'] = 'Pause'
        else:
            self.video_player.pause()
            self.play_pause_btn['text'] = 'Play'
            
        self.is_paused = not self.is_paused
            
    def seek(self, event=None):
        self.video_player.seek(int(self.progress_slider.get()))
        
    def skip(self, value: int):
        self.video_player.seek(int(self.progress_slider.get()) + value)
        self.progress_slider.set(self.progress_slider.get() + value)
        
    def update_duration(self, event):
        duration = self.video_player.video_info()["duration"]
        self.end_time["text"] = str(datetime.timedelta(seconds=duration))
        self.progress_slider['to'] = duration
        
    def update_scale(self, event):
        self.progress_slider.set(self.video_player.current_duration())
        
    def video_ended(self, event):
        self.progress_slider.set(progress_slider['to'])
        self.play_pause_btn['text'] = 'Play'
        self.progress_slider.set(0)
        
    # Figure out later, an experienced tkinter developer should be able to fix this in 10 minutes.
    def set_grid(self, _row: int = 0, _column: int = 0, rowspan: int = 5, columnspan: int = 5):
        self.video_player_frame.grid(row=_row, column=_column, rowspan=rowspan, columnspan=columnspan, sticky="nesw")

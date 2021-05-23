# tkinter-extensions
Extra set of widgets to use with tkinter

## Video Player
### Usage
#### `VideoPlayer(master, file_path, **kwargs)`
> `master (Tk)` root window<br>
> `file_path (str)` path to video file<br>
> `**kwargs` based on `tk.Frame`

##### `settings(**kwargs)`
> `progress_bar (bool) def. False` show progress bar<br>
> `colour (str) def. blue` progress bar colour as hex or name<br>
> `auto_replay (bool) def. False` automatically replay after finish<br>
> `hide_after_play (bool) def. False` unplace or unpack after finish<br>
> `fps (int) def. 20` specify target framerate

##### `load_threaded()` `load the video in a new Thread`
##### `load()` `load the video on the main thread`
##### `play()` `play the video, if unloaded, will load on the main thread`
##### `stop()` `stop/freeze the video, call play() to start again`

### Example
```Python
root = Tk()

vid = VideoPlayer(root, "example.mp4", width=1280, height=720, bg="#34495E")
vid.settings(progress_bar=True, colour="red")
vid.load()
vid.pack()

Button(root, text="Play", command=lambda: vid.play()).pack()

root.mainloop()
```

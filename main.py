import kassandra


display = kassandra.Display()

image = kassandra.load_image("image.png", size=(60, 50))
camera = kassandra.Camera((500, 500), (100, 0), scale=2)
display.add_camera(camera)
sprite = kassandra.Sprite((60, 50), (0, 0), image=image)
camera.add_sprite(sprite)

def callback(self) -> None:
    print(self.delta_time)
    pass

display.set_update_callback(callback)
display.mainloop()

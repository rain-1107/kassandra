import kassandra


display = kassandra.Display()

image = kassandra.load_image("test", size=(50, 50))
sprite = kassandra.Sprite((0, 0), (50, 50), image=image)
camera = kassandra.Camera(display, (100, 100), (0, 0))
# display._add_camera(camera)
camera.add_sprite(sprite)
display.mainloop()

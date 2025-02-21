import kassandra


display = kassandra.Display()

image = kassandra.load_image("image.png", size=(250, 250))
camera = kassandra.Camera((500, 500), display_position=(0, 0), scale=1)

display.compile_program("funky", frag="fragment.glsl")
camera.shader_program_name = "funky"

t = 0

def callback(camera: kassandra.Camera, program: kassandra.moderngl.Program):
    global t
    program["tex"] = camera.id
    program["time"] = t
    t += 1

camera.set_uniform_callback(callback)
display.add_camera(camera)
sprite = kassandra.Sprite((250, 250), (125, 125), image=image)
sprite.position = kassandra.Vector2(125, 250)
camera.add_sprite(sprite)


def calls_every_update(display: kassandra.Display):
    print(display.delta_time)

display.set_update_callback(calls_every_update)

display.mainloop()

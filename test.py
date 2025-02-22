import kassandra

window = kassandra.Window((500, 500), fullscreen=False)

surface = kassandra.display.GLSurface(window, (500, 500))

@window.on_update
def update(ctx: kassandra.Window) -> None:
    surface.update() 

@surface.uniform_setter
def set_uniforms(ctx: kassandra.display.GLSurface) -> None:
    print("test")

window.start()

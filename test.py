import kassandra

window = kassandra.Window()

@window.on_update
def cool(ctx):
    print("test")

window.update()

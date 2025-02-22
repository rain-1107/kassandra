import pygame
import moderngl
from pyglm import glm
import ctypes
from typing import Tuple, List, Dict
from .core import * 

class SHADERS:
    BASIC_VERTEX = """
    #version 330
    in vec2 in_vert;
    in vec2 in_texcoord;
    out vec2 texcoord;
    void main() {
        gl_Position = vec4(in_vert.x, in_vert.y, 0.0, 1.0);
        texcoord = in_texcoord;
    }
    """

    BASIC_FRAGMENT = """
    #version 330
    uniform sampler2D texture0;
    in vec2 texcoord;
    out vec4 fragColor;
    void main() {
        fragColor = texture2D(texture0, texcoord);
    }
    """
    AREA_VERTEX = """
    #version 330
    
    uniform vec2 top_left;
    uniform vec2 area;

    in vec2 in_vert;
    in vec2 in_texcoord;
    out vec2 texcoord;
    void main() {
        gl_Position = vec4(top_left + (area * in_vert), 1.0, 1.0);
        texcoord = in_texcoord;
    }
    """

    SIMPLE_INSTANCED_VERTEX = """
    #version 330
    in vec2 in_vert;
    in vec2 in_texcoord;
    uniform vec3 offset[255];
    out vec2 texcoord;

    void main() {
        gl_Position = vec4(in_vert + offset[gl_InstanceID].xy, offset[gl_InstanceID].z, 1.0);
        texcoord = in_texcoord;
    }
    """


class Window(BaseObject):
    def __init__(self, size: IVectorLike, **kwargs) -> None:
        super().__init__()
        self.running = True

        # Basic pygame setup
        self.size: Tuple[int, int] = (size[0], size[1])
        pygame_options = pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE
        if kwargs.get("fullscreen", False):
            pygame_options = pygame_options | pygame.FULLSCREEN
        self.display: pygame.Surface = pygame.display.set_mode(self.size, pygame_options)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.fps: int = kwargs.get("fps", 60)
        self.delta_time: float = 1/self.fps

        # OpenGL init
        self.ctx = moderngl.create_context()
        self.ctx.gc_mode = "context_gc"
        vertex_array = glm.array.from_numbers(ctypes.c_float, 
            # position (x, y) , texture coordinates (x, y)
            -1.0, 1.0, 0.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, 1.0, 1.0, 0.0,
            1.0, -1.0, 1.0, 1.0,)
        self.quad_buffer = self.ctx.buffer(data=vertex_array)
        self.texture_cache: Dict[str, moderngl.Texture] = {}
        self.program_cache: Dict[Tuple[str, str], Tuple[moderngl.Program, moderngl.VertexArray]] = {}
        self.ready()

    def start(self) -> None:
        while self.running:
            self.update()

    def _object_update_method(self) -> None:
        self.delta_time = self.clock.tick(self.fps) / 1000 
        for _ in pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            self.running = False
            return
        pygame.display.flip()
        self.ctx.screen.clear(0, 0, 0)

    def compile_shader(self, vertex_shader: str, fragment_shader: str) -> Tuple[moderngl.Program, moderngl.VertexArray]:
        program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
        return (program, self.ctx.vertex_array(program, [(self.quad_buffer, "2f 2f", "in_vert", "in_texcoord")])) 

    def surface_to_texture(self, surface: pygame.Surface, **options) -> moderngl.Texture:
        channels = 4
        texture = self.ctx.texture(surface.get_size(), channels, surface.get_buffer().raw)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = "BGRA"
        texture.repeat_x = options.get("repeat_x", False)
        texture.repeat_y = options.get("repeat_y", False)
        texture.write(surface.get_view("1"))
        return texture


class Sprite(BaseObject):
    def __init__(self, window: Window, image: pygame.Surface, size: IVectorLike, position: IVectorLike = (0, 0), **kwargs) -> None:
        super().__init__()
        self.window = window
        self.image = image
        self.size = (size[0], size[1])
        self.position = (position[0], position[1])


class GLSurface(BaseObject):
    def __init__(self, window: Window, size: IVectorLike, **kwargs) -> None:
        super().__init__()
        self.window = window
        self.size = (size[0], size[1])
        self.fbo = self.window.ctx.framebuffer(
            color_attachments=[self.window.ctx.texture(self.size, 4)]
        )
        self._custom_shader = False
        if kwargs.get("shader_program", None):
            self.program, self.vertex_array = kwargs["shader_program"]
            self._custom_shader = True
        else:
            self.program, self.vertex_array = self.window.compile_shader(SHADERS.BASIC_VERTEX, SHADERS.BASIC_FRAGMENT)
        self.set_uniforms = _uniform_setter_placeholder 
    
    def render(self) -> None:
        self.update()
        # Render the fbo to the screen
        self.window.ctx.screen.use()
        self.fbo.color_attachments[0].use() # type: ignore (Pyright complains that it might not be a texture)
        self.set_uniforms(self) # Is actually a classless function
        self.vertex_array.render(moderngl.TRIANGLE_STRIP)

    @property
    def uniform_setter(self) -> Callable[[Callable], Callable]:
        def wrapper(function: Callable[[Self], None]) -> Callable:
            self.set_uniforms = function
            return function
        return wrapper

def _uniform_setter_placeholder(_: GLSurface) -> None:
    pass

class Camera(BaseObject):
    def __init__(self, window: Window, **kwargs) -> None:
        super().__init__()
        self.window = window
        self.viewport_size: IVectorLike = kwargs.get("viewport_size", (window.size[0], window.size[1]))
        self.display_size: IVectorLike = kwargs.get("display_size", (window.size[0], window.size[1]))
        self.viewport_position: IVectorLike = kwargs.get("viewport_position", (0, 0))
        self.display_position: IVectorLike = kwargs.get("display_position", (0, 0))
        if kwargs.get("surface", None):
            self.surface = kwargs["surface"]
        else:
            self.surface = GLSurface(window, self.viewport_size)
        self.render_queue: List[Sprite] = []
    
    def _object_update_method(self) -> None:
        pass

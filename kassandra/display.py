# External
from typing import List
from array import array
import pygame
import moderngl

# Internal
from .math_utils import Vector2
from .sprite import Sprite
from .base import Base
from .load import read_file

DEFAULT_VERT_SHADER = """
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
"""

DEFAULT_FRAG_SHADER = """
#version 330 core
uniform sampler2D tex;
//uniform float time;
in vec2 uvs;
out vec4 f_color;
void main() {
vec2 sample_pos = vec2(uvs.x, uvs.y);

if (texture(tex, sample_pos).a == 0.0) {
discard; // Discard black pixels
}

f_color = vec4(texture(tex, sample_pos).r, texture(tex, sample_pos).g, texture(tex, sample_pos).b, texture(tex, sample_pos).a);
} 
"""

class Display(Base):
    def __init__(self, size: tuple[int, int] = (500, 500), **kwargs):
        super().__init__()
        self.screen: pygame.Surface
        options: int = pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE
        if kwargs.get("fullscreen", False):
            options = options | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(size, options)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.delta_time: float = 1/60
        self.fps: int = kwargs.get("fps", 60)
        self.running: bool = False
        self.cameras = []
        self.next_camera_id: int = 0

        # OpenGL fun
        # NOTE: Each camera has its surface which is then rendered to the main display using moderngl
        self.ctx = moderngl.create_context()
        self.ctx.gc_mode = "context_gc"
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y) , texture coordinates (x, y)
            -1.0, 1.0, 0.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, 1.0, 1.0, 0.0,
            1.0, -1.0, 1.0, 1.0,
        ]))
        self.textures: dict[str, moderngl.Texture] = {}
        self.programs: dict[str, moderngl.Program] = {}
        self.vaos: dict[str, moderngl.VertexArray] = {}

    def update(self) -> None:
        self.delta_time = self.clock.tick(self.fps)
        for _ in pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            self.running = False
            return
        if self._update_callback:
            self._update_callback(self)
        self.ctx.clear(0, 0, 0)
        for i, camera in enumerate(self.cameras):
            camera.update(self.delta_time)
            self.surface_to_texture(str(i), camera.display_surface)
            self.textures[str(i)].use(i) 
            self.programs[camera.shader_program_name]["tex"] = i 
            self.vaos[camera.shader_program_name].render(mode=moderngl.TRIANGLE_STRIP)

        pygame.display.flip()
        self.textures = {}
        self.ctx.gc() 

    def mainloop(self) -> None:
        self.running = True
        while self.running:
            self.update()

    def add_camera(self, camera):
        if camera not in self.cameras:
            camera.initialise(self, self.next_camera_id)
            self.cameras.append(camera)
            self.next_camera_id += 1
    
    def remove_camera(self, camera):
        if camera in self.cameras:
            self.cameras.remove(camera)

    def compile_program(self, program_name, vert=DEFAULT_VERT_SHADER, frag=DEFAULT_FRAG_SHADER) -> None: # From DaFluffyPotato
        if vert != DEFAULT_VERT_SHADER:
            vert = read_file(vert)
        if frag != DEFAULT_FRAG_SHADER:
            frag = read_file(frag)
        program = self.ctx.program(vertex_shader=vert, fragment_shader=frag)
        self.programs[program_name] = program
        self.vaos[program_name] = self.ctx.vertex_array(program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')]) 

    def surface_to_texture(self, name: str, surface: pygame.Surface): # From DaFluffyPotato
        channels = 4
        if name not in self.textures:
            new_tex = self.ctx.texture(surface.get_size(), channels)
            new_tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
            new_tex.swizzle = 'BGRA'
            new_tex.write(surface.get_view("1"))
            self.textures[name] = new_tex
        

    def flush_cameras(self):
        self.cameras.clear()
        self.next_camera_id = 0

class Camera(Base):
    def __init__(self, size: tuple[int, int] = (500, 500), display_position: tuple[int, int] = (0, 0), world_position: tuple[int, int] = (0, 0), **kwargs):
        super().__init__()
        self.scale: float = kwargs.get("scale", 1)
        self._surface = pygame.Surface(size, pygame.SRCALPHA)
        self._display: Display
        self._size = Vector2.list_to_vec(size)
        self._display_position: Vector2 = Vector2.list_to_vec(display_position)
        self._world_position: Vector2 = Vector2.list_to_vec(world_position)
        self._surface.set_clip((0, 0, *self._size.list))
        self.sprites: List[Sprite] = []
        self.shader_program_name: str = kwargs.get("shader_program_name", "")
        self.id: int

    def initialise(self, display: Display, id: int) -> None:
        self._display = display
        self.id = id
        if not self.shader_program_name:
            self._display.compile_program("_display_camera_" + str(id))
            self.shader_program_name = "_display_camera_" + str(id)

    def update(self, dt: float):
        self._surface.fill((0, 0, 0, 0))
        if self._update_callback:
            self._update_callback(self)
        for sprite in self.sprites:
            sprite.update(self._surface, dt, self._world_position)
        # self._display.screen.blit(pygame.transform.scale(self._surface, [self._size.x * self.scale, self._size.y * self.scale]), self._display_position.list)

    @property
    def display_surface(self):
        new_surf = pygame.Surface(self._display.screen.get_size(), pygame.SRCALPHA, 32).convert_alpha()
        new_surf.blit(pygame.transform.scale(self._surface, (self._size * self.scale).list), self._display_position.list)
        return new_surf
    
    def add_sprite(self, sprite: Sprite) -> None:
        if sprite not in self.sprites:
            self.sprites.append(sprite)

    def remove_sprite(self, sprite: Sprite) -> None:
        if sprite in self.sprites:
            self.sprites.remove(sprite)

__all__ = ["GaussianBlurPass"]


import moderngl
import numpy as np

from ..custom_typing import FloatsT
from ..lazy.interface import (
    Lazy,
    LazyMode
)
from ..passes.render_pass import RenderPass
from ..rendering.config import ConfigSingleton
from ..rendering.context import ContextState
from ..rendering.framebuffer_batch import ColorFramebufferBatch
from ..rendering.gl_buffer import (
    UniformBlockBuffer,
    TexturePlaceholders
)
from ..rendering.vertex_array import VertexArray


class GaussianBlurPass(RenderPass):
    __slots__ = ()

    def __init__(
        self,
        sigma_width: float | None = None
    ) -> None:
        super().__init__()
        if sigma_width is not None:
            self._sigma_width_ = sigma_width

    @Lazy.variable(LazyMode.UNWRAPPED)
    @classmethod
    def _sigma_width_(cls) -> float:
        return 0.1

    @Lazy.property(LazyMode.UNWRAPPED)
    @classmethod
    def _convolution_core_(
        cls,
        sigma_width: float
    ) -> FloatsT:
        sigma = sigma_width * ConfigSingleton().size.pixel_per_unit
        n = int(np.ceil(3.0 * sigma))
        convolution_core = np.exp(-np.arange(n + 1) ** 2 / (2.0 * sigma ** 2))
        return convolution_core / (2.0 * convolution_core.sum() - convolution_core[0])

    @Lazy.property(LazyMode.OBJECT)
    @classmethod
    def _u_color_map_(cls) -> TexturePlaceholders:
        return TexturePlaceholders(
            field="sampler2D u_color_map"
        )

    @Lazy.property(LazyMode.OBJECT)
    @classmethod
    def _ub_gaussian_blur_(
        cls,
        convolution_core: FloatsT
    ) -> UniformBlockBuffer:
        return UniformBlockBuffer(
            name="ub_gaussian_blur",
            fields=[
                "vec2 u_uv_offset",
                "float u_convolution_core[CONVOLUTION_CORE_SIZE]"
            ],
            dynamic_array_lens={
                "CONVOLUTION_CORE_SIZE": len(convolution_core)
            },
            data={
                "u_uv_offset": 1.0 / np.array(ConfigSingleton().size.pixel_size),
                "u_convolution_core": convolution_core
            }
        )

    @Lazy.property(LazyMode.OBJECT)
    @classmethod
    def _horizontal_vertex_array_(
        cls,
        _u_color_map_: TexturePlaceholders,
        _ub_gaussian_blur_: UniformBlockBuffer
    ) -> VertexArray:
        return VertexArray(
            shader_filename="gaussian_blur",
            custom_macros=[
                f"#define blur_subroutine horizontal_dilate"
            ],
            texture_placeholders=[
                _u_color_map_
            ],
            uniform_blocks=[
                _ub_gaussian_blur_
            ]
        )

    @Lazy.property(LazyMode.OBJECT)
    @classmethod
    def _vertical_vertex_array_(
        cls,
        _u_color_map_: TexturePlaceholders,
        _ub_gaussian_blur_: UniformBlockBuffer
    ) -> VertexArray:
        return VertexArray(
            shader_filename="gaussian_blur",
            custom_macros=[
                f"#define blur_subroutine vertical_dilate"
            ],
            texture_placeholders=[
                _u_color_map_
            ],
            uniform_blocks=[
                _ub_gaussian_blur_
            ]
        )

    def _render(
        self,
        texture: moderngl.Texture,
        target_framebuffer: moderngl.Framebuffer
    ) -> None:
        with ColorFramebufferBatch() as batch:
            self._horizontal_vertex_array_.render(
                texture_array_dict={
                    "u_color_map": np.array(texture)
                },
                framebuffer=batch.framebuffer,
                context_state=ContextState(
                    enable_only=moderngl.NOTHING
                )
            )
            self._vertical_vertex_array_.render(
                texture_array_dict={
                    "u_color_map": np.array(batch.color_texture)
                },
                framebuffer=target_framebuffer,
                context_state=ContextState(
                    enable_only=moderngl.NOTHING
                )
            )

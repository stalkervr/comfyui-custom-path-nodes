class ContextPipeIn:
    """
    Pipe node: collects or overrides context data into a context_pipe list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "context_pipe": ("CONTEXT_PIPE",),
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "vae": ("VAE",),
                "latent": ("LATENT",),
                "image": ("IMAGE",),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "path_pipe": ("PATH_PIPE",),
            }
        }

    RETURN_TYPES = ("CONTEXT_PIPE",)
    RETURN_NAMES = ("context_pipe",)
    FUNCTION = "execute"
    CATEGORY = "Stalkervr/Context"

    def execute(
        self,
        context_pipe=None,
        model=None,
        clip=None,
        vae=None,
        latent=None,
        image=None,
        positive=None,
        negative=None,
        path_pipe=None,
    ):
        base = context_pipe if isinstance(context_pipe, list) else [None] * 8

        # Объединяем: приоритет у новых значений, затем из base, если новых нет
        out = [
            model if model is not None else base[0] if len(base) > 0 else None,
            clip if clip is not None else base[1] if len(base) > 1 else None,
            vae if vae is not None else base[2] if len(base) > 2 else None,
            latent if latent is not None else base[3] if len(base) > 3 else None,
            image if image is not None else base[4] if len(base) > 4 else None,
            positive if positive is not None else base[5] if len(base) > 5 else None,
            negative if negative is not None else base[6] if len(base) > 6 else None,
            path_pipe if path_pipe is not None else base[7] if len(base) > 7 else None,
        ]

        return (out,)
    
class ContextPipeOut:
    """
    Pipe node: expands context_pipe back to individual outputs.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "context_pipe": ("CONTEXT_PIPE",),
            }
        }

    RETURN_TYPES = ("CONTEXT_PIPE", "MODEL", "CLIP", "VAE", "LATENT", "IMAGE", "CONDITIONING", "CONDITIONING", "PATH_PIPE")
    RETURN_NAMES = ("context_pipe", "MODEL", "CLIP", "VAE", "LATENT", "IMAGE", "POSITIVE", "NEGATIVE", "path_pipe")
    FUNCTION = "execute"
    CATEGORY = "Stalkervr/Context"

    def execute(self, context_pipe):
        # Fill with None if missing
        ctx = context_pipe if isinstance(context_pipe, list) else [None] * 8
        while len(ctx) < 8:
            ctx.append(None)
        return (ctx, *ctx)
    
class ContextPipeReroute:
    """
    Pipe node: pass through the context_pipe without changes.
    Useful for rerouting or organizing graph flow.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "context_pipe": ("CONTEXT_PIPE",),
            }
        }

    RETURN_TYPES = ("CONTEXT_PIPE",)
    RETURN_NAMES = ("context_pipe",)
    FUNCTION = "execute"
    CATEGORY = "Stalkervr/Context"

    def execute(self, context_pipe):
        return (context_pipe,)

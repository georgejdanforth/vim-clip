import neovim


@neovim.plugin
class VimClip:

    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('Clip', sync=True)
    def clip(self, *args, **kwargs):
        self.nvim.command('echo "SUHHHHHHHH DUDE"')

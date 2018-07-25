import neovim
import os


@neovim.plugin
class VimClip:

    def __init__(self, nvim):
        self.nvim = nvim

    def mark(self, char):
        return self.nvim.current.buffer.mark(char)

    def get_visual_selection(self):

        s_line, s_col = self.mark('<')
        e_line, e_col = self.mark('>')

        if all(map(lambda n: not n, [s_line, s_col, e_line, e_col])):
            return

        lines = self.nvim.eval('getline({}, {})'.format(s_line, e_line))
        lines[0] = lines[0][s_col:]
        lines[-1] = lines[-1][:e_col + 1]

        return '\n'.join(lines)

    def copy_to_clipboard(self, text):
        os.system('echo "{}" | pbcopy'.format(text))

    @neovim.command('Clip', sync=True, range='')
    def clip(self, *args, **kwargs):
        visual_selection = self.get_visual_selection()
        if visual_selection is not None:
            self.copy_to_clipboard(visual_selection)

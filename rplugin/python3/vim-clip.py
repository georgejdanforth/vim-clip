"""
vim-clip

A neovim plugin for copying visual selections to your clipboard on OSX

Usage: In visual selection mode, simply execute the :Clip command, and your
selection will be copied to the system clipboard.
"""
import neovim
import subprocess


@neovim.plugin
class VimClip:

    def __init__(self, nvim):
        self.nvim = nvim

    def mark(self, char):
        """
        A shortcut for getting buffer coordinates using named characters.

        Args:
            char (string): The named character to get buffer coordinates for.
        Returns:
            coords (list): Coordinates of [line, column].
        """
        return self.nvim.current.buffer.mark(char)

    def get_visual_selection(self):
        """
        Get the current visual selection in string format.

        Args:
            None
        Returns:
            visual_selection (string): A string of the current visual selection.
        """
        # Get start and end [line, col] coordinates of selection.
        s_line, s_col = self.mark('<')
        e_line, e_col = self.mark('>')

        # If this isn't a visual selection, then all coords will be zero, in
        # which case we should just return None.
        if all(map(lambda n: not n, [s_line, s_col, e_line, e_col])):
            return

        # Grab the lines of this selection using the VimScript getline function.
        lines = self.nvim.eval('getline({}, {})'.format(s_line, e_line))

        # Slice lines to the given column numbers.
        lines[0] = lines[0][s_col:]
        lines[-1] = lines[-1][:e_col + 1]

        return '\n'.join(lines)

    def copy_to_clipboard(self, text):
        """
        Utility method for copying some text to the system clipboard

        Args:
            text (string): The text to be copied to the clipboard.
        Returns:
            None
        """
        try:
            subprocess.Popen(
                ['pbcopy'],
                stdin=subprocess.PIPE
            ).communicate(text.encode('utf-8'))
            self.nvim.command('echo "Copied to clipboard!"')
        except OSError:
            self.nvim.command('Failure: Check to make sure XCode is installed.')


    @neovim.command('Clip', sync=True, range='')
    def clip(self, *args, **kwargs):
        """
        Command definition for :Clip.
        """
        visual_selection = self.get_visual_selection()
        if visual_selection is not None:
            self.copy_to_clipboard(visual_selection)

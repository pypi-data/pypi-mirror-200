from js import document
from wwwpy.remote.components.ForwardTo import forward_to
from wwwpy.remote.widget import Widget


class PnSlider:

    def __init__(self):
        w = Widget(f'<input type="range">')
        self._proxy = w.container.firstChild
        document.body.append(w.container)


forward_to(PnSlider, '_proxy')

from js import document
from wwwpy.remote.components.ForwardTo import forward_to


class PnText:

    def __init__(self, text=None):
        div = document.createElement("div")
        self._proxy = div
        self.original_text = text
        if text is not None:
            div.innerHTML = text
        self._proxy = div
        document.body.append(div)

    def reset_text(self):
        self._proxy.innerHTML = self.original_text


forward_to(PnText, '_proxy')

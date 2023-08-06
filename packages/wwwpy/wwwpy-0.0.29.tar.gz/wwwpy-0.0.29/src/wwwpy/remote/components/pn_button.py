from js import document
from wwwpy.remote.components.ForwardTo import forward_to


class PnButton:

    def __init__(self, label: str, onclick=None):
        div = document.createElement("div")
        div.innerHTML = f"<button>{label}</button>"

        self._proxy = div.firstChild
        if onclick is not None:
            self.onclick = onclick
        document.body.append(div)


forward_to(PnButton, '_proxy')

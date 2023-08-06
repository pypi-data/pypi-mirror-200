from pathlib import Path
from typing import List


class Bootstrap:
    def __init__(self):
        self._remote_python: List[str] = []
        self.default_python = _wrap_in_try_except(
            'from js import document\n' +
            'document.body.innerHTML = "<h1>bootstrap done. No remote python specified</h1>"'
        )

    def add_python(self, code: str) -> 'Bootstrap':
        self._remote_python.append(_wrap_in_try_except(code))
        return self

    def get_javascript(self) -> str:
        rp = self._remote_python.copy()
        if len(rp) == 0:
            rp.append(self.default_python)
        with_indent = map(lambda l: '' + l, rp)
        parent = Path(__file__).parent
        # js = parent / 'bootstrap_pyodide.js'
        # js_content = js.read_text()
        python_log = 'print("first instruction run by pyodide")\n'
        return js_content.replace('# python replace marker', python_log + '\n'.join(with_indent))


def _wrap_in_try_except(code: str) -> str:
    import textwrap
    # language=python
    return f"""
try:
    pass
except Exception as ex:
    import traceback
    traceback.print_exc()            
""".replace('pass', '\n' + textwrap.indent(code, ' ' * 4))


js_content = """
if (typeof loadPyodide === 'undefined') {
    let script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/pyodide/v0.22.1/full/pyodide.js';
    script.onload = async () => {
        let pyodide = await loadPyodide();
        window.pyodide = pyodide;
        console.log('loading pyodide.runPythonAsync(...). See in the following lines for the code');
        console.log('-----------------------  START PYTHON CODE  -------------------------------');
        console.log(`# python replace marker`);
        console.log('-----------------------  END PYTHON CODE    -------------------------------');
        pyodide.runPythonAsync(`# python replace marker`);
    };
    document.body.append(script)
}
"""

"""A decentralized social web platform."""

import web

app = web.application(__name__, automount=True, autotemplate=True)


@app.control("")
class Home:
    """Your homepage."""

    def get(self):
        """Render your homepage."""
        return app.view.index()

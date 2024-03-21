import json
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import Optional

import pya

_path = Path(__file__).parent.parent
off = str(_path / "Koff.png")
live = str(_path / "Klive.png")
recv = str(_path / "Krecv.png")
poff = str(_path / "PortOff.png")
pon = str(_path / "PortOn.png")


polygon_dict = {}
dpolygon_dict = {}
shapes_shown = {}


class ServerInstance(pya.QTcpServer):
    """
    Implements a TCP server listening on port 8082.
    You can use it to instantly load a GDS or lyrdb (Results Database) file, programmatically, from Python.
    Just send a JSON-formatted command to localhost:8082.
    See README for more details.
    """

    def new_connection(self):
        """
        Handler for a new connection
        """

        try:
            self.action.icon = recv
            self.app.process_events()

            url = None

            # Get a new connection object
            connection = self.nextPendingConnection()

            # Read in the request
            data = None
            while (
                connection.isOpen()
                and connection.state() == pya.QTcpSocket.ConnectedState
            ):
                if connection.canReadLine():
                    line = connection.readLine()
                    data = json.loads(line)

                    # Interpret the data
                    gds_path = data["gds"]

                    # Store the current view
                    window = pya.Application.instance().main_window()
                    current_view = window.current_view()
                    previous_view = current_view.box() if current_view else None

                    send_data = {"version": "0.3.2"}

                    libs = data.get("libraries", {})
                    for lib_dict in libs:
                        lib = pya.Library()
                        lib.register(lib_dict["name"])
                        lib.layout().read(lib_dict["file"])

                    def load_existing_layout():
                        for i in range(window.views()):
                            view = window.view(i)
                            for j in range(view.cellviews()):
                                if view.active_cellview().filename() == gds_path:
                                    print(
                                        "File {} already openend".format(
                                            view.active_cellview().filename()
                                        )
                                    )
                                    window.current_view_index = i
                                    view.active_setview_index = j
                                    view.reload_layout(j)
                                    if view.active_cellview().cell is None:
                                        view.active_cellview().cell = (
                                            view.active_cellview()
                                            .layout()
                                            .top_cells()[0]
                                        )
                                    send_data["type"] = "reload"
                                    send_data["file"] = gds_path
                                    connection.write(
                                        json.dumps(send_data).encode("utf-8")
                                    )
                                    connection.flush()
                                    return view
                        else:
                            # Load the new layout
                            new_cview = window.load_layout(gds_path, 1)
                            new_view = new_cview.view()
                            new_view.max_hier()
                            window.current_view_index = window.index_of(new_view)
                            send_data["type"] = "open"
                            send_data["file"] = gds_path
                            connection.write(json.dumps(send_data).encode("utf-8"))
                            connection.flush()
                            return new_view

                    if window.views() > 0:
                        view = load_existing_layout()
                    else:
                        # Load the new layout
                        window.load_layout(gds_path, 1)

                        # Restore the previous position
                        view = window.current_view()
                        view.max_hier()
                        if previous_view and data["keep_position"] == True:
                            view.zoom_box(previous_view)

                        # Report progress
                        print("Loaded {}".format(gds_path))
                        send_data["type"] = "open"
                        send_data["file"] = gds_path
                        connection.write(json.dumps(send_data).encode("utf-8"))
                        connection.flush()
                    if "lyrdb" in data:
                        lyrdb_path = data["lyrdb"]
                        rdb = pya.ReportDatabase().load(lyrdb_path)
                        rdb_i = view.add_rdb(rdb)
                        view.show_rdb(rdb_i, view.active_cellview().cell_index)
                    if "l2n" in data:
                        l2n_path = data["l2n"]
                        l2n = pya.LayoutToNetlist()
                        l2n.read(l2n_path)
                        l2n_i = view.add_l2ndb(l2n)
                        view.show_l2ndb(l2n_i, view.active_cellview().cell_index)

                else:
                    connection.waitForReadyRead(100)

            # Disconnect
            connection.disconnectFromHost()
            signal = pya.qt_signal("disconnected()")
            slot = pya.qt_slot("deleteLater()")
            pya.QObject.connect(connection, signal, connection, slot)

            self.action.icon = live

        except Exception as ex:
            print("ERROR " + str(ex))

    def __init__(self, server, parent=None, action=None):
        """
        Initialize the server and put into listen mode (port is tcp/8082)
        """

        super(ServerInstance, self).__init__(parent)
        ha = pya.QHostAddress.new_special(pya.QHostAddress.LocalHost)
        self.listen(ha, 8082)
        ha6 = pya.QHostAddress("::1")
        self.listen(ha6, 8082)
        self.newConnection(self.new_connection)
        self.action = action
        self.server = server
        if self.action is not None and self.isListening():
            self.action.on_triggered = self.on_action_click
            print("klive 0.3.2 is running")
            self.action.icon = live
        else:
            print("klive didn't start correctly. Most likely port tcp/8082")
        self.app = app = pya.Application.instance()

    def on_action_click(self):
        self.server.reset(self.action)

    def close(self):
        super().close()

        print("klive 0.3.2 stopped")
        if self.action is not None and not self.action._destroyed():
            self.action.icon = off

    def __del__(self):
        self.close()
        super(ServerInstance, self).__del__()
def update_icon(action):
    acv = pya.CellView.active()
    idx = acv.index()
    cell = acv.cell
    if cell is not None:
        cidx = cell.cell_index()
    if idx in shapes_shown and cidx in shapes_shown[idx]:
        action.icon = pon
        action.icon_text = "Hide Ports"
        action.tool_tip = "Current Status: Shown"
    else:
        action.icon = poff
        action.icon_text = "Show Ports"
        action.tool_tip = "Current Status: Hidden"


@dataclass
class KliveServer:
    instance: Optional[ServerInstance] = None

    def reset(self, action):
        app = pya.Application.instance()
        mw = app.main_window()
        if self.instance is not None and self.instance.isListening():
            self.instance.close()
            app.process_events()
            sleep(0.1)
        self.instance = ServerInstance(self, parent=mw, action=action)



server = KliveServer()

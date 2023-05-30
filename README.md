# klive 0.2.2

klive is a small extension to KLayout that allows automatic loading for GDS files by sending a json with the gds path to klive.

klive starts a QTcpServer on port tcp/8082 binding to localhost. Projects like [kfactory](https://github.com/gdsfactory/kfactory) and
[gdsfactory](https://github.com/gdsfactory/gdsfactory) use this to make use of `show`.

## Installation

To install klive, open KLayout and open the package manger under `Tools -> Manage Packages`. In the package manager search for `klive`,
double-click it, check that it has a green check mark on it and press `Apply` on the bottom left. When asked to run the initial script press
`Yes` in order to start klive. Please make sure that you don't have `gdsfactory` installed anymore. This klive and the klive from the
gdsfactory KLayout package aren't compatible.

![type:video](_static/klive.webm "klive installation")

## Usage

klive will create an action button on the right of the Technology button in the toolbar. It will change the icon depending on the status.

It can be restarted by clicking on the klive symbool in the toolbar.

### Green

![Online](_static/Klive.png)

klive is up and running, waiting for incoming requests.

### Red

![Offline](_static/Koff.png)

When klive is initialized it will set the icon to ~~live~~ with a red bar. This indicates klive tried to start and crashed or started and crashed.
This can also happen if the port is occupied, e.g. by the `gdsfactory` package.

### Yellow

![Receiving](_static/Krecv.png)

klive is currently receiving a request to load a gds. If this is taking too long, there might be network problems or klive crashed.

# Troubleshooting klive

If klive stays in the red state, it can help to either open klayout from a terminal to receive stdout and stderror message or the same can be done
bey opening the macro editor under `Macros -> Macro Development` (or by pressing \[F5\]).

In the editor, go to the python section on the left and
look for the "Package klive" folder and open the `klive` script. Run it with the "Run scrip from current tab" (or \[Shift + F5\]).
Make sure to switch the Console on the bottom to python. If you don't get an error message or don't see a "klive 0.2.2 is running",
klive is not running. If you cannot debug your problem, please feel free to open an
issue on [GitHub](https://github.com/gdsfactory/klive/issues).

It can be useful to inspect the network connections to find whether klive is running. For example with netstat you can check whether klayout has a
port open that is listening

## Linux/MacOS

```
$ netstat -tupna | grep 8082
```
 
```
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 0.0.0.0:8082            0.0.0.0:*               LISTEN      543559/klayout 
```

## Windows

### CMD

```
netstat -na | find "8082"
```

### PowerShell

```
netstat -na | Select-String "8082"
```
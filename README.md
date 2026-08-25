# Proton Vessel Inspector

See what a running Proton game can access inside Steam's container.

It checks Discord sockets, GPU and controller devices, mounted paths, and the Proton environment. It only reads your own processes through `/proc`; it does not change Steam or game files.

## Run It

Start a Proton game in Steam, then run:

```bash
./proton-vessel-inspector
```

Use the arrow keys and Enter to pick a game, then choose `All`, `Checks`, `Paths`, `Environment`, or `Mount points`.

Reports stay open in the inspector. Use arrow keys to scroll, `b` or Escape to return to the menu, and `q` or Ctrl-C to exit.

To target a known Steam app ID instead:

```bash
./proton-vessel-inspector inspect --app 292000
```

`292000` is No More Room in Hell 2. Use `./proton-vessel-inspector list` to see running games and their app IDs.

Add `--json` before the command if you need a machine-readable report:

```bash
./proton-vessel-inspector --json inspect --app 292000
```

## Development

```bash
python3 -m unittest discover -s tests -v
```

# Elduin's Mod Lab

The website for the mods in [Elduin-Labs](https://github.com/Elduin-Labs) and the
[Modrinth profile](https://modrinth.com/user/ItsElduin) they get published to.

Live at **https://elduin-labs.github.io**

## Nothing on the page is typed in by hand

The mod cards and the wall of days are both generated from real sources, so the
site keeps itself up to date:

| File | Comes from | Rebuilt by |
| --- | --- | --- |
| `data/mods.json` | every public repo in the org, each mod's own `fabric.mod.json`, its GitHub releases, and its Modrinth page | `tools/build_mods.py`, run daily by Actions |
| `data/days.json` | the days the mod source files were actually written, on Elduin's Mac | `tools/build_days.py`, run by hand |
| `data/overrides.json` | hand-drawn 8×8 icon, category and tags per mod | edited by hand |

Publishing a new mod is enough to put it on the site. Within a day the workflow
picks up the new repo, gives it a guessed icon and a guessed category, and
commits the change. Give it a proper icon by adding an entry to
`data/overrides.json` — that is the only file anyone needs to edit by hand.

The page also asks Modrinth directly when it loads, so a mod that clears
Modrinth's review queue shows its download count without waiting for a rebuild.

### Rebuilding by hand

    python3 tools/build_mods.py     # needs GITHUB_TOKEN for the API rate limit
    python3 tools/build_days.py     # only works on the machine the mods live on

### Pushing the site straight after a release

A mod's release workflow can nudge the site instead of waiting for the daily run:

    gh api repos/Elduin-Labs/elduin-labs.github.io/dispatches -f event_type=mod-released

## The wall of days

One block per day, from the first day there is a record of to today. Green means
mod code was written that day; hover a block to see which mods.

The git history in the mod repos was squashed flat when they were tidied up, so
the honest record left is the modification date on each source file. That is what
`tools/build_days.py` reads — file dates only, never file contents. Days it has
no record of are grey.

Clicking a block still cycles it, and that edit is saved in the visitor's own
browser (`localStorage`) — it never changes the published data.

## The 3D bits

The hero is a pixel slime head that follows your pointer, rendered with WebGPU:
a ray-box intersection per pixel, with the face drawn procedurally on a 16×16
grid so the pupils can move independently of the head. The mod cards each show
their 8×8 icon extruded into a rotating slab.

None of it is required. If the browser has no WebGPU — older Safari, plenty of
Android — the 3D never starts and the page falls back to the flat pixel art it
was built on. Nobody sees an error.

## Editing

    git clone https://github.com/Elduin-Labs/elduin-labs.github.io.git
    cd elduin-labs.github.io
    python3 -m http.server 8000        # then open localhost:8000

A plain `open index.html` will not work: browsers refuse to read `data/*.json`
off the disk, and the page will say so instead of pretending to be empty.

## Deploying

GitHub Pages, straight from `main`. Every push republishes within a minute.

For a custom domain: put the bare domain in a `CNAME` file, then point four A
records at `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and
`185.199.111.153`, or a `www` CNAME at `elduin-labs.github.io`.

## License

MIT — see `LICENSE`.

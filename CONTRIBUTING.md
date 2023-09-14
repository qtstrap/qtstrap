# Mission & Mindset

Qtstrap has a broad range of features:

- quickly bootstrap qt applications (`qtstrap init`, project structure, `app_info.py`, `PortableSettings`)
- resolve common pitfalls (`ctrl-c handler`, saving window size/position)
- improve DX (context layouts, signal `Adapter`, `SettingsModel`)
- provide useful generic utilities (`SignalBlocker`, `Defer`, `[get|enable|disable]_children()`)
- new basic widgets (`LabelEdit`, `LinkLabel`, `HLine`, `VLine`)
- new advanced widgets (`CodeEditor`, `CodeLine`, `CommandPalette`, `LogMonitor`/db logging system)

At first glance, it seems to be a kitchen sink collection of stuff that one guy found useful when working on Qt applications. That's true, of course, but there's also a common thread connecting these things: developer ergonomics.

Everything that's in Qtstrap is here because it:

- provides some kind of ergonomic benefit
- fits with or otherwise does not impede the existing Qt ergonomics

The second point is more important than the first: any additions must either strictly conform to existing Qt APIs and expectations, OR be implemented as an alternate system/API. 
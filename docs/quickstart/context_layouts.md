# Context Layouts

This is how Qt expects you to build user interfaces with code:

```py
window = QWidget()
button1 = QPushButton("One")
button2 = QPushButton("Two")
button3 = QPushButton("Three")
button4 = QPushButton("Four")

layout = QVBoxLayout()
window.setLayout(layout)

hbox1 = QHBoxLayout()
layout.addLayout(hbox1)
hbox1.addWidget(button1)
hbox1.addWidget(button2)

hbox2 = QHBoxLayout()
layout.addLayout(hbox2)
hbox2.addWidget(button3)
hbox2.addWidget(button4)
```

This is only 4 buttons and it's already extremely ugly. Each nested layout needs a unique name. Every time you create a new layout you have to shift gears to add it to its parent. Don't even get me started on how pointless the distinction between `.addWidget()` and `.addLayout()` is. There isn't even a hint about what this layout will look like when it's built. We haven't even started messing with attributes like margins or alignments yet!

This is _definitely_ not pythonic.

Enter, the Context Layout:

```py
window = QWidget()
button1 = QPushButton("One")
button2 = QPushButton("Two")
button3 = QPushButton("Three")
button4 = QPushButton("Four")

with CVBoxLayout(window) as layout:
    with layout.hbox():
        layout.add(button1)
        layout.add(button2)
    with layout.hbox():
        layout.add(button3)
        layout.add(button4)
```

All of the backtracking and repetition is gone. The pointless effort of naming each layout is gone. The indentation helps show the structure of the layout.

The top level `CVBoxLayout` adds itself to its parent correctly and automatically. The `.add()` method can handle a layout or a widget or even a mixed list of both.
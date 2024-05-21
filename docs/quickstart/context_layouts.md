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

The `.add()` method also returns the item you give it, which allows us to remove even more duplication in some situations:

```py
# note that a with block does not create a new scope
with CHBoxLayout(QWidget()) as layout:
    button1 = layout.add(QPushButton("One"))
    button2 = layout.add(QPushButton("Two"))

# so these references are available after the with block closes
print(button1) 
```

Context layouts also support more advanced usages:

```py
with CVBoxLayout(QWidget()) as layout:
    # supports '+='
    layout += QLabel('Title') 
    # supports '+', which returns the added widget
    button1 = layout + QPushButton("One")
    # All add() methods also support lists and tuples of widgets
    button2, button3 = layout.add((QPushButton("Two"), QPushButton("Three")))
    button4, button5 = layout + [QPushButton("Four"), QPushButton("Five")]
```

# Advanced Layouts

Other Qt layout types are supported:

- Forms:
    ```py
    with CFormLayout(QWidget()) as layout:
        layout.add('label', QPushButton(''))
        layout += ['label', QPushButton('')]
        layout += {
            'label': QPushButton(''),
            'label': QPushButton(''),
        }
    ```
- Splitters:
    ```py
    with CSplitter(QWidget()) as split:
        # coming soon
        pass
    ```
- Scroll Areas:
    ```py
    with CScrollArea(QWidget()) as layout:
        # coming soon
        pass
    ```
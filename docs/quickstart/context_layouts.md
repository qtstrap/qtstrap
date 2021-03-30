# Context Layouts

This is how Qt expects you to build user interfaces with code:

```py
window = QWidget()
button1 = QPushButton("One")
button2 = QPushButton("Two")
button3 = QPushButton("Three")
button4 = QPushButton("Four")

layout = QVBoxLayout()

hbox1 = QHBoxLayout()
hbox1.addWidget(button1)
hbox1.addWidget(button2)

hbox2 = QHBoxLayout()
hbox2.addWidget(button3)
hbox2.addWidget(button4)

layout.addLayout(hbox1)
layout.addLayout(hbox2)

window.setLayout(layout)
```

It works, but it's extremely ugly.

```py
window = QWidget()
button1 = QPushButton("One")
button2 = QPushButton("Two")
button3 = QPushButton("Three")
button4 = QPushButton("Four")

with CVBoxLayout(window) as layout:
    with layout.hbox() as layout:
        layout.add(button1)
        layout.add(button2)
    with layout.hbox() as layout:
        layout.add(button3)
        layout.add(button4)
```
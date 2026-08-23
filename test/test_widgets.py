from qtstrap import *
import qtawesome as qta
import pytest


def test_state_button_icons_kwarg(qtbot):
    """StateButton should accept icons as a constructor kwarg."""
    icons = [qta.icon('fa5s.play'), qta.icon('fa5s.pause')]
    btn = StateButton(icons=icons)
    qtbot.addWidget(btn)

    assert btn.icons == icons
    assert btn._state == 0
    assert not btn.icon().isNull()


def test_state_button_no_icons(qtbot):
    """StateButton without icons should not crash on construction or click."""
    btn = StateButton()
    qtbot.addWidget(btn)

    assert btn.icons == []
    assert btn._state is None
    # clicking should be a no-op, not a crash
    qtbot.mouseClick(btn, QtCore.Qt.LeftButton)


def test_state_button_cycles(qtbot):
    """StateButton should cycle through states on click."""
    icons = [qta.icon('fa5s.play'), qta.icon('fa5s.pause'), qta.icon('fa5s.stop')]
    btn = StateButton(icons=icons)
    qtbot.addWidget(btn)

    assert btn.state == 0
    qtbot.mouseClick(btn, QtCore.Qt.LeftButton)
    assert btn.state == 1
    qtbot.mouseClick(btn, QtCore.Qt.LeftButton)
    assert btn.state == 2
    qtbot.mouseClick(btn, QtCore.Qt.LeftButton)
    assert btn.state == 0  # wraps around


def test_state_button_state_changed_signal(qtbot):
    """state_changed signal should fire with the new state index."""
    btn = StateButton(icons=[qta.icon('fa5s.play'), qta.icon('fa5s.pause')])
    qtbot.addWidget(btn)

    received = []
    btn.state_changed.connect(lambda s: received.append(s))

    qtbot.mouseClick(btn, QtCore.Qt.LeftButton)
    assert received == [1]


def test_link_label_text_and_link(qtbot):
    """LinkLabel(text=display, link=url) — text is display text, link is URL."""
    label = LinkLabel(text='Click here', link='https://example.com')
    qtbot.addWidget(label)

    # the rendered HTML should have the URL in the href and display text as content
    html = label.text()
    assert 'href="https://example.com"' in html
    assert 'Click here' in html


def test_link_label_default_empty(qtbot):
    """LinkLabel with no args should not crash."""
    label = LinkLabel()
    qtbot.addWidget(label)
    # no link set, should render empty
    assert 'href=""' in label.text()


def test_link_label_set_text(qtbot):
    """setText should update the display text, not the URL."""
    label = LinkLabel(text='Original', link='https://example.com')
    qtbot.addWidget(label)

    label.setText('Changed')
    html = label.text()
    assert 'Changed' in html
    assert 'href="https://example.com"' in html
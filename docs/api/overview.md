<!-- markdownlint-disable -->

# API Overview

## Modules

- [`extras`](./extras.md#module-extras)
- [`extras.code_editor`](./extras.code_editor.md#module-extrascode_editor)
- [`extras.code_editor.code_editor`](./extras.code_editor.code_editor.md#module-extrascode_editorcode_editor)
- [`extras.code_editor.code_line`](./extras.code_editor.code_line.md#module-extrascode_editorcode_line)
- [`extras.code_editor.highlighters`](./extras.code_editor.highlighters.md#module-extrascode_editorhighlighters)
- [`extras.code_editor.highlighters.python`](./extras.code_editor.highlighters.python.md#module-extrascode_editorhighlighterspython)
- [`extras.command_palette`](./extras.command_palette.md#module-extrascommand_palette)
- [`extras.command_palette.command_palette`](./extras.command_palette.command_palette.md#module-extrascommand_palettecommand_palette)
- [`extras.log_monitor`](./extras.log_monitor.md#module-extraslog_monitor)
- [`extras.log_monitor.log_database_handler`](./extras.log_monitor.log_database_handler.md#module-extraslog_monitorlog_database_handler)
- [`extras.log_monitor.log_filter_controls`](./extras.log_monitor.log_filter_controls.md#module-extraslog_monitorlog_filter_controls)
- [`extras.log_monitor.log_profile`](./extras.log_monitor.log_profile.md#module-extraslog_monitorlog_profile)
- [`extras.log_monitor.log_table_view`](./extras.log_monitor.log_table_view.md#module-extraslog_monitorlog_table_view)
- [`extras.log_monitor.log_widget`](./extras.log_monitor.log_widget.md#module-extraslog_monitorlog_widget)
- [`extras.style`](./extras.style.md#module-extrasstyle)
- [`extras.style.colors`](./extras.style.colors.md#module-extrasstylecolors)
- [`extras.style.dark_palette`](./extras.style.dark_palette.md#module-extrasstyledark_palette)
- [`options`](./options.md#module-options)
- [`settings`](./settings.md#module-settings)
- [`utils`](./utils.md#module-utils)
- [`utils.adapter`](./utils.adapter.md#module-utilsadapter)
- [`utils.decorators`](./utils.decorators.md#module-utilsdecorators)
- [`utils.defer`](./utils.defer.md#module-utilsdefer)
- [`utils.signals`](./utils.signals.md#module-utilssignals)
- [`utils.singleton`](./utils.singleton.md#module-utilssingleton)
- [`utils.timestamp`](./utils.timestamp.md#module-utilstimestamp)
- [`utils.utils`](./utils.utils.md#module-utilsutils)
- [`widgets`](./widgets.md#module-widgets)
- [`widgets.buttons`](./widgets.buttons.md#module-widgetsbuttons)
- [`widgets.labeledit`](./widgets.labeledit.md#module-widgetslabeledit)
- [`widgets.layouts`](./widgets.layouts.md#module-widgetslayouts)
- [`widgets.line_widgets`](./widgets.line_widgets.md#module-widgetsline_widgets)
- [`widgets.link_label`](./widgets.link_label.md#module-widgetslink_label)
- [`widgets.persistent_tab_widget`](./widgets.persistent_tab_widget.md#module-widgetspersistent_tab_widget)
- [`widgets.persistent_widgets`](./widgets.persistent_widgets.md#module-widgetspersistent_widgets)

## Classes

- [`code_editor.CodeEditor`](./extras.code_editor.code_editor.md#class-codeeditor)
- [`code_line.CodeLine`](./extras.code_editor.code_line.md#class-codeline)
- [`python.PythonHighlighter`](./extras.code_editor.highlighters.python.md#class-pythonhighlighter)
- [`command_palette.Command`](./extras.command_palette.command_palette.md#class-command)
- [`command_palette.CommandCompleter`](./extras.command_palette.command_palette.md#class-commandcompleter)
- [`command_palette.CommandModel`](./extras.command_palette.command_palette.md#class-commandmodel)
- [`command_palette.CommandRegistry`](./extras.command_palette.command_palette.md#class-commandregistry)
- [`command_palette.PopupDelegate`](./extras.command_palette.command_palette.md#class-popupdelegate)
- [`log_database_handler.DatabaseHandler`](./extras.log_monitor.log_database_handler.md#class-databasehandler)
- [`log_filter_controls.FilterControls`](./extras.log_monitor.log_filter_controls.md#class-filtercontrols)
- [`log_filter_controls.LoggerDelegate`](./extras.log_monitor.log_filter_controls.md#class-loggerdelegate)
- [`log_filter_controls.LoggerTreeWidget`](./extras.log_monitor.log_filter_controls.md#class-loggertreewidget)
- [`log_filter_controls.LoggerTreeWidgetItem`](./extras.log_monitor.log_filter_controls.md#class-loggertreewidgetitem)
- [`log_filter_controls.ProfileSelector`](./extras.log_monitor.log_filter_controls.md#class-profileselector)
- [`log_profile.Column`](./extras.log_monitor.log_profile.md#class-column)
- [`log_profile.LogProfile`](./extras.log_monitor.log_profile.md#class-logprofile)
- [`log_table_view.LogDbModel`](./extras.log_monitor.log_table_view.md#class-logdbmodel)
- [`log_table_view.LogTableView`](./extras.log_monitor.log_table_view.md#class-logtableview)
- [`log_widget.LogMonitorDockWidget`](./extras.log_monitor.log_widget.md#class-logmonitordockwidget)
- [`log_widget.LogMonitorDropdown`](./extras.log_monitor.log_widget.md#class-logmonitordropdown)
- [`log_widget.LogMonitorWidget`](./extras.log_monitor.log_widget.md#class-logmonitorwidget)
- [`colors.colors`](./extras.style.colors.md#class-colors)
- [`colors.qcolors`](./extras.style.colors.md#class-qcolors)
- [`options.OPTIONS`](./options.md#class-options)
- [`adapter.Adapter`](./utils.adapter.md#class-adapter)
- [`defer.Defer`](./utils.defer.md#class-defer): A context manager that emulates the defer keyword from other languages.
- [`signals.SignalBlocker`](./utils.signals.md#class-signalblocker): A context manager that blocks the signals of the provided widget.
- [`timestamp.TimeStamp`](./utils.timestamp.md#class-timestamp)
- [`buttons.ConfirmToggleButton`](./widgets.buttons.md#class-confirmtogglebutton)
- [`buttons.IconToggleButton`](./widgets.buttons.md#class-icontogglebutton)
- [`buttons.StateButton`](./widgets.buttons.md#class-statebutton)
- [`labeledit.LabelEdit`](./widgets.labeledit.md#class-labeledit)
- [`layouts.CGridLayout`](./widgets.layouts.md#class-cgridlayout)
- [`layouts.CHBoxLayout`](./widgets.layouts.md#class-chboxlayout)
- [`layouts.CScrollArea`](./widgets.layouts.md#class-cscrollarea)
- [`layouts.CSplitter`](./widgets.layouts.md#class-csplitter)
- [`layouts.CVBoxLayout`](./widgets.layouts.md#class-cvboxlayout)
- [`layouts.ContextLayout`](./widgets.layouts.md#class-contextlayout)
- [`layouts.PersistentCScrollArea`](./widgets.layouts.md#class-persistentcscrollarea)
- [`layouts.PersistentCSplitter`](./widgets.layouts.md#class-persistentcsplitter)
- [`line_widgets.HLine`](./widgets.line_widgets.md#class-hline)
- [`line_widgets.VLine`](./widgets.line_widgets.md#class-vline)
- [`link_label.LinkLabel`](./widgets.link_label.md#class-linklabel)
- [`persistent_tab_widget.PersistentTabWidget`](./widgets.persistent_tab_widget.md#class-persistenttabwidget)
- [`persistent_widgets.PersistentCheckBox`](./widgets.persistent_widgets.md#class-persistentcheckbox)
- [`persistent_widgets.PersistentCheckableAction`](./widgets.persistent_widgets.md#class-persistentcheckableaction)
- [`persistent_widgets.PersistentComboBox`](./widgets.persistent_widgets.md#class-persistentcombobox)
- [`persistent_widgets.PersistentLineEdit`](./widgets.persistent_widgets.md#class-persistentlineedit)
- [`persistent_widgets.PersistentListWidget`](./widgets.persistent_widgets.md#class-persistentlistwidget)
- [`persistent_widgets.PersistentTextEdit`](./widgets.persistent_widgets.md#class-persistenttextedit)
- [`persistent_widgets.PersistentTreeWidget`](./widgets.persistent_widgets.md#class-persistenttreewidget)

## Functions

- [`python.format`](./extras.code_editor.highlighters.python.md#function-format): Return a QTextCharFormat with the given attributes.
- [`command_palette.CommandPalette`](./extras.command_palette.command_palette.md#function-commandpalette)
- [`log_monitor.install`](./extras.log_monitor.md#function-install)
- [`settings.uncache`](./settings.md#function-uncache): Remove package modules from cache except excluded ones.
- [`decorators.trace`](./utils.decorators.md#function-trace)
- [`singleton.singleton`](./utils.singleton.md#function-singleton):     
- [`timestamp.time_since`](./utils.timestamp.md#function-time_since)
- [`utils.disable_children`](./utils.utils.md#function-disable_children): Recursively walk the provided thing and disable all of its widget children.
- [`utils.enable_children`](./utils.utils.md#function-enable_children): Recursively walk the provided thing and enable all of its widget children.
- [`utils.get_children`](./utils.utils.md#function-get_children): Recursively visit all the children of the specified object and collect them in a list.
- [`utils.print_children`](./utils.utils.md#function-print_children): Recursively visit all the children of the specified object and print them.
- [`utils.set_font_options`](./utils.utils.md#function-set_font_options): Set the QFont options of the specified object.


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

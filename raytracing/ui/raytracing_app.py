import sys

try:
    import tkinter as tk
    from tkinter import filedialog, ttk, StringVar
    from mytk import *
    from mytk.base import BaseNotification
    from mytk.canvasview import *
    from mytk.dataviews import *
    from mytk.entries import CellEntry
    from mytk.vectors import Point, PointDefault, DynamicBasis
    from mytk.labels import Label
    from mytk.notificationcenter import NotificationCenter
except ImportError as e:
    print(f"Error: {e}", file=sys.stderr)
    print("\nThe graphical interface requires 'mytk' and 'tkinter'.", file=sys.stderr)
    print("Install mytk with: pip install mytk", file=sys.stderr)
    print("On Linux, you may also need: sudo apt install python3-tk (Debian/Ubuntu)", file=sys.stderr)
    print("                          or: sudo dnf install python3-tkinter (Fedora)", file=sys.stderr)
    sys.exit(1)

import ast
import inspect
from math import sqrt, copysign
from numpy import linspace, isfinite
from raytracing import *
# Vendor catalogs — pull every catalog class into the module namespace
# so the table can instantiate parts by name (e.g. "AC254_050_A()" with
# no args) via globals() lookup in instantiate_element.
from raytracing.thorlabs import *
from raytracing.eo import *
from raytracing.olympus import *
import colorsys
import pyperclip
from contextlib import suppress


class Polygon(CanvasElement):
    """A filled polygon. mytk doesn't ship one, so we define a small
    wrapper that follows the same pattern as mytk's Line / Oval classes
    but calls Tkinter's create_polygon under the hood. Used for lens
    bodies bounded by spherical (arc) surfaces and for objective
    silhouettes.
    """

    def __init__(self, points=None, basis=None, **kwargs):
        super().__init__(basis=basis, **kwargs)
        self.points = points

    def create(self, canvas, position=None):
        if position is None:
            position = Point(0, 0)
        self.canvas = canvas
        shifted = [(position + p).standard_tuple() for p in self.points]
        self.id = canvas.widget.create_polygon(shifted, **self._element_kwargs)
        return self.id


def _collect_element_class_names():
    """All class names the user can type in the Element column: the
    primitives shipped by raytracing plus every catalog part from
    thorlabs, eo, and olympus. Used to populate the autocomplete popup.
    """
    from raytracing import thorlabs, eo, olympus
    names = {
        "Lens", "ThickLens", "Aperture", "DielectricSlab",
        "DielectricInterface", "Space", "Matrix",
        "AchromatDoubletLens", "Objective",
    }
    for mod in (thorlabs, eo, olympus):
        for n, obj in inspect.getmembers(mod, inspect.isclass):
            if obj.__module__ == mod.__name__:
                names.add(n)
    return sorted(names)


ELEMENT_CLASS_NAMES = _collect_element_class_names()


class AutocompleteCellEntry(CellEntry):
    """CellEntry with a filter-as-you-type popup listbox.

    Behaviour:
      - Typing filters the listbox to prefix (and then substring) matches.
      - No item is pre-selected — Enter on free-form text commits what
        the user typed verbatim (so "Lens(f=50)" still works).
      - Pressing Down moves into the listbox; Up/Down navigate from
        there; Enter then commits the highlighted item instead.
      - Clicking an item in the listbox commits it immediately.
      - Escape dismisses the popup and the edit without changes.
    """

    def __init__(self, *args, choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices or []
        self.popup = None
        self.listbox = None
        self._user_activated_listbox = False

    def create_widget(self, master):
        super().create_widget(master)
        self.widget.bind("<KeyRelease>", self._on_key_release)
        self.widget.bind("<Down>", self._on_down_arrow)
        self.widget.bind("<Up>", self._on_up_arrow)
        self.widget.bind("<Escape>", self._on_escape)
        # Override the inherited <Return> binding so Enter consults the
        # listbox selection when the user has navigated into it.
        self.widget.bind("<Return>", self._on_return)
        self.widget.after_idle(self._open_popup)

    def _open_popup(self):
        if self.popup is not None or self.widget is None:
            return
        # Force Tk to finish laying the entry widget out so winfo_rootx /
        # winfo_rooty return its actual screen coordinates instead of 0.
        self.widget.update_idletasks()
        self.popup = tk.Toplevel(self.widget)
        self.popup.wm_overrideredirect(True)  # borderless, no title bar
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.popup.wm_geometry(f"+{x}+{y}")
        self.listbox = tk.Listbox(
            self.popup, height=12, width=28, activestyle="dotbox"
        )
        self.listbox.pack()
        self.listbox.bind("<Button-1>", self._on_listbox_click)
        self._refresh_listbox()

    def _close_popup(self):
        if self.popup is not None:
            self.popup.destroy()
        self.popup = None
        self.listbox = None

    def _refresh_listbox(self):
        if self.listbox is None:
            return
        typed = self.value_variable.get().lower()
        prefix = [c for c in self.choices if c.lower().startswith(typed)]
        substr = [c for c in self.choices
                  if typed and typed in c.lower() and c not in prefix]
        matches = prefix + substr
        self.listbox.delete(0, "end")
        for c in matches:
            self.listbox.insert("end", c)
        # Reset the "user navigated into listbox" flag every time the
        # text changes — typed text always wins on Enter unless the user
        # explicitly pressed Down after typing.
        self._user_activated_listbox = False

    def _on_key_release(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return
        self._refresh_listbox()

    def _on_down_arrow(self, event):
        if self.listbox is None or self.listbox.size() == 0:
            return "break"
        cur = self.listbox.curselection()
        idx = (cur[0] + 1) if cur else 0
        idx = min(idx, self.listbox.size() - 1)
        self.listbox.select_clear(0, "end")
        self.listbox.select_set(idx)
        self.listbox.see(idx)
        self._user_activated_listbox = True
        return "break"

    def _on_up_arrow(self, event):
        if self.listbox is None or self.listbox.size() == 0:
            return "break"
        cur = self.listbox.curselection()
        idx = (cur[0] - 1) if cur else 0
        idx = max(idx, 0)
        self.listbox.select_clear(0, "end")
        self.listbox.select_set(idx)
        self.listbox.see(idx)
        self._user_activated_listbox = True
        return "break"

    def _on_listbox_click(self, event):
        idx = self.listbox.nearest(event.y)
        if idx < 0:
            return "break"
        self.value_variable.set(self.listbox.get(idx))
        self._commit()
        return "break"

    def _on_return(self, event):
        if self._user_activated_listbox and self.listbox is not None:
            cur = self.listbox.curselection()
            if cur:
                self.value_variable.set(self.listbox.get(cur[0]))
        self._commit()
        return "break"

    def _on_escape(self, event):
        self._close_popup()
        self.widget.destroy()
        return "break"

    def _commit(self):
        self._close_popup()
        # Defer to CellEntry's existing commit path (writes back to the
        # data source, then destroys this widget via FocusOut).
        super().event_return_callback(None)

    def event_focusout_callback(self, event):
        self._close_popup()
        return super().event_focusout_callback(event)


class RaytracingApp(App):
    def __init__(self):
        App.__init__(self, name="Raytracing Application")
        self.window.widget.title("Raytracing")

        self.number_of_heights = 5
        self.max_height = 5
        self.number_of_angles = 5
        self.max_fan_angle = 0.1
        self.dont_show_blocked_rays = True
        self.show_raytraces = True
        self.show_apertures = True
        self.show_labels = True
        self.show_principal_rays = 1
        self.show_conjugates = True
        self.show_intermediate_conjugates = False
        self.maximum_x = 60
        self.initialization_completed = False
        self.path_has_field_stop = True

        self.create_window_widgets()
        self.refresh()

    def create_window_widgets(self):
        self._build_element_table()
        self._build_results_table()
        self._build_controls_panel()
        self._build_canvas()
        self._wire_bindings()
        self._register_observers()
        self.initialization_completed = True

    def _build_element_table(self):
        # Element table on the right side of the window, with its three
        # action buttons (Add / Delete / Copy script) underneath.
        self.table_group = View(width=300, height=300)
        self.table_group.grid_into(
            self.window, row=0, column=1, pady=5, padx=5, sticky="nsew"
        )
        self.table_group.column_resize_weight(index=0, weight=1)

        self.button_group = View(width=300, height=200)
        self.button_group.grid_into(
            self.table_group, row=1, column=0, pady=5, padx=5, sticky="nsew"
        )

        self.add_lens_button = Button(
            "Add element", user_event_callback=self.click_table_buttons
        )
        self.add_lens_button.grid_into(
            self.button_group, row=0, column=0, pady=5, padx=5
        )

        self.delete_button = Button(
            "Delete element", user_event_callback=self.click_table_buttons
        )
        self.delete_button.grid_into(self.button_group, row=0, column=2, pady=5, padx=5)

        self.copy_code_button = Button(
            "Copy script", user_event_callback=self.click_copy_buttons
        )
        self.copy_code_button.grid_into(
            self.button_group, row=0, column=3, pady=5, padx=5
        )

        self.tableview = TableView(
            columns_labels={
                "element": "Element",
                "arguments": "Properties",
                "position": "Position [mm]",
            }
        )
        self.tableview.column_formats["position"] = {
            "format_string": "{0:g}",
            "multiplier": 1,
            "anchor": "",
        }
        self.tableview.data_source.update_field_properties("position", {"type": float})

        self.tableview.grid_into(
            self.table_group, column=0, row=0, columnspan=2,
            pady=5, padx=5, sticky="nsew",
        )
        self.tableview.displaycolumns = ["position", "element", "arguments"]
        widths = {"position": 5, "element": 5, "arguments": 150}
        for column in self.tableview.displaycolumns:
            self.tableview.widget.column(column, width=widths[column], anchor=W)

        self.tableview.data_source.append_record(
            {"element": "Lens", "arguments": "f=100", "position": 200}
        )
        self.tableview.delegate = self
        self._install_element_autocomplete()

    def _install_element_autocomplete(self):
        # Replace TableView.focus_edit_cell with a wrapper that pops up
        # an autocomplete listbox for the "element" column and falls
        # back to the default Entry for every other column. The other
        # columns (Properties, Position) are still plain text.
        original_focus_edit_cell = self.tableview.focus_edit_cell
        tableview = self.tableview

        def focus_edit_cell(item_id, column_name):
            if column_name != "element":
                original_focus_edit_cell(item_id, column_name)
                return
            bbox = tableview.widget.bbox(item_id, column=column_name)
            entry = AutocompleteCellEntry(
                tableview=tableview,
                item_id=item_id,
                column_name=column_name,
                choices=ELEMENT_CLASS_NAMES,
            )
            entry.place_into(
                parent=tableview,
                x=bbox[0] - 2, y=bbox[1] - 2,
                width=bbox[2] + 4, height=bbox[3] + 4,
            )
            entry.widget.focus()

        self.tableview.focus_edit_cell = focus_edit_cell

    def _build_results_table(self):
        # Imaging-path results table in the rightmost column.
        self.results_tableview = TableView(
            columns_labels={"property": "Property", "value": "Value"}
        )
        self.results_tableview.grid_into(
            self.window, column=2, row=0, pady=5, padx=5, sticky="nsew"
        )
        self.results_tableview.all_elements_are_editable = False
        self.results_tableview.widget.column("property", width=250)
        self.results_tableview.widget.column("value", width=150)

    def _build_controls_panel(self):
        # Display controls on the left: an "Input ray" sub-box with the
        # principal/custom radio + ray-fan parameters, and four checkboxes
        # for what to draw on the canvas.
        self.controls = Box(label="Display", width=200)
        self.controls.grid_into(
            self.window, column=0, row=0, columnspan=1, pady=5, padx=5, sticky="nsew"
        )

        self.control_input_rays = Box(label="Input ray", width=200)
        self.control_input_rays.grid_into(
            self.controls, column=0, row=0, columnspan=1, pady=5, padx=5, sticky="nsew"
        )

        # radio_custom is gridded but never referenced again; only
        # radio_principal needs to live on self for the bindings step.
        self.radio_principal, radio_custom = RadioButton.linked_group(
            labels_values={"Principal rays": 1, "Custom rays": 0}
        )
        radio_custom.grid_into(
            self.control_input_rays, column=0, row=0, columnspan=1,
            pady=5, padx=5, sticky="nsew",
        )
        self.radio_principal.grid_into(
            self.control_input_rays, column=0, row=4, columnspan=1,
            pady=5, padx=5, sticky="nsew",
        )
        self.radio_principal.bind_properties("is_enabled", self, "path_has_field_stop")

        self.number_heights_label = Label(text="# ray heights:")
        self.number_heights_label.grid_into(
            self.control_input_rays, column=0, row=1, pady=5, padx=5, sticky="e"
        )
        self.number_heights_entry = IntEntry(minimum=1, maximum=100, width=3)
        self.number_heights_entry.grid_into(
            self.control_input_rays, column=1, row=1, pady=5, padx=5, sticky="w"
        )

        self.number_angles_label = Label(text="# ray angles:")
        self.number_angles_label.grid_into(
            self.control_input_rays, column=0, row=2, pady=5, padx=5, sticky="e"
        )
        self.number_angles_entry = IntEntry(minimum=1, maximum=100, width=3)
        self.number_angles_entry.grid_into(
            self.control_input_rays, column=1, row=2, pady=5, padx=5, sticky="w"
        )

        self.max_heights_label = Label(text="Max height:")
        self.max_heights_label.grid_into(
            self.control_input_rays, column=3, row=1, pady=5, padx=5, sticky="w"
        )
        self.max_heights_entry = Entry(character_width=3)
        self.max_heights_entry.grid_into(
            self.control_input_rays, column=4, row=1, pady=5, padx=5, sticky="w"
        )

        self.fan_angles_label = Label(text="Max angle:")
        self.fan_angles_label.grid_into(
            self.control_input_rays, column=3, row=2, pady=5, padx=5, sticky="w"
        )
        self.fan_angles_entry = Entry(character_width=3)
        self.fan_angles_entry.grid_into(
            self.control_input_rays, column=4, row=2, pady=5, padx=5, sticky="w"
        )

        self.show_conjugates_checkbox = Checkbox(label="Show object/image planes")
        self.show_conjugates_checkbox.grid_into(
            self.controls, column=0, row=1, columnspan=4, pady=5, padx=5, sticky="w"
        )

        self.apertures_checkbox = Checkbox(
            label="Show Aperture stop (AS) and field stop (FS)"
        )
        self.apertures_checkbox.grid_into(
            self.controls, column=0, row=3, columnspan=4, pady=5, padx=5, sticky="w"
        )

        self.show_labels_checkbox = Checkbox(label="Show object labels")
        self.show_labels_checkbox.grid_into(
            self.controls, column=0, row=4, columnspan=4, pady=5, padx=5, sticky="w"
        )

        self.blocked_rays_checkbox = Checkbox(label="Do not show blocked rays")
        self.blocked_rays_checkbox.grid_into(
            self.controls, column=0, row=5, columnspan=4, pady=5, padx=5, sticky="w"
        )

    def _build_canvas(self):
        # Drawing surface that fills the bottom row of the window, plus
        # the coordinate system element rays and optics are rendered on.
        self.canvas = CanvasView(width=1000, height=400, background="white")
        self.canvas.grid_into(
            self.window, column=0, row=1, columnspan=3, pady=5, padx=5, sticky="nsew"
        )

        NotificationCenter().add_observer(
            self, self.canvas_did_resize, BaseNotification.did_resize
        )

        self.window.column_resize_weight(index=1, weight=1)
        self.window.row_resize_weight(index=1, weight=1)

        self.coords_origin = Point(
            0.05, 0.5, basis=DynamicBasis(self.canvas, "relative_basis")
        )

        size = (
            Vector(0.85, 0, basis=DynamicBasis(self.canvas, "relative_basis")),
            Vector(0, -0.6, basis=DynamicBasis(self.canvas, "relative_basis")),
        )
        self.coords = XYCoordinateSystemElement(
            size=size, axes_limits=((0, 400), (-25, 25)), width=2
        )
        self.coords.nx_major = 20
        self.coords.ny_major = 10

        self.canvas.place(
            self.coords, position=Point(0.05, 0.5, basis=self.canvas.relative_basis)
        )

    def _wire_bindings(self):
        # Two-way property bindings: `self.<attr>` <-> widget value.
        self.bind_properties("number_of_heights", self.number_heights_entry, "value_variable")
        self.bind_properties("number_of_angles", self.number_angles_entry, "value_variable")
        self.bind_properties("dont_show_blocked_rays", self.blocked_rays_checkbox, "value_variable")
        self.bind_properties("show_apertures", self.apertures_checkbox, "value_variable")
        self.bind_properties("show_labels", self.show_labels_checkbox, "value_variable")
        self.bind_properties("show_principal_rays", self.radio_principal, "value_variable")
        self.bind_properties("show_conjugates", self.show_conjugates_checkbox, "value_variable")
        self.bind_properties("max_height", self.max_heights_entry, "value_variable")
        self.bind_properties("max_fan_angle", self.fan_angles_entry, "value_variable")

        # When "Principal rays" is selected, the custom-ray inputs gray out.
        for widget in (
            self.number_heights_entry,
            self.number_angles_entry,
            self.max_heights_entry,
            self.fan_angles_entry,
            self.blocked_rays_checkbox,
        ):
            widget.bind_properties("is_disabled", self, "show_principal_rays")

    def _register_observers(self):
        # Any change to one of these triggers a canvas refresh.
        for prop in (
            "number_of_heights",
            "number_of_angles",
            "dont_show_blocked_rays",
            "show_apertures",
            "show_principal_rays",
            "show_labels",
            "show_conjugates",
        ):
            self.add_observer(self, prop)

    def canvas_did_resize(self, notification):
        self.refresh()

    def observed_property_changed(
        self, observed_object, observed_property_name, new_value, context
    ):
        super().observed_property_changed(
            observed_object, observed_property_name, new_value, context
        )
        if context == "refresh_graph":
            self.canvas.widget.delete(self.coords.id)
            self.coords.axes_limits = ((0, float(self.maximum_x)), (-50, 50))

        self.refresh()

    def source_data_changed(self, tableview):
        self.refresh()

    def validate_source_data(self, tableview):
        try:
            user_provided_path = self.get_path_from_ui(
                without_apertures=True, max_position=None
            )
            return False
        except Exception as err:
            # Only the missing-required-args ValueError from
            # get_path_from_ui carries err.details with the full
            # signature we need to write "<param>=?" hints. Anything
            # else (e.g. ast.parse SyntaxError triggered by the "?"
            # placeholders still sitting in a cell the user hasn't
            # edited yet) would have crashed trying to access the
            # nonexistent err.details — just report validation failure
            # and leave the cell alone.
            if not hasattr(err, "details"):
                return True

            mandatory_arguments = [
                f"{k}=?" for k, v in err.details.items() if v is inspect._empty
            ]

            uuid = err.details["element"]["__uuid"]

            updated_record = {
                k: v
                for k, v in err.details["element"].items()
                if not k.startswith("__")
            }

            updated_record["arguments"] = ", ".join(mandatory_arguments)

            self.tableview.data_source.update_record(uuid, updated_record)

            return True

    def click_copy_buttons(self, event, button):
        if button == self.copy_code_button:
            script = self.get_path_script()
            pyperclip.copy(script)

    def click_table_buttons(self, event, button):
        path = self.get_path_from_ui(without_apertures=False)

        if button == self.delete_button:
            for selected_item in self.tableview.widget.selection():
                record = self.tableview.data_source.record(selected_item)
                self.tableview.data_source.remove_record(selected_item)
        elif button == self.add_lens_button:
            record = self.tableview.data_source.empty_record()
            record["element"] = "Lens"
            record["arguments"] = "f=50, diameter=25.4"
            record["position"] = position = path.L + 50
            self.tableview.data_source.append_record(record)

    def refresh(self):
        if not self.initialization_completed:
            return

        if self.validate_source_data(self.tableview):
            return

        self.tableview.sort_column(column_name="position")

        self.canvas.widget.delete("ray")
        self.canvas.widget.delete("optics")
        self.canvas.widget.delete("apertures")
        self.canvas.widget.delete("labels")
        self.canvas.widget.delete("conjugates")
        self.canvas.widget.delete("x-axis")
        self.canvas.widget.delete("y-axis")
        self.canvas.widget.delete("tick")
        self.canvas.widget.delete("tick-label")

        try:
            user_provided_path = self.get_path_from_ui(
                without_apertures=True, max_position=None
            )
            finite_imaging_path = None
            finite_path = None

            conjugate = user_provided_path.forwardConjugate()

            if isfinite(conjugate.d):
                image_position = user_provided_path.L + conjugate.d
                finite_imaging_path = self.get_path_from_ui(
                    without_apertures=False, max_position=image_position
                )

            finite_path = finite_imaging_path
            if finite_path is None:
                finite_path = self.get_path_from_ui(
                    without_apertures=False, max_position=self.coords.axes_limits[0][1]
                )

            self.path_has_field_stop = finite_path.hasFieldStop()

            self.adjust_axes_limits(finite_path)

            self.coords.create_x_axis()
            self.coords.create_x_major_ticks()
            self.coords.create_x_major_ticks_labels()
            self.coords.create_y_axis()
            self.coords.create_y_major_ticks()
            self.coords.create_y_major_ticks_labels()

            self.calculate_imaging_path_results(finite_imaging_path)

            self.create_optical_path(finite_path, self.coords)

            if self.show_raytraces:
                self.create_all_traces(finite_path)

            if self.show_conjugates:
                self.create_conjugate_planes(finite_path)

            if self.show_apertures:
                self.create_apertures_labels(finite_path)

            if self.show_labels:
                self.create_object_labels(finite_path)
        except ValueError as err:
            pass

    def adjust_axes_limits(self, path):
        # half_diameter = (
        #     max(
        #         filter(
        #             lambda e: e is not None and type(e) != str,
        #             self.tableview.data_source.field("diameter"),
        #         )
        #     )
        #     / 2
        # )
        half_diameter = 40

        raytraces = self.raytraces_to_display(path)
        y_min, y_max = self.raytraces_limits(raytraces)

        self.coords.axes_limits = (
            (0, path.L),
            (min(y_min, -half_diameter) * 1.1, max(y_max, half_diameter) * 1.1),
        )

    def raytraces_limits(self, raytraces):
        ys = []
        for raytrace in raytraces:
            ys.extend([ray.y for ray in raytrace])
        y_max = max(ys)
        y_min = min(ys)
        return y_min, y_max

    def raytraces_to_display(self, path):
        if self.show_principal_rays:
            principal_ray = path.principalRay()
            if principal_ray is not None:
                principal_raytrace = path.trace(principal_ray)
                axial_ray = path.axialRay()
                axial_raytrace = path.trace(axial_ray)
                return [principal_raytrace, axial_raytrace]
        else:
            M = int(self.number_of_heights)
            N = int(self.number_of_angles)
            yMax = float(self.max_height)
            thetaMax = float(self.max_fan_angle)

            if M == 1:
                yMax = 0
            if N == 1:
                thetaMax = 0
            rays = UniformRays(yMax=yMax, thetaMax=thetaMax, M=M, N=N)
            return path.traceMany(rays)

    def create_all_traces(self, path):
        if self.show_principal_rays:
            basis = DynamicBasis(self.coords, "basis")
            principal_ray = path.principalRay()
            if principal_ray is not None:
                for raytrace, color in (
                    (path.trace(principal_ray), "green"),
                    (path.trace(path.axialRay()), "red"),
                ):
                    for segment in self.create_line_segments_from_raytrace(
                        raytrace, basis=basis, color=color
                    ):
                        self.coords.place(segment, position=Point(0, 0))

        else:
            M = int(self.number_of_heights)
            N = int(self.number_of_angles)
            yMax = float(self.max_height)
            thetaMax = float(self.max_fan_angle)

            if M == 1:
                yMax = 0
            if N == 1:
                thetaMax = 0
            rays = UniformRays(yMax=yMax, thetaMax=thetaMax, M=M, N=N)
            self.create_raytraces_lines(path, rays)

    def create_conjugate_planes(self, path):
        arrow_width = 10
        object_z = 0
        object_height = float(self.max_height) * 2
        if self.show_principal_rays:
            object_height = path.fieldOfView()

        basis = DynamicBasis(self.coords, "basis")
        canvas_object = Arrow(
            start=Point(object_z, -object_height / 2, basis=basis),
            end=Point(object_z, object_height / 2, basis=basis),
            fill="blue",
            width=arrow_width,
            tag=("conjugates"),
        )
        self.coords.place(canvas_object, position=Point(0, 0))

        conjugate = path.forwardConjugate()
        if conjugate.transferMatrix is not None:
            image_z = conjugate.transferMatrix.L
            magnification = conjugate.transferMatrix.magnification().transverse
            image_height = magnification * object_height
            canvas_image = Arrow(
                start=Point(image_z, -image_height / 2, basis=basis),
                end=Point(image_z, image_height / 2, basis=basis),
                fill="red",
                width=arrow_width,
                tag=("conjugates"),
            )
            self.coords.place(canvas_image, position=Point(0, 0))

    def create_apertures_labels(self, path):
        position = path.apertureStop()
        y_lims = self.coords.axes_limits[1]
        label_position = y_lims[1] * 1.4

        if position.z is not None:
            aperture_stop_label = CanvasLabel(text="AS", tag=("apertures"))
            self.coords.place(
                aperture_stop_label, position=Point(position.z, label_position)
            )

        position = path.fieldStop()
        if position.z is not None:
            field_stop_label = CanvasLabel(text="FS", tag=("apertures"))
            self.coords.place(
                field_stop_label, position=Point(position.z, label_position)
            )

    def create_object_labels(self, path):
        z = 0
        y_lims = self.coords.axes_limits[1]
        label_position = y_lims[1] * 1.1
        for element in path:
            label = CanvasLabel(text=element.label, tag=("labels"))
            self.coords.place(label, position=Point(z, label_position))
            z += element.L

    def create_raytraces_lines(self, path, rays):
        raytraces = path.traceMany(rays)

        if self.dont_show_blocked_rays:
            raytraces_to_show = [
                raytrace for raytrace in raytraces if not raytrace[-1].isBlocked
            ]
        else:
            raytraces_to_show = raytraces

        line_traces = self.raytraces_to_lines(
            raytraces_to_show, DynamicBasis(self.coords, "basis")
        )

        for line_trace in line_traces:
            self.canvas.place(line_trace, position=self.coords_origin)
            self.canvas.widget.tag_lower(line_trace.id)

    def fill_color_for_index(self, n):
        n_max = 1.6
        t = (n - 1) / (n_max - 1)

        base_color = (173, 216, 255)
        r = round(255 + t * (base_color[0] - 255))
        g = round(255 + t * (base_color[1] - 255))
        b = round(255 + t * (base_color[2] - 255))

        return f"#{r:02x}{g:02x}{b:02x}"

    def create_optical_path(self, path, coords):
        # Each drawer places all canvas items for one element at position z.
        # Compound elements (doublets, objectives) are checked first via
        # isinstance so they're drawn as a single unit instead of being
        # decomposed into their child surfaces.
        type_drawers = {
            Lens: self._draw_thin_lens,
            Aperture: self._draw_aperture,
            ThickLens: lambda z, e, c: self._draw_thick_element(z, e, c, Oval),
            DielectricSlab: lambda z, e, c: self._draw_thick_element(z, e, c, Rectangle),
        }

        z = 0
        for element in path:
            if isinstance(element, AchromatDoubletLens):
                self._draw_doublet(z, element, coords)
            elif isinstance(element, Objective):
                self._draw_objective(z, element, coords)
            else:
                draw = type_drawers.get(type(element))
                if draw is not None:
                    draw(z, element, coords)
            z += element.L

    def _draw_aperture_marks(self, z_start, z_end, diameter, coords):
        # Two horizontal lines marking the rim at ±diameter/2 along the
        # whole z extent of the element. For thin elements pass
        # z_start == z_end and the marks degenerate to short ticks
        # (extended ±3 beyond the vertex for visibility). For thick
        # elements (ThickLens, doublet, slab) the marks span the full
        # length so the rim reads as a continuous line.
        overhang = min(3, abs(z_start - z_end))
        half_d = diameter / 2
        for y_sign in (1, -1):
            mark = Line(
                points=(
                    Point(z_start - overhang, y_sign * half_d, basis=coords.basis),
                    Point(z_end + overhang, y_sign * half_d, basis=coords.basis),
                ),
                fill="black",
                width=4,
                tag=("optics"),
            )
            coords.place(mark, position=Point(0, 0, basis=coords.basis))

    def _draw_thin_lens(self, z, element, coords):
        diameter = element.apertureDiameter
        if isfinite(diameter):
            self._draw_aperture_marks(z, z, diameter, coords)
        else:
            y_lims = self.coords.axes_limits[1]
            diameter = 0.98 * (y_lims[1] - y_lims[0])

        body = Oval(
            size=(5, diameter),
            basis=coords.basis,
            position_is_center=True,
            fill=self.fill_color_for_index(1.5),
            outline="black",
            width=2,
            tag=("optics"),
        )
        coords.place(body, position=Point(z, 0, basis=coords.basis))

    def _draw_aperture(self, z, element, coords):
        diameter = element.apertureDiameter
        if not isfinite(diameter):
            diameter = 90
        self._draw_aperture_marks(z, z, diameter, coords)

    def _draw_thick_element(self, z, element, coords, body_class):
        diameter = element.apertureDiameter
        if isfinite(diameter):
            self._draw_aperture_marks(z, z + element.L, diameter, coords)
        else:
            y_lims = self.coords.axes_limits[1]
            diameter = 0.98 * (y_lims[1] - y_lims[0])

        body = body_class(
            size=(element.L, diameter),
            basis=coords.basis,
            position_is_center=True,
            fill=self.fill_color_for_index(element.n),
            outline="black",
            width=2,
            tag=("optics"),
        )
        coords.place(body, position=Point(z + element.L / 2, 0, basis=coords.basis))

    def _arc_points(self, z_vertex, R, half_diameter, n_samples=30):
        # Sample n_samples+1 points along a spherical surface of radius R,
        # vertex at (z_vertex, 0), running from y=-half_diameter to
        # y=+half_diameter. R > 0: center of curvature to the right of the
        # vertex (surface bulges left). R < 0: center to the left (bulges
        # right). For a flat surface (infinite R), returns just the two
        # endpoints — the polygon edge is a straight line.
        if not isfinite(R):
            return [(z_vertex, -half_diameter), (z_vertex, half_diameter)]

        # A spherical surface cannot be wider than its own diameter (2|R|);
        # clamp so we don't take sqrt of a negative number for over-sized
        # lenses. The 0.999 keeps us strictly inside the sphere.
        if half_diameter >= abs(R):
            half_diameter = abs(R) * 0.999

        points = []
        for i in range(n_samples + 1):
            y = -half_diameter + i * (2 * half_diameter) / n_samples
            # On the sphere centered at (z_vertex + R, 0):
            #   (z - (z_vertex + R))**2 + y**2 = R**2
            #   z = z_vertex + R - sign(R) * sqrt(R**2 - y**2)
            z = z_vertex + R - copysign(sqrt(R * R - y * y), R)
            points.append((z, y))
        return points

    def _lens_body_points(self, z_front, R_front, z_back, R_back, half_diameter):
        # Closed polygon for the glass between two spherical surfaces:
        # walk the front surface bottom → top, across the top rim, down
        # the back surface, across the bottom rim, close.
        #
        # Each of the four corners (where an arc meets a rim) is
        # duplicated 3x. Under smooth=True Tk's Bezier smoothing passes
        # through repeated points without curving them, which keeps the
        # top/bottom rims straight while the arcs stay smooth. Without
        # the repeats, the rim segments get bent into curves too.
        front = self._arc_points(z_front, R_front, half_diameter)
        back = list(reversed(self._arc_points(z_back, R_back, half_diameter)))
        pts = (
            [front[0]] * 3 +       # pin bottom-front corner
            front[1:-1] +
            [front[-1]] * 3 +      # pin top-front corner
            [back[0]] * 3 +        # pin top-back corner
            back[1:-1] +
            [back[-1]] * 3         # pin bottom-back corner
        )
        return [Point(z, y, basis=None) for z, y in pts]

    def _place_lens_body(self, z_front, R_front, z_back, R_back, half_diameter,
                          fill_color, coords):
        # Build a Polygon from sampled arc points and place it on the canvas.
        # Points are constructed with a basis of None then re-parented to
        # the coordinate system at place-time via the position argument.
        body_points = self._lens_body_points(
            z_front, R_front, z_back, R_back, half_diameter
        )
        for p in body_points:
            p.basis = coords.basis

        body = Polygon(
            points=body_points,
            basis=coords.basis,
            fill=fill_color,
            outline="black",
            width=2,
            # smooth=True tells Tk to Bezier-interpolate between the
            # sampled arc points instead of connecting them with straight
            # segments, which is what made the polyline approximation
            # look jagged. splinesteps controls the curve resolution per
            # segment — 24 is plenty for a 30-sample arc.
            smooth=True,
            splinesteps=24,
            tag=("optics"),
        )
        coords.place(body, position=Point(0, 0, basis=coords.basis))

    def _draw_doublet(self, z, element, coords):
        # AchromatDoubletLens has three surfaces (R1, R2, R3) and two
        # thicknesses (tc1, tc2). We render the crown (between R1 and R2)
        # and the flint (between R2 and R3) as two separate filled
        # polygons. The cement interface at R2 falls naturally as the
        # shared edge between the two — no separate line needed.
        diameter = element.apertureDiameter
        if isfinite(diameter):
            self._draw_aperture_marks(z, z + element.L, diameter, coords)
        else:
            y_lims = self.coords.axes_limits[1]
            diameter = 0.98 * (y_lims[1] - y_lims[0])
        half_d = diameter / 2

        z_R1 = z
        z_R2 = z + element.tc1
        z_R3 = z + element.tc1 + element.tc2

        self._place_lens_body(
            z_R1, element.R1, z_R2, element.R2, half_d,
            self.fill_color_for_index(element.n1), coords,
        )
        self._place_lens_body(
            z_R2, element.R2, z_R3, element.R3, half_d,
            self.fill_color_for_index(element.n2), coords,
        )

    def _draw_objective(self, z, element, coords):
        # Objectives render as a dashed truncated-cone silhouette:
        # back aperture at the entry plane, narrowing to the front
        # aperture at (L - workingDistance). This matches the matplotlib
        # ObjectiveGraphic shape from the main raytracing library.
        L = element.focusToFocusLength
        wd = element.workingDistance
        half_back = element.backAperture / 2
        half_front = element.frontAperture / 2
        # NA dictates how steeply the cone narrows toward the front.
        shoulder = half_back / element.NA if element.NA else 0

        outline = [
            (z, half_back),
            (z + L - shoulder, half_back),
            (z + L - wd, half_front),
            (z + L - wd, -half_front),
            (z + L - shoulder, -half_back),
            (z, -half_back),
        ]
        if getattr(element, "isFlipped", False):
            outline = [(2 * z + L - zp, y) for zp, y in outline]

        body = Polygon(
            points=[Point(zp, y, basis=coords.basis) for zp, y in outline],
            basis=coords.basis,
            fill="",
            outline="black",
            width=2,
            dash=(5, 3),
            tag=("optics"),
        )
        coords.place(body, position=Point(0, 0, basis=coords.basis))

    def raytraces_to_lines(self, raytraces, basis):
        line_traces = []

        all_initial_y = [raytrace[0].y for raytrace in raytraces]
        max_y = max(all_initial_y)
        min_y = min(all_initial_y)

        with PointDefault(basis=basis):
            for raytrace in raytraces:
                initial_y = raytrace[0].y
                if float(max_y - min_y) != 0:
                    hue = (initial_y - min_y) / float(max_y - min_y)
                else:
                    hue = 1.0
                color = self.color_from_hue(hue)

                line_segments = self.create_line_segments_from_raytrace(
                    raytrace, basis=basis, color=color
                )
                line_traces.extend(line_segments)

        return line_traces

    def create_line_segments_from_raytrace(self, raytrace, basis, color):
        points = [Point(r.z, r.y, basis=basis) for r in raytrace]
        return [Line(points, tag=("ray"), fill=color, width=2)]

    def color_from_hue(self, hue):
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        rgbi = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        return "#{0:02x}{1:02x}{2:02x}".format(*rgbi)

    @staticmethod
    def parse_element_call(expr_str: str) -> tuple[str, dict]:
        # Parse the string as an expression
        expr = ast.parse(expr_str, mode="eval")

        # Make sure it's a function or constructor call
        if not isinstance(expr.body, ast.Call):
            raise ValueError("Expected a function or constructor call")

        # Extract the class/function name
        if isinstance(expr.body.func, ast.Name):
            class_name = expr.body.func.id
        else:
            raise ValueError("Unsupported function expression")

        # Extract keyword arguments as a dictionary
        kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in expr.body.keywords}

        return class_name, kwargs

    @staticmethod
    def instantiate_element(class_name, class_kwargs) -> Any:
        # allowed_classes = {
        #     "Lens": Lens,
        #     "Aperture": Aperture,
        #     "DielectricInterface": DielectricInterface,
        #     "Matrix": Matrix,
        #     "ThickLens": ThickLens,
        #     "DielectricSlab":DielectricSlab
        # }

        cls = globals()[class_name]
        # cls = allowed_classes.get(class_name)
        if cls is None:
            raise ValueError(f"Class {class_name} not allowed")

        # Get init signature for this class
        sig = inspect.signature(cls.__init__)

        # Extract argument names and default values
        signature_kwargs = {
            name: param.default
            for name, param in sig.parameters.items()
            if name != "self"  # exclude 'self'
        }

        filtered_class_kwargs = {
            k: v for k, v in class_kwargs.items() if k in signature_kwargs
        }

        instance = None

        try:
            instance = cls(**filtered_class_kwargs)
        except Exception as err:
            instance = None

        return instance, signature_kwargs

    def _describe_element(self, element):
        # Short "f=..., diameter=..." string summarising an instantiated
        # element. Used to populate the Properties cell after a catalog
        # part is loaded so the user can see what they got. Only the
        # values that are finite are shown. Both kwarg names match real
        # constructor params for Lens / AchromatDoubletLens / Objective
        # so editing one back into the cell behaves predictably.
        parts = []
        try:
            f = element.effectiveFocalLengths()[0]
            if isfinite(f):
                parts.append(f"f={f:.1f}")
        except Exception:
            pass
        if hasattr(element, "apertureDiameter") and isfinite(element.apertureDiameter):
            parts.append(f"diameter={element.apertureDiameter:.1f}")
        return ", ".join(parts)

    def get_path_from_ui(self, without_apertures=True, max_position=None):
        path = ImagingPath()

        z = 0
        ordered_records = self.tableview.data_source.records
        if without_apertures:
            ordered_records = [
                record
                for record in ordered_records
                if "aperture" not in record["element"].lower()
            ]

        ordered_records.sort(key=lambda e: float(e["position"]))
        if max_position is not None:
            ordered_records = [
                record
                for record in ordered_records
                if record["position"] <= max_position
            ]

        for element in ordered_records:
            path_element = None

            constructor_string = f"{element['element']}({element['arguments']})"
            class_name, class_kwargs = self.parse_element_call(constructor_string)

            path_element, signature_kwargs = self.instantiate_element(
                class_name, class_kwargs
            )

            if path_element is None:
                err = ValueError(f"{class_name} requires arguments")
                err.details = signature_kwargs
                err.details["element"] = element
                raise err

            # Keep the Properties cell in sync with the instantiated
            # element: after every successful instantiation, re-derive
            # an "f=..., diameter=..." string and write it back if it
            # changed. This means switching Element from one catalog
            # part to another automatically refreshes Properties.
            # Typed input like "f=50" gets normalised to "f=50.0" on
            # the first refresh — same value, slightly different form.
            description = self._describe_element(path_element)
            if description and description != element["arguments"]:
                updated = {k: v for k, v in element.items() if not k.startswith("__")}
                updated["arguments"] = description
                self.tableview.data_source.update_record(element["__uuid"], updated)

            next_z = float(element["position"])

            delta = next_z - z

            path.append(Space(d=delta))
            path.append(path_element)
            z += delta

        if max_position is not None:
            if path.L < max_position:
                path.append(Space(d=max_position - path.L))

        return path

    def get_path_script(self):
        # Reconstruct the constructor string ("ClassName(args)") from
        # the element and arguments columns — the same format
        # get_path_from_ui parses. Works uniformly for primitives
        # (Lens, Aperture, ThickLens, ...), compound types
        # (AchromatDoubletLens, Objective) and zero-arg catalog parts
        # (AC254_050_A, PN_33_922, XLUMPlanFLN20X, ...). The old code
        # special-cased Lens and Aperture with table columns
        # (focal_length, label, diameter) that no longer exist, and
        # crashed with UnboundLocalError on anything else.
        z = 0
        ordered_records = sorted(
            self.tableview.data_source.records,
            key=lambda e: float(e["position"]),
        )

        script = (
            "from raytracing import *\n"
            "# Vendor catalog imports so part numbers like AC254_050_A\n"
            "# or PN_33_922 resolve when this script is run standalone.\n"
            "from raytracing.thorlabs import *\n"
            "from raytracing.eo import *\n"
            "from raytracing.olympus import *\n"
            "\npath = ImagingPath()\n"
        )

        for element in ordered_records:
            next_z = float(element["position"])
            delta = next_z - z
            constructor = f"{element['element']}({element['arguments']})"
            script += f"path.append(Space(d={delta}))\n"
            script += f"path.append({constructor})\n"
            z = next_z

        script += "\n"

        display_help = '''"""
There are many options for display:

1. Use the principal rays that define the optimal field of view and image size:
path.display(onlyPrincipalAndAxialRays=True)

2. Specify the rays directly in the display function:
path.display(diameter=10)

3. Specify the rays for a given object diameter with a different (but equivalent) display function:
path.displayWithObject(diameter=10, rayNumber=3, fanAngle=0.1, fanNumber=3, removeBlocked=True)

4. Provide your own rays to the display function, independent of any imaging properties

rays = RandomUniformRays(yMax=10, thetaMax=0.1, maxCount=100)
path.display(rays=rays)

rays = UniformRays(yMax=10, thetaMax=0.1, M=5, N=5)
path.display(rays=rays)

5. Provide a list of specific rays:
rays = [Ray(y=0, theta=0.1), Ray(y=0.5, theta=0)]
path.display(rays=rays)
"""
'''

        script += display_help

        script += "\n"
        if self.show_principal_rays == 0:
            script += f"rays = UniformRays(yMax={self.max_height}, thetaMax={self.max_fan_angle}, M={self.number_of_heights}, N={self.number_of_angles})\n"
            script += f"path.display(rays=rays, onlyPrincipalAndAxialRays=False, removeBlocked={self.dont_show_blocked_rays})\n"
        else:
            script += f"path.display(onlyPrincipalAndAxialRays=True)\n"

        return script

    # One row per imaging-path metric. Each lambda returns the string to
    # display in the results table; the inline `if ... else "..."` handles
    # the "this metric doesn't exist for this path" case (no aperture
    # stop, no field stop, infinite field of view).
    RESULT_ROWS = [
        # Object and image positions
        ("Object position", lambda p: "0.0 (always)"),
        ("Image position", lambda p: f"{p.L:.2f}"),

        # Aperture stop and axial ray (require an aperture stop)
        ("AS position",
            lambda p: f"{p.apertureStop().z:.2f}"
                      if p.apertureStop().z is not None else "Inexistent"),
        ("AS size",
            lambda p: f"{p.apertureStop().diameter:.2f}"
                      if p.apertureStop().z is not None else "Inexistent"),
        ("Axial ray θ_max",
            lambda p: f"{p.axialRay().theta:.2f} rad / "
                      f"{p.axialRay().theta * 180 / 3.1416:.2f}°"
                      if p.apertureStop().z is not None else "Inexistent [no AS]"),
        ("NA",
            lambda p: f"{p.NA():.1f}"
                      if p.apertureStop().z is not None else "Inexistent"),

        # Field stop, vignetting and principal ray (require a field stop)
        ("FS position",
            lambda p: f"{p.fieldStop().z:.2f}"
                      if p.fieldStop().z is not None else "Inexistent"),
        ("FS size",
            lambda p: f"{p.fieldStop().diameter:.2f}"
                      if p.fieldStop().z is not None else "Inexistent"),
        ("Has vignetting [FS before image]",
            lambda p: str(p.fieldStop().z < p.L)
                      if p.fieldStop().z is not None else "Inexistent"),
        ("Principal ray y_max",
            lambda p: f"{p.principalRay().y:.2f}"
                      if p.fieldStop().z is not None else "Inexistent [no FS]"),

        # Field of view, sizes and magnification (require a finite FOV)
        ("Field of view [FOV]",
            lambda p: f"{p.fieldOfView():.2f}"
                      if isfinite(p.fieldOfView()) else "Infinite [no FS]"),
        ("Object size [same as FOV]",
            lambda p: f"{p.fieldOfView():.2f}"
                      if isfinite(p.fieldOfView()) else "Infinite [no FS]"),
        ("Image size",
            lambda p: f"{p.imageSize():.2f}"
                      if isfinite(p.fieldOfView()) else "Infinite [no FS]"),
        ("Magnification [Transverse]",
            lambda p: f"{p.magnification()[0]:.2f}"
                      if isfinite(p.fieldOfView()) else "Inexistent"),
        ("Magnification [Angular]",
            lambda p: f"{p.magnification()[1]:.2f}"
                      if isfinite(p.fieldOfView()) else "Inexistent"),
    ]

    def calculate_imaging_path_results(self, imaging_path):
        data_source = self.results_tableview.data_source

        for uid in data_source.sorted_records_uuids(field="__uuid"):
            data_source.remove_record(uid)

        if imaging_path is None:
            data_source.append_record(
                {"property": "Imaging Path", "value": "Non-imaging/infinite conjugate"}
            )
            return

        for label, get_value in self.RESULT_ROWS:
            data_source.append_record(
                {"property": label, "value": get_value(imaging_path)}
            )

        self.results_tableview.sort_column(column_name="property")

    def save(self):
        filepath = filedialog.asksaveasfilename()
        self.canvas.save_to_pdf(filepath=filepath)


if __name__ == "__main__":
    app = RaytracingApp()

    app.mainloop()

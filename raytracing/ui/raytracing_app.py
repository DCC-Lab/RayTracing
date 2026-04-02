import sys

try:
    from tkinter import DoubleVar, StringVar
    from tkinter import filedialog
    import tkinter.ttk as ttk
    from mytk import *
    from mytk.base import BaseNotification
    from mytk.canvasview import *
    from mytk.dataviews import *
    from mytk.tableview import CellEntry, TableView
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

import time
import ast
import inspect
import traceback
from numpy import linspace, isfinite
from raytracing import *
import colorsys
import pyperclip
from contextlib import suppress

ELEMENT_DEFAULTS = {
    "Thin Lens": "f=50, diameter=25.4",
    "Aperture": "diameter=25.4",
    "CurvedMirror": "R=100, diameter=25.4",
    "DielectricInterface": "n1=1.0, n2=1.5, R=100, diameter=25.4",
    "ThickLens": "n=1.5, R1=100, R2=-100, thickness=10, diameter=25.4",
    "DielectricSlab": "n=1.5, thickness=10, diameter=25.4",
    "Axicon": "alpha=2.0, n=1.5, diameter=25.4",
}

ELEMENT_ALIASES = {
    "Thin Lens": "Lens",
    "Lens": "Lens",
    "AS": "Aperture",
    "FS": "Aperture",
    "Aperture Stop": "Aperture",
    "Field Stop": "Aperture",
}


class ElementCellEditor(CellEntry):
    def create_widget(self, master):
        record = self.tableview.data_source.record(self.item_id)

        self.parent = master
        self.value_variable = StringVar()
        self.widget = ttk.Combobox(
            master,
            textvariable=self.value_variable,
            values=list(ELEMENT_DEFAULTS.keys()),
            state="readonly",
        )
        self.widget.bind("<<ComboboxSelected>>", self.event_return_callback)
        self.widget.bind("<Escape>", self.event_focusout_callback)
        self.widget.set(str(record[self.column_name]))

    def event_return_callback(self, event):
        record = dict(self.tableview.data_source.record(self.item_id))
        new_element = self.value_variable.get()
        old_element = record.get(self.column_name)
        record[self.column_name] = new_element

        if new_element != old_element:
            default_arguments = ELEMENT_DEFAULTS.get(new_element)
            if default_arguments is not None:
                record["arguments"] = default_arguments

        self.tableview.item_modified(item_id=self.item_id, modified_record=record)
        self.event_generate("<FocusOut>")

    def event_focusout_callback(self, event):
        self.widget.destroy()


class ObjectThicknessCellEditor(CellEntry):
    def create_widget(self, master):
        record = self.tableview.data_source.record(self.item_id)

        self.parent = master
        self.value_variable = StringVar()
        self.widget = ttk.Combobox(
            master,
            textvariable=self.value_variable,
            values=["Finite", "Infinity"],
            state="readonly",
        )
        self.widget.bind("<<ComboboxSelected>>", self.event_return_callback)
        self.widget.bind("<Escape>", self.event_focusout_callback)
        current_value = str(record.get(self.column_name, "Finite"))
        if current_value not in {"Finite", "Infinity"}:
            current_value = "Finite"
        self.widget.set(current_value)

    def event_return_callback(self, event):
        record = dict(self.tableview.data_source.record(self.item_id))
        record[self.column_name] = self.value_variable.get()
        self.tableview.item_modified(item_id=self.item_id, modified_record=record)
        self.event_generate("<FocusOut>")

    def event_focusout_callback(self, event):
        self.widget.destroy()


class SmoothedPolygon(CanvasElement):
    def __init__(self, points, smooth=1, **kwargs):
        super().__init__(**kwargs)
        self.points = points
        self.smooth = smooth

    def create(self, canvas, position=None):
        if position is None:
            position = Point(0, 0, basis=self.basis)

        translated_points = [
            (position + point).standard_tuple() for point in self.points
        ]
        self.id = canvas.widget.create_polygon(
            translated_points,
            smooth=self.smooth,
            **self._element_kwargs,
        )
        return self.id


class ElementTableView(TableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active_editor_item_id = None
        self.active_editor_column_name = None

    def dismiss_active_editors(self):
        for child in self.widget.winfo_children():
            with suppress(Exception):
                child.destroy()
        self.active_editor_item_id = None
        self.active_editor_column_name = None

    def click_cell(self, item_id, column_name):
        if column_name == "solve":
            record = dict(self.data_source.record(item_id))
            current_value = record.get("solve", "")
            new_value = "" if current_value == "*" else "*"

            for other_record in list(self.data_source.records):
                other_update = {"solve": ""}
                if other_record["__uuid"] == item_id:
                    other_update["solve"] = new_value
                self.item_modified(other_record["__uuid"], {**dict(other_record), **other_update})
            return True

        if (
            self.active_editor_item_id is not None
            and (
                item_id != self.active_editor_item_id
                or column_name != self.active_editor_column_name
            )
        ):
            self.dismiss_active_editors()
        return super().click_cell(item_id, column_name)

    def focus_edit_cell(self, item_id, column_name):
        assert isinstance(column_name, str)
        record = dict(self.data_source.record(item_id))
        if column_name == "solve":
            return
        if (
            record.get("element") == "Image"
            and column_name == "thickness"
            and record.get("solve") == "*"
        ):
            return
        if record.get("element") in {"Object", "Image"} and column_name in {"element", "arguments"}:
            return
        if (
            column_name == "thickness"
            and hasattr(self.delegate, "first_real_element_record")
            and hasattr(self.delegate, "object_record")
        ):
            first_real = self.delegate.first_real_element_record()
            object_record = self.delegate.object_record()
            if (
                first_real is not None
                and object_record is not None
                and record.get("__uuid") == first_real.get("__uuid")
                and str(object_record.get("thickness", "Finite")) == "Infinity"
            ):
                return

        self.dismiss_active_editors()
        self.active_editor_item_id = item_id
        self.active_editor_column_name = column_name
        bbox = self.widget.bbox(item_id, column=column_name)
        if record.get("element") == "Object" and column_name == "thickness":
            entry_box = ObjectThicknessCellEditor(
                tableview=self,
                item_id=item_id,
                column_name=column_name,
            )
        elif column_name == "element":
            entry_box = ElementCellEditor(
                tableview=self,
                item_id=item_id,
                column_name=column_name,
            )
        else:
            entry_box = CellEntry(
                tableview=self,
                item_id=item_id,
                column_name=column_name,
            )

        entry_box.place_into(
            parent=self,
            x=bbox[0] - 2,
            y=bbox[1] - 2,
            width=bbox[2] + 4,
            height=bbox[3] + 4,
        )
        entry_box.widget.focus()


class BiconcaveLens(CanvasElement):
    def __init__(self, lens_width, height, basis=None, **kwargs):
        super().__init__(basis=basis, **kwargs)
        self.lens_width = lens_width
        self.height = height

    def create(self, canvas, position=None):
        if position is None:
            position = Point(0, 0, basis=self.basis)
        self.canvas = canvas

        half_width = self.lens_width / 2
        half_height = self.height / 2

        outline_points = (
            position + Point(-half_width, -half_height, basis=self.basis),
            position + Point(-half_width, -half_height, basis=self.basis),
            position + Point(half_width, -half_height, basis=self.basis),
            position + Point(half_width, -half_height, basis=self.basis),
            position + Point(half_width * 0.45, -half_height * 0.45, basis=self.basis),
            position + Point(half_width * 0.45, 0, basis=self.basis),
            position + Point(half_width * 0.45, half_height * 0.45, basis=self.basis),
            position + Point(half_width, half_height, basis=self.basis),
            position + Point(half_width, half_height, basis=self.basis),
            position + Point(-half_width, half_height, basis=self.basis),
            position + Point(-half_width, half_height, basis=self.basis),
            position + Point(-half_width * 0.45, half_height * 0.45, basis=self.basis),
            position + Point(-half_width * 0.45, 0, basis=self.basis),
            position + Point(-half_width * 0.45, -half_height * 0.45, basis=self.basis),
        )

        self.id = canvas.widget.create_polygon(
            [point.standard_tuple() for point in outline_points],
            smooth=1,
            **self._element_kwargs,
        )
        return self.id


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
        self.show_principal_planes = False
        self.show_intermediate_conjugates = False
        self.maximum_x = 60
        self.initialization_completed = False
        self.path_has_field_stop = True
        self.object_conjugate_mode = "Preset: finite object"
        self.image_conjugate_mode = "Preset: finite image"
        self.conjugation_status_message = ""
        self.solver_status_message = ""

        self.create_window_widgets()
        self.refresh()

    @staticmethod
    def safe_int(value, default):
        try:
            if value == "":
                return default
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def safe_float(value, default):
        try:
            if value == "":
                return default
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def parse_thickness(value):
        if isinstance(value, (int, float)):
            return float(value)
        text = str(value).strip()
        if text == "":
            return 0.0
        if text.lower() == "finite":
            return 0.0
        if text.lower() in {"inf", "+inf", "infinity", "+infinity", "∞", "+∞"}:
            return float("inf")
        if text.lower() in {"-inf", "-infinity", "-∞"}:
            return float("-inf")
        return float(text)

    @staticmethod
    def normalized_thickness_text(value):
        try:
            numeric_value = RaytracingApp.parse_thickness(value)
        except (TypeError, ValueError):
            return value

        if str(value).strip().lower() == "finite":
            return "Finite"
        if numeric_value == float("inf"):
            return "Infinity"
        if numeric_value == float("-inf"):
            return "-Infinity"
        return f"{numeric_value:g}"

    def create_window_widgets(self):
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
        # self.add_aperture_button = Button(
        #     "Add Aperture", user_event_callback=self.click_table_buttons
        # )
        # self.add_aperture_button.grid_into(
        #     self.button_group, row=0, column=1, pady=5, padx=5
        # )

        self.delete_button = Button(
            "Delete element", user_event_callback=self.click_table_buttons
        )
        self.delete_button.grid_into(self.button_group, row=0, column=2, pady=5, padx=5)

        self.move_up_button = Button(
            "⬆", user_event_callback=self.click_table_buttons
        )
        self.move_up_button.grid_into(self.button_group, row=0, column=3, pady=5, padx=5)

        self.move_down_button = Button(
            "⬇", user_event_callback=self.click_table_buttons
        )
        self.move_down_button.grid_into(
            self.button_group, row=0, column=4, pady=5, padx=5
        )

        self.copy_code_button = Button(
            "Copy script", user_event_callback=self.click_copy_buttons
        )
        self.copy_code_button.grid_into(
            self.button_group, row=0, column=5, pady=5, padx=5
        )

        self.solve_button = Button(
            "Solve", user_event_callback=self.click_table_buttons
        )
        self.solve_button.grid_into(
            self.button_group, row=0, column=6, pady=5, padx=5
        )

        self.tableview = ElementTableView(
            columns_labels={
                "thickness": "Thickness [mm]",
                "element": "Element",
                "arguments": "Properties",
                "solve": "Variable",
            }
        )

        self.tableview.grid_into(
            self.table_group,
            column=0,
            row=0,
            columnspan=2,
            pady=5,
            padx=5,
            sticky="nsew",
        )
        self.tableview.displaycolumns = [
            "thickness",
            "element",
            "arguments",
            "solve",
        ]
        for column in self.tableview.displaycolumns:
            widths = {
                "thickness": 8,
                "element": 5,
                "arguments": 150,
                "solve": 5,
            }
            self.tableview.widget.column(column, width=widths[column], anchor=W)

        self.tableview.data_source.append_record(
            {
                "element": "Object",
                "arguments": "",
                "thickness": "Finite",
                "solve": "",
            }
        )
        self.tableview.data_source.append_record(
            {
                "element": "Thin Lens",
                "arguments": "f=100, diameter=25.4",
                "thickness": 0,
                "solve": "",
            }
        )
        self.tableview.data_source.append_record(
            {
                "element": "Image",
                "arguments": "",
                "thickness": 200,
                "solve": "*",
            }
        )
        # self.tableview.data_source.append_record(
        #     {
        #         "element": "Aperture",
        #         "focal_length": "",
        #         "diameter": 10,
        #         "position": 400,
        #         "label": "Camera",
        #     }
        # )
        self.tableview.delegate = self
        self.update_variable_row_styles()

        self.results_tableview = TableView(
            columns_labels={
                "property": "Property",
                "value": "Value",
            }
        )
        self.results_tableview.grid_into(
            self.window, column=2, row=0, pady=5, padx=5, sticky="nsew"
        )
        self.results_tableview.all_elements_are_editable = False
        self.results_tableview.widget.column("property", width=250)
        self.results_tableview.widget.column("value", width=150)

        self.controls = Box(label="Display", width=200)
        self.controls.grid_into(
            self.window, column=0, row=0, columnspan=1, pady=5, padx=5, sticky="nsew"
        )

        self.control_input_rays = Box(label="Input ray", width=200)
        self.control_input_rays.grid_into(
            self.controls, column=0, row=0, columnspan=1, pady=5, padx=5, sticky="nsew"
        )

        radio_principal, radio_custom = RadioButton.linked_group(
            labels_values={"Principal rays": 1, "Custom rays": 0}
        )
        radio_custom.grid_into(
            self.control_input_rays,
            column=0,
            row=0,
            columnspan=1,
            pady=5,
            padx=5,
            sticky="nsew",
        )
        radio_principal.grid_into(
            self.control_input_rays,
            column=0,
            row=4,
            columnspan=1,
            pady=5,
            padx=5,
            sticky="nsew",
        )

        radio_principal.bind_properties("is_enabled", self, "path_has_field_stop")

        self.number_heights_label = Label(text="# ray heights:")
        self.number_heights_label.grid_into(
            self.control_input_rays, column=0, row=1, pady=5, padx=5, sticky="e"
        )

        self.number_heights_entry = Entry(
            value=str(self.number_of_heights), character_width=3
        )
        self.number_heights_entry.grid_into(
            self.control_input_rays, column=1, row=1, pady=5, padx=5, sticky="w"
        )

        self.number_angles_label = Label(text="# ray angles:")
        self.number_angles_label.grid_into(
            self.control_input_rays, column=0, row=2, pady=5, padx=5, sticky="e"
        )

        self.number_angles_entry = Entry(
            value=str(self.number_of_angles), character_width=3
        )
        self.number_angles_entry.grid_into(
            self.control_input_rays, column=1, row=2, pady=5, padx=5, sticky="w"
        )

        self.max_heights_label = Label(text="Max height:")
        self.max_heights_label.grid_into(
            self.control_input_rays, column=3, row=1, pady=5, padx=5, sticky="w"
        )

        self.max_heights_entry = Entry(value=str(self.max_height), character_width=3)
        self.max_heights_entry.grid_into(
            self.control_input_rays, column=4, row=1, pady=5, padx=5, sticky="w"
        )

        self.fan_angles_label = Label(text="Max angle:")
        self.fan_angles_label.grid_into(
            self.control_input_rays, column=3, row=2, pady=5, padx=5, sticky="w"
        )

        self.fan_angles_entry = Entry(
            value=str(self.max_fan_angle), character_width=3
        )
        self.fan_angles_entry.grid_into(
            self.control_input_rays, column=4, row=2, pady=5, padx=5, sticky="w"
        )

        self.show_conjugates_checkbox = Checkbox(label="Show object/image planes")
        self.show_conjugates_checkbox.grid_into(
            self.controls, column=0, row=1, columnspan=4, pady=5, padx=5, sticky="w"
        )

        self.show_principal_planes_checkbox = Checkbox(label="Show principal planes")
        self.show_principal_planes_checkbox.grid_into(
            self.controls, column=0, row=2, columnspan=4, pady=5, padx=5, sticky="w"
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
        optics_basis = DynamicBasis(self.coords, "basis")

        self.bind_properties(
            "number_of_heights", self.number_heights_entry, "value_variable"
        )
        self.bind_properties(
            "number_of_angles", self.number_angles_entry, "value_variable"
        )

        # self.bind_properties('maximum_x', self.maximum_x_entry, 'value_variable')
        self.bind_properties(
            "dont_show_blocked_rays", self.blocked_rays_checkbox, "value_variable"
        )
        self.bind_properties(
            "show_apertures", self.apertures_checkbox, "value_variable"
        )
        self.bind_properties("show_labels", self.show_labels_checkbox, "value_variable")
        self.bind_properties("show_principal_rays", radio_principal, "value_variable")

        self.bind_properties(
            "show_conjugates", self.show_conjugates_checkbox, "value_variable"
        )
        self.bind_properties(
            "show_principal_planes",
            self.show_principal_planes_checkbox,
            "value_variable",
        )
        self.bind_properties("max_height", self.max_heights_entry, "value_variable")
        self.bind_properties("max_fan_angle", self.fan_angles_entry, "value_variable")
        self.number_heights_entry.bind_properties(
            "is_disabled", self, "show_principal_rays"
        )
        self.number_angles_entry.bind_properties(
            "is_disabled", self, "show_principal_rays"
        )
        self.max_heights_entry.bind_properties(
            "is_disabled", self, "show_principal_rays"
        )
        self.fan_angles_entry.bind_properties(
            "is_disabled", self, "show_principal_rays"
        )
        self.blocked_rays_checkbox.bind_properties(
            "is_disabled", self, "show_principal_rays"
        )

        self.add_observer(self, "number_of_heights")
        self.add_observer(self, "number_of_angles")
        self.add_observer(self, "dont_show_blocked_rays")
        self.add_observer(self, "show_apertures")
        self.add_observer(self, "show_principal_rays")
        self.add_observer(self, "show_labels")
        self.add_observer(self, "show_conjugates")
        self.add_observer(self, "show_principal_planes")

        self.initialization_completed = True

    def canvas_did_resize(self, notification):
        self.refresh()

    def relabel_infinite_x_axis_ends(self):
        if (
            self.object_conjugate_mode != "Preset: object at infinity"
            and self.image_conjugate_mode != "Preset: image at infinity"
        ):
            return

        tick_label_ids = [
            item_id
            for item_id in self.canvas.widget.find_withtag("tick-label")
            if "x-axis" in self.canvas.widget.gettags(item_id)
        ]
        if len(tick_label_ids) < 2:
            return

        tick_label_ids.sort(key=lambda item_id: self.canvas.widget.coords(item_id)[0])
        left_label_id = tick_label_ids[0]
        right_label_id = tick_label_ids[-1]

        if self.object_conjugate_mode == "Preset: object at infinity":
            self.canvas.widget.itemconfigure(left_label_id, text="−∞")
        if self.image_conjugate_mode == "Preset: image at infinity":
            self.canvas.widget.itemconfigure(right_label_id, text="+∞")

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
        self.normalize_special_rows()
        self.ensure_image_row_last()
        self.update_variable_row_styles()
        self.solver_status_message = ""
        self.refresh()

    def ordered_table_records(self):
        return [dict(self.tableview.data_source.record(item_id)) for item_id in self.tableview.items_ids()]

    def image_record(self):
        for record in self.ordered_table_records():
            if record.get("element") == "Image":
                return record
        return None

    def object_record(self):
        for record in self.ordered_table_records():
            if record.get("element") == "Object":
                return record
        return None

    def first_real_element_record(self):
        for record in self.ordered_table_records():
            if record.get("element") not in {"Object", "Image"}:
                return record
        return None

    def normalize_special_rows(self):
        for record in self.ordered_table_records():
            if "thickness" not in record:
                continue
            normalized_value = self.normalized_thickness_text(record["thickness"])
            if normalized_value != record["thickness"]:
                self.tableview.data_source.update_record(
                    record["__uuid"], {"thickness": normalized_value}
                )

        object_record = self.object_record()
        image_record = self.image_record()
        self.conjugation_status_message = ""
        if object_record is not None:
            object_is_infinite = (
                self.parse_thickness(object_record.get("thickness", "Finite")) == float("inf")
            )
            self.object_conjugate_mode = (
                "Preset: object at infinity" if object_is_infinite else "Preset: finite object"
            )
            first_real_element = self.first_real_element_record()
            if first_real_element is not None:
                if object_is_infinite:
                    updates = {}
                    try:
                        first_thickness = self.parse_thickness(first_real_element.get("thickness", 0))
                    except (TypeError, ValueError):
                        first_thickness = 0.0
                    if isfinite(first_thickness):
                        updates["__finite_thickness_backup"] = self.normalized_thickness_text(
                            first_real_element.get("thickness", 0)
                        )
                    if first_real_element.get("thickness") != "Infinity":
                        updates["thickness"] = "Infinity"
                    if updates:
                        self.tableview.data_source.update_record(
                            first_real_element["__uuid"], updates
                        )
                else:
                    if str(first_real_element.get("thickness", "")) == "Infinity":
                        restored_value = first_real_element.get("__finite_thickness_backup", "200")
                        self.tableview.data_source.update_record(
                            first_real_element["__uuid"], {"thickness": restored_value}
                        )
        if image_record is not None:
            image_is_infinite = self.parse_thickness(image_record.get("thickness", 0)) == float("inf")
            self.image_conjugate_mode = (
                "Preset: image at infinity" if image_is_infinite else "Preset: finite image"
            )

    def ensure_image_row_last(self):
        records = self.ordered_table_records()
        if not records:
            return

        object_records = [record for record in records if record.get("element") == "Object"]
        non_special_records = [
            record for record in records if record.get("element") not in {"Object", "Image"}
        ]
        image_records = [record for record in records if record.get("element") == "Image"]
        if len(image_records) != 1 or len(object_records) != 1:
            return

        desired_records = object_records + non_special_records + image_records
        current_ids = [record["__uuid"] for record in records]
        desired_ids = [record["__uuid"] for record in desired_records]
        if current_ids == desired_ids:
            return

        for index, record in enumerate(desired_records):
            self.tableview.widget.move(record["__uuid"], "", index)

    def update_variable_row_styles(self):
        bold_font = ("TkDefaultFont", 9, "bold")
        self.tableview.widget.tag_configure(
            "solved-variable", background="#fff2b3", font=bold_font
        )
        self.tableview.widget.tag_configure(
            "normal-row", background="", font=("TkDefaultFont", 9)
        )

        for item_id in self.tableview.items_ids():
            record = dict(self.tableview.data_source.record(item_id))
            if record.get("solve") == "*":
                self.tableview.widget.item(item_id, tags=("solved-variable",))
            else:
                self.tableview.widget.item(item_id, tags=("normal-row",))

    def reorder_table_rows(self, tableview, dragged_item_id, target_item_id, insert_after):
        records = [
            dict(tableview.data_source.record(item_id))
            for item_id in tableview.items_ids()
        ]
        item_ids = [record["__uuid"] for record in records]
        if dragged_item_id not in item_ids or target_item_id not in item_ids:
            return

        dragged_index = item_ids.index(dragged_item_id)
        target_index = item_ids.index(target_item_id)

        if records[dragged_index].get("element") in {"Object", "Image"}:
            return
        if records[target_index].get("element") in {"Object", "Image"}:
            return
        if insert_after:
            target_index += 1
        tableview.widget.move(dragged_item_id, "", target_index)
        self.ensure_image_row_last()

    def move_selected_row(self, offset):
        selected_items = list(self.tableview.widget.selection())
        if not selected_items:
            return

        records = self.ordered_table_records()
        item_ids = [record["__uuid"] for record in records]
        selected_item_id = selected_items[0]
        if selected_item_id not in item_ids:
            return
        selected_index = item_ids.index(selected_item_id)
        if records[selected_index].get("element") in {"Object", "Image"}:
            return
        target_index = selected_index + offset

        if target_index < 0 or target_index >= len(records):
            return
        if records[target_index].get("element") in {"Object", "Image"}:
            return

        target_item_id = item_ids[target_index]
        insert_index = target_index
        if offset > 0:
            insert_index = target_index + 1
        self.tableview.widget.move(selected_item_id, "", insert_index)
        self.ensure_image_row_last()

        self.tableview.widget.selection_set(selected_item_id)

    def validate_source_data(self, tableview):
        try:
            self.get_path_from_ui(
                without_apertures=True, max_position=None, include_image_plane=False
            )
            return False
        except Exception as err:
            if not hasattr(err, "details") or not isinstance(err.details, dict):
                traceback.print_exc()
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
            # Dialog.showerror(
            #     title=f"Error in element argument",
            #     message=f"The element {uuid} requires at least the following arguments: {', '.join(mandatory_arguments)}",
            # )

            return True

    def click_copy_buttons(self, event, button):
        if button == self.copy_code_button:
            script = self.get_path_script()
            pyperclip.copy(script)

    def click_table_buttons(self, event, button):
        path = self.get_path_from_ui(
            without_apertures=False, include_image_plane=False
        )

        if button == self.delete_button:
            self.tableview.dismiss_active_editors()
            self.tableview.widget.focus_set()
            for selected_item in self.tableview.widget.selection():
                record = dict(self.tableview.data_source.record(selected_item))
                if record.get("element") not in {"Object", "Image"}:
                    self.tableview.data_source.remove_record(selected_item)
            self.tableview.widget.update_idletasks()
        elif button == self.add_lens_button:
            record = self.tableview.data_source.empty_record()
            record["element"] = "Thin Lens"
            record["arguments"] = "f=50, diameter=25.4"
            record["thickness"] = 50
            record["solve"] = ""
            self.tableview.data_source.append_record(record)
            self.ensure_image_row_last()
        elif button == self.move_up_button:
            self.move_selected_row(-1)
        elif button == self.move_down_button:
            self.move_selected_row(1)
        elif button == self.solve_button:
            self.solve_marked_variable()
        elif button == self.add_aperture_button:
            record = self.tableview.data_source.empty_record()
            record["element"] = "Aperture"
            record["arguments"] = "diameter=25.4"
            record["thickness"] = 50
            record["solve"] = ""
            self.tableview.data_source.append_record(record)

    def solve_marked_variable(self):
        variable_records = [
            record for record in self.ordered_table_records() if record.get("solve") == "*"
        ]
        if len(variable_records) != 1:
            self.solver_status_message = "Mark exactly one variable row."
            self.refresh()
            return

        variable_record = variable_records[0]
        if variable_record.get("element") != "Image":
            self.solver_status_message = "First pass only solves Image thickness."
            self.refresh()
            return

        system_path = self.get_path_from_ui(
            without_apertures=False, max_position=None, include_image_plane=False
        )
        conjugate = system_path.forwardConjugate()
        if conjugate.transferMatrix is None or conjugate.d is None or not isfinite(conjugate.d):
            self.solver_status_message = "Image distance is not finite for this system."
            self.refresh()
            return

        solved_image_distance = conjugate.d
        self.tableview.data_source.update_record(
            variable_record["__uuid"], {"thickness": solved_image_distance}
        )
        self.update_variable_row_styles()
        self.solver_status_message = f"Solved image distance = {solved_image_distance:.4g} mm."
        self.refresh()

    def refresh(self):
        if not self.initialization_completed:
            return

        if self.validate_source_data(self.tableview):
            return

        self.canvas.widget.delete("ray")
        self.canvas.widget.delete("optics")
        self.canvas.widget.delete("apertures")
        self.canvas.widget.delete("labels")
        self.canvas.widget.delete("conjugates")
        self.canvas.widget.delete("principal-planes")
        self.canvas.widget.delete("x-axis")
        self.canvas.widget.delete("y-axis")
        self.canvas.widget.delete("tick")
        self.canvas.widget.delete("tick-label")

        try:
            user_provided_path = self.get_path_from_ui(
                without_apertures=True, max_position=None, include_image_plane=False
            )
            finite_imaging_path = None
            finite_path = None

            if (
                self.object_conjugate_mode == "Preset: finite object"
                and self.image_conjugate_mode == "Preset: finite image"
            ):
                finite_path = self.get_path_from_ui(
                    without_apertures=False, max_position=None, include_image_plane=True
                )
                finite_imaging_path = finite_path

            elif (
                self.object_conjugate_mode == "Preset: object at infinity"
                and self.image_conjugate_mode == "Preset: finite image"
            ):
                finite_path = self.get_path_from_ui(
                    without_apertures=False, max_position=None
                )
                finite_imaging_path = self.get_path_from_ui(
                    without_apertures=False, max_position=None
                )
                back_focus = finite_imaging_path.backFocalLength()
                if back_focus is not None and isfinite(back_focus) and back_focus > 0:
                    finite_imaging_path.append(Space(d=back_focus))
            else:
                conjugate = user_provided_path.forwardConjugate()

                if isfinite(conjugate.d):
                    image_position = user_provided_path.L + conjugate.d
                    if image_position > 0:
                        finite_imaging_path = self.get_path_from_ui(
                            without_apertures=False, max_position=image_position
                        )
                    else:
                        finite_imaging_path = None

            if (
                self.object_conjugate_mode == "Preset: finite object"
                and self.image_conjugate_mode == "Preset: image at infinity"
            ):
                if finite_path is None:
                    finite_path = self.get_path_from_ui(
                        without_apertures=False, max_position=None
                    )
                finite_path.append(
                    Space(d=self.infinite_image_display_extension(finite_path))
                )

            if finite_path is None:
                finite_path = finite_imaging_path
            if finite_path is None:
                finite_path = self.get_path_from_ui(
                    without_apertures=False, max_position=self.coords.axes_limits[0][1]
                )

            display_path = finite_path
            if (
                self.object_conjugate_mode == "Preset: object at infinity"
                and self.image_conjugate_mode == "Preset: finite image"
                and finite_imaging_path is not None
            ):
                display_path = finite_imaging_path

            self.path_has_field_stop = display_path.hasFieldStop()

            self.adjust_axes_limits(display_path)
            self.coords.create_x_axis()
            self.coords.create_x_major_ticks()
            self.coords.create_x_major_ticks_labels()
            self.coords.create_y_axis()
            self.coords.create_y_major_ticks()
            self.coords.create_y_major_ticks_labels()
            self.relabel_infinite_x_axis_ends()

            self.calculate_imaging_path_results(finite_imaging_path)

            self.create_optical_path(display_path, self.coords)

            if self.show_raytraces:
                self.create_all_traces(display_path)

            if self.show_conjugates:
                self.create_conjugate_planes(
                    finite_imaging_path if finite_imaging_path is not None else finite_path
                )

            if self.show_principal_planes:
                self.create_principal_planes(finite_path)

            if self.show_apertures:
                self.create_apertures_labels(display_path)

            if self.show_labels:
                self.create_object_labels(display_path)
        except Exception:
            traceback.print_exc()

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

        x_max = max(float(path.L), 1.0)

        self.coords.axes_limits = (
            (0, x_max),
            (min(y_min, -half_diameter) * 1.1, max(y_max, half_diameter) * 1.1),
        )

    def raytraces_limits(self, raytraces):
        if not raytraces:
            return (-1.0, 1.0)
        ys = []
        for raytrace in raytraces:
            ys.extend([ray.y for ray in raytrace])
        if not ys:
            return (-1.0, 1.0)
        y_max = max(ys)
        y_min = min(ys)
        return y_min, y_max

    def visible_image_size(self, path):
        raytraces = self.raytraces_to_display(path)
        output_ys = [
            raytrace[-1].y for raytrace in raytraces if raytrace and not raytrace[-1].isBlocked
        ]
        if not output_ys:
            return None
        return max(output_ys) - min(output_ys)

    def input_rays_to_display(self):
        M = self.safe_int(self.number_of_heights, 5)
        N = self.safe_int(self.number_of_angles, 5)
        yMax = self.safe_float(self.max_height, 5.0)
        thetaMax = self.safe_float(self.max_fan_angle, 0.1)

        if M == 1:
            yMax = 0
        if N == 1:
            thetaMax = 0

        if self.object_conjugate_mode == "Preset: object at infinity":
            # On-axis object at infinity: incoming rays are parallel before the first element.
            return UniformRays(yMax=yMax, yMin=-yMax, thetaMax=0, thetaMin=0, M=M, N=1)

        return UniformRays(yMax=yMax, thetaMax=thetaMax, M=M, N=N)

    def infinite_image_display_extension(self, path):
        if path is None:
            return 100.0
        return max(100.0, path.L * 0.5)

    def raytraces_to_display(self, path):
        if self.show_principal_rays and self.object_conjugate_mode != "Preset: object at infinity":
            raytraces = []
            principal_ray = path.principalRay()
            if principal_ray is not None:
                principal_raytrace = path.trace(principal_ray)
                raytraces.append(principal_raytrace)
            axial_ray = path.axialRay()
            if axial_ray is not None:
                axial_raytrace = path.trace(axial_ray)
                raytraces.append(axial_raytrace)
            if raytraces:
                return raytraces
        rays = self.input_rays_to_display()
        return path.traceMany(rays)

    def create_all_traces(self, path):
        if self.show_principal_rays and self.object_conjugate_mode != "Preset: object at infinity":
            line_traces = []
            principal_ray = path.principalRay()
            if principal_ray is not None:
                principal_raytrace = path.trace(principal_ray)
                line_traces.extend(
                    self.create_line_segments_from_raytrace(
                        principal_raytrace,
                        basis=DynamicBasis(self.coords, "basis"),
                        color="green",
                    )
                )

            axial_ray = path.axialRay()
            if axial_ray is not None:
                axial_raytrace = path.trace(axial_ray)
                line_traces.extend(
                    self.create_line_segments_from_raytrace(
                        axial_raytrace,
                        basis=DynamicBasis(self.coords, "basis"),
                        color="red",
                    )
                )

            if not line_traces:
                M = self.safe_int(self.number_of_heights, 5)
                N = self.safe_int(self.number_of_angles, 5)
                yMax = self.safe_float(self.max_height, 5.0)
                thetaMax = self.safe_float(self.max_fan_angle, 0.1)

                if M == 1:
                    yMax = 0
                if N == 1:
                    thetaMax = 0
                rays = UniformRays(yMax=yMax, thetaMax=thetaMax, M=M, N=N)
                self.create_raytraces_lines(path, rays)
                return

            for line_trace in line_traces:
                self.canvas.place(line_trace, position=self.coords_origin)
                self.canvas.widget.tag_lower(line_trace.id)

        else:
            rays = self.input_rays_to_display()
            self.create_raytraces_lines(path, rays)

    def create_conjugate_planes(self, path):
        arrow_width = 10
        object_z = 0
        object_height = self.safe_float(self.max_height, 5.0) * 2
        if self.show_principal_rays:
            object_height = path.fieldOfView()
            if not isfinite(object_height):
                object_height = self.safe_float(self.max_height, 5.0) * 2

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

    def create_principal_planes(self, path):
        principal_planes = path.principalPlanePositions(z=0)
        y_lims = self.coords.axes_limits[1]
        line_height = y_lims[1] - y_lims[0]
        label_y = y_lims[1] * 1.2
        plane_labels = []
        if principal_planes.z1 is not None and isfinite(principal_planes.z1):
            plane_labels.append((principal_planes.z1, "H1"))
        if principal_planes.z2 is not None and isfinite(principal_planes.z2):
            plane_labels.append((principal_planes.z2, "H2"))

        if len(plane_labels) == 2 and abs(plane_labels[0][0] - plane_labels[1][0]) < 1e-9:
            plane_labels = [(plane_labels[0][0], "H1 = H2")]

        for z_value, label_text in plane_labels:
            if z_value is None or not isfinite(z_value):
                continue

            line = Line(
                points=(
                    Point(0, -line_height / 2, basis=self.coords.basis),
                    Point(0, line_height / 2, basis=self.coords.basis),
                ),
                fill="purple",
                width=2,
                tag=("principal-planes"),
            )
            self.coords.place(line, position=Point(z_value, 0, basis=self.coords.basis))
            self.coords.place(
                CanvasLabel(text=label_text, tag=("principal-planes")),
                position=Point(z_value, label_y),
            )

    def create_apertures_labels(self, path):
        y_lims = self.coords.axes_limits[1]
        label_position = y_lims[1] * 1.4
        aperture_labels = []

        aperture_stop = path.apertureStop()
        if aperture_stop.z is not None and isfinite(aperture_stop.z):
            aperture_labels.append((aperture_stop.z, "AS"))

        field_stop = path.fieldStop()
        if field_stop.z is not None and isfinite(field_stop.z):
            aperture_labels.append((field_stop.z, "FS"))

        if len(aperture_labels) == 2 and abs(aperture_labels[0][0] - aperture_labels[1][0]) < 1e-9:
            aperture_labels = [(aperture_labels[0][0], "AS = FS")]

        for z_value, label_text in aperture_labels:
            self.coords.place(
                CanvasLabel(text=label_text, tag=("apertures")),
                position=Point(z_value, label_position),
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

        if not line_traces:
            self.coords.place(
                CanvasLabel(text="No drawable rays", tag=("labels")),
                position=Point(10, self.coords.axes_limits[1][1] * 0.85),
            )

    def fill_color_for_index(self, n):
        n_max = 1.6
        t = (n - 1) / (n_max - 1)

        base_color = (173, 216, 255)
        r = round(255 + t * (base_color[0] - 255))
        g = round(255 + t * (base_color[1] - 255))
        b = round(255 + t * (base_color[2] - 255))

        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def thick_surface_sag(radius, semi_diameter, thickness):
        if radius is None or not isfinite(radius) or radius == 0:
            return 0.0

        usable_height = min(abs(semi_diameter), abs(radius) * 0.98)
        if usable_height <= 0:
            return 0.0

        sag = abs(radius) - (abs(radius) ** 2 - usable_height ** 2) ** 0.5
        return min(max(sag, 0.0), max(thickness * 0.45, 0.0))

    def thick_lens_outline_points(self, element, diameter, basis):
        half_height = diameter / 2
        thickness = max(element.L, 1e-6)

        front_sag = self.thick_surface_sag(element.R1, half_height, thickness)
        back_sag = self.thick_surface_sag(element.R2, half_height, thickness)

        if element.R1 > 0:
            front_corner_x = front_sag
            front_mid_x = 0
        else:
            front_corner_x = 0
            front_mid_x = front_sag

        if element.R2 < 0:
            back_corner_x = thickness - back_sag
            back_mid_x = thickness
        else:
            back_corner_x = thickness
            back_mid_x = thickness - back_sag

        return (
            Point(front_corner_x, -half_height, basis=basis),
            Point(front_corner_x, -half_height, basis=basis),
            Point(back_corner_x, -half_height, basis=basis),
            Point(back_corner_x, -half_height, basis=basis),
            Point(back_mid_x, -half_height * 0.45, basis=basis),
            Point(back_mid_x, 0, basis=basis),
            Point(back_mid_x, half_height * 0.45, basis=basis),
            Point(back_corner_x, half_height, basis=basis),
            Point(back_corner_x, half_height, basis=basis),
            Point(front_corner_x, half_height, basis=basis),
            Point(front_corner_x, half_height, basis=basis),
            Point(front_mid_x, half_height * 0.45, basis=basis),
            Point(front_mid_x, 0, basis=basis),
            Point(front_mid_x, -half_height * 0.45, basis=basis),
        )

    def create_optical_path(self, path, coords):
        z = 0
        x_lims = self.coords.axes_limits[0]
        x_span = max(x_lims[1] - x_lims[0], 1.0)
        thickness = 0.003 * x_span
        drew_optics = False
        for element in path:
            if type(element) is Lens:
                diameter = element.apertureDiameter
                lens_half_width = 0.005 * x_span
                if not isfinite(diameter):
                    y_lims = self.coords.axes_limits[1]
                    diameter = 0.98 * (y_lims[1] - y_lims[0])
                else:
                    aperture_top = Line(
                        points=(
                            Point(-thickness, diameter / 2, basis=coords.basis),
                            Point(thickness, diameter / 2, basis=coords.basis),
                        ),
                        fill="black",
                        width=4,
                        tag=("optics"),
                    )
                    coords.place(aperture_top, position=Point(z, 0, basis=coords.basis))
                    aperture_bottom = Line(
                        points=(
                            Point(-thickness, -diameter / 2, basis=coords.basis),
                            Point(thickness, -diameter / 2, basis=coords.basis),
                        ),
                        fill="black",
                        width=4,
                        tag=("optics"),
                    )
                    coords.place(
                        aperture_bottom, position=Point(z, 0, basis=coords.basis)
                    )

                if getattr(element, "f", 0) < 0:
                    lens = BiconcaveLens(
                        lens_width=2 * lens_half_width,
                        height=diameter,
                        basis=coords.basis,
                        fill=self.fill_color_for_index(1.5),
                        outline="black",
                        width=2,
                        tag=("optics"),
                    )
                    coords.place(lens, position=Point(z, 0, basis=coords.basis))
                else:
                    lens = Oval(
                        size=(2 * lens_half_width, diameter),
                        basis=coords.basis,
                        position_is_center=True,
                        fill=self.fill_color_for_index(1.5),
                        outline="black",
                        width=2,
                        tag=("optics"),
                    )
                    coords.place(lens, position=Point(z, 0, basis=coords.basis))
                drew_optics = True

            elif type(element) is Aperture:
                diameter = element.apertureDiameter
                if not isfinite(diameter):
                    diameter = 90

                aperture_top = Line(
                    points=(
                        Point(-thickness, diameter / 2, basis=coords.basis),
                        Point(thickness, diameter / 2, basis=coords.basis),
                    ),
                    fill="black",
                    width=4,
                    tag=("optics"),
                )
                coords.place(aperture_top, position=Point(z, 0, basis=coords.basis))
                aperture_bottom = Line(
                    points=(
                        Point(-thickness, -diameter / 2, basis=coords.basis),
                        Point(thickness, -diameter / 2, basis=coords.basis),
                    ),
                    fill="black",
                    width=4,
                    tag=("optics"),
                )
                coords.place(aperture_bottom, position=Point(z, 0, basis=coords.basis))
                drew_optics = True

            elif type(element) is CurvedMirror:
                diameter = element.apertureDiameter
                if not isfinite(diameter):
                    y_lims = self.coords.axes_limits[1]
                    diameter = 0.98 * (y_lims[1] - y_lims[0])

                mirror_depth = 0.008 * x_span
                if getattr(element, "C", 0) > 0:
                    points = (
                        Point(0, -diameter / 2, basis=coords.basis),
                        Point(0, -diameter / 2, basis=coords.basis),
                        Point(-mirror_depth, -diameter * 0.2, basis=coords.basis),
                        Point(-mirror_depth, 0, basis=coords.basis),
                        Point(-mirror_depth, diameter * 0.2, basis=coords.basis),
                        Point(0, diameter / 2, basis=coords.basis),
                        Point(0, diameter / 2, basis=coords.basis),
                    )
                else:
                    points = (
                        Point(0, -diameter / 2, basis=coords.basis),
                        Point(0, -diameter / 2, basis=coords.basis),
                        Point(mirror_depth, -diameter * 0.2, basis=coords.basis),
                        Point(mirror_depth, 0, basis=coords.basis),
                        Point(mirror_depth, diameter * 0.2, basis=coords.basis),
                        Point(0, diameter / 2, basis=coords.basis),
                        Point(0, diameter / 2, basis=coords.basis),
                    )
                mirror = SmoothedPolygon(
                    points=points,
                    smooth=1,
                    fill="",
                    outline="black",
                    width=3,
                    tag=("optics"),
                )
                coords.place(mirror, position=Point(z, 0, basis=coords.basis))
                drew_optics = True

            elif type(element) is DielectricInterface:
                diameter = element.apertureDiameter
                if not isfinite(diameter):
                    y_lims = self.coords.axes_limits[1]
                    diameter = 0.98 * (y_lims[1] - y_lims[0])

                interface_depth = 0.006 * x_span
                radius = getattr(element, "R", float("inf"))
                if not isfinite(radius) or radius == 0:
                    interface = Line(
                        points=(
                            Point(0, -diameter / 2, basis=coords.basis),
                            Point(0, diameter / 2, basis=coords.basis),
                        ),
                        fill="black",
                        width=2,
                        tag=("optics"),
                    )
                    coords.place(interface, position=Point(z, 0, basis=coords.basis))
                else:
                    if radius > 0:
                        points = (
                            Point(0, -diameter / 2, basis=coords.basis),
                            Point(0, -diameter / 2, basis=coords.basis),
                            Point(interface_depth, -diameter * 0.2, basis=coords.basis),
                            Point(interface_depth, 0, basis=coords.basis),
                            Point(interface_depth, diameter * 0.2, basis=coords.basis),
                            Point(0, diameter / 2, basis=coords.basis),
                            Point(0, diameter / 2, basis=coords.basis),
                        )
                    else:
                        points = (
                            Point(0, -diameter / 2, basis=coords.basis),
                            Point(0, -diameter / 2, basis=coords.basis),
                            Point(-interface_depth, -diameter * 0.2, basis=coords.basis),
                            Point(-interface_depth, 0, basis=coords.basis),
                            Point(-interface_depth, diameter * 0.2, basis=coords.basis),
                            Point(0, diameter / 2, basis=coords.basis),
                            Point(0, diameter / 2, basis=coords.basis),
                        )
                    interface = SmoothedPolygon(
                        points=points,
                        smooth=1,
                        fill="",
                        outline="black",
                        width=2,
                        tag=("optics"),
                    )
                    coords.place(interface, position=Point(z, 0, basis=coords.basis))
                drew_optics = True

            elif type(element) is Axicon:
                diameter = element.apertureDiameter
                if not isfinite(diameter):
                    y_lims = self.coords.axes_limits[1]
                    diameter = 0.98 * (y_lims[1] - y_lims[0])
                axicon_half_width = 0.006 * x_span
                axicon = Line(
                    points=(
                        Point(-axicon_half_width, -diameter / 2, basis=coords.basis),
                        Point(0, 0, basis=coords.basis),
                        Point(-axicon_half_width, diameter / 2, basis=coords.basis),
                        Point(axicon_half_width, diameter / 2, basis=coords.basis),
                        Point(0, 0, basis=coords.basis),
                        Point(axicon_half_width, -diameter / 2, basis=coords.basis),
                    ),
                    fill=self.fill_color_for_index(element.n),
                    width=2,
                    tag=("optics"),
                )
                coords.place(axicon, position=Point(z, 0, basis=coords.basis))
                drew_optics = True

            elif type(element) is ThickLens:
                diameter = element.apertureDiameter
                if not isfinite(diameter):
                    y_lims = self.coords.axes_limits[1]
                    diameter = 0.98 * (y_lims[1] - y_lims[0])
                else:
                    for edge_z in (z, z + element.L):
                        aperture_top = Line(
                            points=(
                                Point(-thickness, diameter / 2, basis=coords.basis),
                                Point(thickness, diameter / 2, basis=coords.basis),
                            ),
                            fill="black",
                            width=4,
                            tag=("optics"),
                        )
                        coords.place(
                            aperture_top, position=Point(edge_z, 0, basis=coords.basis)
                        )
                        aperture_bottom = Line(
                            points=(
                                Point(-thickness, -diameter / 2, basis=coords.basis),
                                Point(thickness, -diameter / 2, basis=coords.basis),
                            ),
                            fill="black",
                            width=4,
                            tag=("optics"),
                        )
                        coords.place(
                            aperture_bottom, position=Point(edge_z, 0, basis=coords.basis)
                        )

                lens = SmoothedPolygon(
                    points=self.thick_lens_outline_points(
                        element, diameter, coords.basis
                    ),
                    smooth=1,
                    fill=self.fill_color_for_index(element.n),
                    outline="black",
                    width=2,
                    tag=("optics"),
                )
                coords.place(lens, position=Point(z, 0, basis=coords.basis))
                drew_optics = True

            elif type(element) is DielectricSlab:
                diameter = element.apertureDiameter
                if not isfinite(diameter):
                    y_lims = self.coords.axes_limits[1]
                    diameter = 0.98 * (y_lims[1] - y_lims[0])
                else:
                    for edge_z in (z, z + element.L):
                        aperture_top = Line(
                            points=(
                                Point(-thickness, diameter / 2, basis=coords.basis),
                                Point(thickness, diameter / 2, basis=coords.basis),
                            ),
                            fill="black",
                            width=4,
                            tag=("optics"),
                        )
                        coords.place(
                            aperture_top, position=Point(edge_z, 0, basis=coords.basis)
                        )
                        aperture_bottom = Line(
                            points=(
                                Point(-thickness, -diameter / 2, basis=coords.basis),
                                Point(thickness, -diameter / 2, basis=coords.basis),
                            ),
                            fill="black",
                            width=4,
                            tag=("optics"),
                        )
                        coords.place(
                            aperture_bottom, position=Point(edge_z, 0, basis=coords.basis)
                        )

                lens = Rectangle(
                    size=(element.L, diameter),
                    basis=coords.basis,
                    position_is_center=True,
                    fill=self.fill_color_for_index(element.n),
                    outline="black",
                    width=2,
                    tag=("optics"),
                )
                coords.place(
                    lens, position=Point(z + element.L / 2, 0, basis=coords.basis)
                )
                drew_optics = True

            z += element.L

        if not drew_optics:
            self.coords.place(
                CanvasLabel(text="No drawable optical elements", tag=("labels")),
                position=Point(10, self.coords.axes_limits[1][1] * 0.7),
            )

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
        finite_points = []
        for ray in raytrace:
            if isfinite(ray.z) and isfinite(ray.y):
                finite_points.append(Point(ray.z, ray.y, basis=basis))

        if len(finite_points) < 2:
            return []

        return [Line(finite_points, tag=("ray"), fill=color, width=2)]

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

        class_name = ELEMENT_ALIASES.get(class_name, class_name)
        cls = globals().get(class_name)
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
            traceback.print_exc()

        return instance, signature_kwargs

    def get_path_from_ui(self, without_apertures=True, max_position=None, include_image_plane=True):
        path = ImagingPath()

        z = 0
        ordered_records = self.ordered_table_records()
        first_real_element = self.first_real_element_record()
        object_is_infinite = (
            self.object_record() is not None
            and self.parse_thickness(self.object_record().get("thickness", "Finite")) == float("inf")
        )

        for element in ordered_records:
            element_name = element["element"]
            if element_name == "Image" and not include_image_plane:
                continue
            if without_apertures and "aperture" in element_name.lower():
                continue

            if element_name == "Object":
                continue

            delta = self.parse_thickness(element["thickness"])
            if not isfinite(delta):
                if (
                    first_real_element is not None
                    and element.get("__uuid") == first_real_element.get("__uuid")
                    and object_is_infinite
                ):
                    continue
                if element_name == "Image":
                    continue
                raise ValueError("Infinite thickness is only supported on Object or Image rows.")
            if max_position is not None and z + delta > max_position:
                delta = max_position - z
            if delta > 0:
                path.append(Space(d=delta))
                z += delta
            if max_position is not None and z >= max_position:
                break

            if element_name == "Image":
                continue

            path_element = None

            class_name = ELEMENT_ALIASES.get(element_name, element_name)
            constructor_string = f"{class_name}({element['arguments']})"
            class_name, class_kwargs = self.parse_element_call(constructor_string)

            path_element, signature_kwargs = self.instantiate_element(
                class_name, class_kwargs
            )

            if path_element is None:
                err = ValueError(f"{class_name} requires arguments")
                err.details = signature_kwargs
                err.details["element"] = element
                raise err

            path.append(path_element)
            z += path_element.L

        if self.object_conjugate_mode == "Preset: finite object" and self.image_conjugate_mode == "Preset: image at infinity":
            front_focus = path.frontFocalLength()
            if front_focus is not None and isfinite(front_focus) and front_focus > 0:
                shifted_path = ImagingPath()
                shifted_path.objectHeight = path.objectHeight
                shifted_path.append(Space(d=front_focus))
                for element in path:
                    shifted_path.append(element)
                path = shifted_path

        if max_position is not None:
            if path.L < max_position:
                path.append(Space(d=max_position - path.L))

        return path

    def get_path_script(self):
        script = "from raytracing import *\n\npath = ImagingPath()\n"

        for element in self.ordered_table_records():
            thickness = self.parse_thickness(element["thickness"])
            if isfinite(thickness) and thickness > 0:
                script += f"path.append(Space(d={thickness}))\n"
            if element["element"] in {"Object", "Image"}:
                continue

            class_name = ELEMENT_ALIASES.get(element["element"], element["element"])
            script += f"path.append({class_name}({element['arguments']}))\n"

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

    def calculate_imaging_path_results(self, imaging_path):
        data_source = self.results_tableview.data_source

        uuids = data_source.sorted_records_uuids(field="__uuid")
        for uid in uuids:
            data_source.remove_record(uid)

        if self.solver_status_message:
            data_source.append_record(
                {
                    "property": "Solve status",
                    "value": self.solver_status_message,
                }
            )

        if imaging_path is None:
            data_source.append_record(
                {"property": "Imaging Path", "value": "Non-imaging or virtual-image case"}
            )
            return
        """
        Object and Image positions
        """

        image_position = imaging_path.L
        principal_planes = imaging_path.principalPlanePositions(z=0)

        object_position_value = "Infinity" if self.object_conjugate_mode == "Preset: object at infinity" else "0.0"
        image_position_value = (
            "Infinity"
            if self.image_conjugate_mode == "Preset: image at infinity"
            else f"{image_position:.2f}"
        )
        data_source.append_record(
            {"property": "Object position", "value": object_position_value}
        )
        data_source.append_record(
            {"property": "Image position", "value": image_position_value}
        )
        if principal_planes.z1 is not None and isfinite(principal_planes.z1):
            data_source.append_record(
                {"property": "H1 position", "value": f"{principal_planes.z1:.2f}"}
            )
        else:
            data_source.append_record(
                {"property": "H1 position", "value": "Inexistent"}
            )
        if principal_planes.z2 is not None and isfinite(principal_planes.z2):
            data_source.append_record(
                {"property": "H2 position", "value": f"{principal_planes.z2:.2f}"}
            )
        else:
            data_source.append_record(
                {"property": "H2 position", "value": "Inexistent"}
            )

        """
        Aperture Stop and Axial ray
        """
        aperture_stop = imaging_path.apertureStop()
        has_aperture_stop = False

        if aperture_stop.z is not None:
            has_aperture_stop = True

        if has_aperture_stop:
            data_source.append_record(
                {"property": "AS position", "value": f"{aperture_stop.z:.2f}"}
            )
            data_source.append_record(
                {"property": "AS size", "value": f"{aperture_stop.diameter:.2f}"}
            )

            axial_ray = imaging_path.axialRay()
            if axial_ray is not None:
                NA = imaging_path.NA()
                data_source.append_record(
                    {
                        "property": "Axial ray θ_max",
                        "value": f"{axial_ray.theta:.2f} rad / {axial_ray.theta*180/3.1416:.2f}°",
                    }
                )
                data_source.append_record(
                    {
                        "property": "NA",
                        "value": f"{NA:.1f}",
                    }
                )
            else:
                data_source.append_record(
                    {
                        "property": "Axial ray θ_max",
                        "value": "Inexistent",
                    }
                )
                data_source.append_record(
                    {
                        "property": "NA",
                        "value": "Inexistent",
                    }
                )
        else:
            data_source.append_record(
                {"property": "AS position", "value": f"Inexistent"}
            )
            data_source.append_record({"property": "AS size", "value": f"Inexistent"})

            data_source.append_record(
                {"property": "Axial ray θ_max", "value": f"Inexistent [no AS]"}
            )
            data_source.append_record(
                {
                    "property": "NA",
                    "value": f"Inexistent",
                }
            )

        """
        Field Stop
        """
        has_field_stop = False
        field_stop = imaging_path.fieldStop()
        if field_stop.z is not None:
            has_field_stop = True

        if has_field_stop:
            data_source.append_record(
                {"property": "FS position", "value": f"{field_stop.z:.2f}"}
            )
            data_source.append_record(
                {"property": "FS size", "value": f"{field_stop.diameter:.2f}"}
            )
            if field_stop.z < image_position:
                data_source.append_record(
                    {"property": "Has vignetting [FS before image]", "value": f"True"}
                )
            else:
                data_source.append_record(
                    {"property": "Has vignetting [FS before image]", "value": f"False"}
                )
            principal_ray = imaging_path.principalRay()
            if principal_ray is not None:
                data_source.append_record(
                    {"property": "Principal ray y_max", "value": f"{principal_ray.y:.2f}"}
                )
            else:
                data_source.append_record(
                    {"property": "Principal ray y_max", "value": "Inexistent"}
                )
        else:
            data_source.append_record(
                {"property": "FS position", "value": f"Inexistent"}
            )
            data_source.append_record({"property": "FS size", "value": f"Inexistent"})
            data_source.append_record(
                {"property": "Has vignetting [FS before image]", "value": f"Inexistent"}
            )

            data_source.append_record(
                {"property": "Principal ray y_max", "value": f"Inexistent [no FS]"}
            )

        """
        Object [FOV] and Image Sizes, dicated by finite FOV
        """
        fov = imaging_path.fieldOfView()
        mag_tran, mag_angle = imaging_path.magnification()
        has_numeric_magnification = mag_tran is not None and mag_angle is not None
        visible_image_size = self.visible_image_size(imaging_path)

        if isfinite(fov):
            data_source.append_record(
                {"property": "Field of view [FOV]", "value": f"{fov:.2f}"}
            )
            data_source.append_record(
                {"property": "Object size [same as FOV]", "value": f"{fov:.2f}"}
            )
            image_size_value = imaging_path.imageSize()
            if visible_image_size is not None:
                image_size_value = visible_image_size
            data_source.append_record(
                {"property": "Image size", "value": f"{image_size_value:.2f}"}
            )
            if has_numeric_magnification:
                data_source.append_record(
                    {"property": "Magnification [Transverse]", "value": f"{mag_tran:.2f}"}
                )
                data_source.append_record(
                    {"property": "Magnification [Angular]", "value": f"{mag_angle:.2f}"}
                )
            else:
                data_source.append_record(
                    {"property": "Magnification [Transverse]", "value": "Inexistent"}
                )
                data_source.append_record(
                    {"property": "Magnification [Angular]", "value": "Inexistent"}
                )
        else:
            data_source.append_record(
                {"property": "Field of view [FOV]", "value": f"Infinite [no FS]"}
            )
            data_source.append_record(
                {
                    "property": "Object size [current object height]",
                    "value": f"{imaging_path.objectHeight:.2f}",
                }
            )
            image_size = imaging_path.imageSize(useObject=True)
            if isfinite(image_size):
                image_size_value = image_size
                if visible_image_size is not None:
                    image_size_value = visible_image_size
                data_source.append_record(
                    {
                        "property": "Image size",
                        "value": f"{image_size_value:.2f}",
                    }
                )
            else:
                data_source.append_record(
                    {
                        "property": "Image size",
                        "value": f"Inexistent",
                    }
                )

            if has_numeric_magnification:
                data_source.append_record(
                    {
                        "property": "Magnification [Transverse]",
                        "value": f"{mag_tran:.2f}",
                    }
                )
                data_source.append_record(
                    {
                        "property": "Magnification [Angular]",
                        "value": f"{mag_angle:.2f}",
                    }
                )
            else:
                data_source.append_record(
                    {"property": "Magnification [Transverse]", "value": f"Inexistent"}
                )
                data_source.append_record(
                    {"property": "Magnification [Angular]", "value": f"Inexistent"}
                )

        self.results_tableview.sort_column(column_name="property")

    def save(self):
        filepath = filedialog.asksaveasfilename()
        self.canvas.save_to_pdf(filepath=filepath)


if __name__ == "__main__":
    app = RaytracingApp()

    app.mainloop()

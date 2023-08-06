import os
from datetime import date, datetime, timedelta
from typing import Callable, List, Tuple, TypeVar, cast

import ipyvue
import ipyvuetify
import reacton.core
import traitlets

import solara
from solara.alias import rv

T = TypeVar("T")


@solara.value_component(int)
def SliderInt(
    label: str,
    value: int = 0,
    min: int = 0,
    max: int = 10,
    step: int = 1,
    on_value: Callable[[int], None] = None,
    thumb_label=True,
    disabled: bool = False,
):
    """Slider for controlling an integer value.

    ## Arguments

    * `label`: Label to display next to the slider.
    * `value`: The currently selected value.
    * `min`: Minimum value.
    * `max`: Maximum value.
    * `step`: Step size.
    * `on_value`: Callback to call when the value changes.
    * `thumb_label`: Show a thumb label when sliding (True), always ("always"), or never (False).
    * `disabled`: Whether the slider is disabled.
    """

    def set_value_cast(value):
        if on_value is None:
            return
        on_value(int(value))

    return rv.Slider(
        v_model=value,
        on_v_model=set_value_cast,
        label=label,
        min=min,
        max=max,
        step=step,
        thumb_label=thumb_label,
        dense=False,
        hide_details=True,
        disabled=disabled,
    )


@solara.value_component(None)
def SliderRangeInt(
    label: str,
    value: Tuple[int, int] = (1, 3),
    min: int = 0,
    max: int = 10,
    step: int = 1,
    on_value: Callable[[Tuple[int, int]], None] = None,
    thumb_label=True,
    disabled: bool = False,
) -> reacton.core.ValueElement[ipyvuetify.RangeSlider, Tuple[int, int]]:
    """Slider for controlling a range of integer values.

    ## Arguments
    * `label`: Label to display next to the slider.
    * `value`: The currently selected value.
    * `min`: Minimum value.
    * `max`: Maximum value.
    * `step`: Step size.
    * `on_value`: Callback to call when the value changes.
    * `thumb_label`: Show a thumb label when sliding (True), always ("always"), or never (False).
    * `disabled`: Whether the slider is disabled.
    """

    def set_value_cast(value):
        if on_value is None:
            return
        v1, v2 = value
        on_value((int(v1), int(v2)))

    return cast(
        reacton.core.ValueElement[ipyvuetify.RangeSlider, Tuple[int, int]],
        rv.RangeSlider(
            v_model=value,
            on_v_model=set_value_cast,
            label=label,
            min=min,
            max=max,
            step=step,
            thumb_label=thumb_label,
            dense=False,
            hide_details=True,
            disabled=disabled,
        ),
    )


@solara.value_component(float)
def SliderFloat(
    label: str,
    value: float = 0,
    min: float = 0,
    max: float = 10.0,
    step: float = 0.1,
    on_value: Callable[[float], None] = None,
    thumb_label=True,
    disabled: bool = False,
):
    """Slider for controlling a float value.

    ## Arguments
    * `label`: Label to display next to the slider.
    * `value`: The current value.
    * `min`: The minimum value.
    * `max`: The maximum value.
    * `step`: The step size.
    * `on_value`: Callback to call when the value changes.
    * `thumb_label`: Show a thumb label when sliding (True), always ("always"), or never (False).
    * `disabled`: Whether the slider is disabled.
    """

    def set_value_cast(value):
        if on_value is None:
            return
        on_value(float(value))

    return rv.Slider(
        v_model=value,
        on_v_model=set_value_cast,
        label=label,
        min=min,
        max=max,
        step=step,
        thumb_label=thumb_label,
        dense=False,
        hide_details=True,
        disabled=disabled,
    )


@solara.value_component(None)
def SliderRangeFloat(
    label: str,
    value: Tuple[float, float] = (1.0, 3.0),
    min: float = 0.0,
    max: float = 10.0,
    step: float = 0.1,
    on_value: Callable[[Tuple[float, float]], None] = None,
    thumb_label=True,
    disabled: bool = False,
) -> reacton.core.ValueElement[ipyvuetify.RangeSlider, Tuple[float, float]]:
    """Slider for controlling a range of float values.

    ## Arguments
    * `label`: Label to display next to the slider.
    * `value`: The current value.
    * `min`: The minimum value.
    * `max`: The maximum value.
    * `step`: The step size.
    * `on_value`: Callback to call when the value changes.
    * `thumb_label`: Show a thumb label when sliding (True), always ("always"), or never (False).
    * `disabled`: Whether the slider is disabled.
    """

    def set_value_cast(value):
        if on_value is None:
            return
        v1, v2 = value
        on_value((float(v1), float(v2)))

    return cast(
        reacton.core.ValueElement[ipyvuetify.RangeSlider, Tuple[float, float]],
        rv.RangeSlider(
            v_model=value,
            on_v_model=set_value_cast,
            label=label,
            min=min,
            max=max,
            step=step,
            thumb_label=thumb_label,
            dense=False,
            hide_details=True,
            disabled=disabled,
        ),
    )


@solara.value_component(None)
def SliderValue(
    label: str,
    value: T,
    values: List[T],
    on_value: Callable[[T], None] = None,
    disabled: bool = False,
) -> reacton.core.ValueElement[ipyvuetify.Slider, T]:
    """Slider for selecting a value from a list of values.

    ## Arguments
    * `label`: Label to display next to the slider.
    * `value`: The currently selected value.
    * `values`: List of values to select from.
    * `on_value`: Callback to call when the value changes.
    * `disabled`: Whether the slider is disabled.

    """
    index, set_index = solara.use_state(values.index(value), key="index")

    def on_index(index):
        set_index(index)
        value = values[index]
        if on_value:
            on_value(value)

    return cast(
        reacton.core.ValueElement[ipyvuetify.Slider, T],
        rv.Slider(
            v_model=index,
            on_v_model=on_index,
            ticks=True,
            tick_labels=values,
            label=label,
            min=0,
            max=len(values) - 1,
            dense=False,
            hide_details=True,
            disabled=disabled,
        ),
    )


class DateSliderWidget(ipyvue.VueTemplate):
    template_file = os.path.realpath(os.path.join(os.path.dirname(__file__), "slider_date.vue"))

    min = traitlets.CFloat(0).tag(sync=True)
    days = traitlets.CFloat(0).tag(sync=True)
    value = traitlets.Any(0).tag(sync=True)

    label = traitlets.Unicode("").tag(sync=True)
    disabled = traitlets.Bool(False).tag(sync=True)


@solara.value_component(date)
def SliderDate(
    label: str,
    value: date = date(1981, 7, 28),
    min: date = date(1981, 1, 1),
    max: date = date(3000, 12, 30),
    on_value: Callable[[date], None] = None,
    disabled: bool = False,
):
    """Slider for controlling a date value.

    ## Arguments
    * `label`: Label to display next to the slider.
    * `value`: The current value.
    * `min`: The minimum value.
    * `max`: The maximum value.
    * `on_value`: Callback to call when the value changes.
    * `disabled`: Whether the slider is disabled.
    """

    def format(d: date):
        return float(datetime(d.year, d.month, d.day).timestamp())

    dt_min = format(min)
    delta: timedelta = max - min
    days = delta.days

    delta_value: timedelta = value - min
    days_value = delta_value.days
    if days_value < 0:
        days_value = 0

    def set_value_cast(value):
        date = min + timedelta(days=value)
        if on_value:
            on_value(date)

    return DateSliderWidget.element(label=label, min=dt_min, days=days, on_value=set_value_cast, value=days_value, disabled=disabled)


FloatSlider = SliderFloat
IntSlider = SliderInt
ValueSlider = SliderValue
DateSlider = SliderDate

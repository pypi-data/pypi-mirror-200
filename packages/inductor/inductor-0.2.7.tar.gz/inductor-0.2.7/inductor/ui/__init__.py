# Copyright 2022 Inductor, Inc.

"""Abstractions for constructing interactive web UIs in Python."""

# pylint: disable=redefined-builtin

import base64
import contextlib
import contextvars
import copy
import datetime
import inspect
import io
import json
import os
from types import TracebackType
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union
from typing_extensions import get_args, Literal

import numpy as np
import pandas as pd
from PIL import Image
import plotly

from inductor.data.table import table

Number = Union[int, float]


def frontend_assets_dir_path() -> str:
    """Returns path to directory containing production-built frontend assets."""
    return os.path.join(os.path.dirname(__file__), "frontend", "build")


def html_scaffold() -> str:
    """Returns HTML scaffold for the abstractions below."""
    index_html_path = os.path.join(frontend_assets_dir_path(), "index.html")
    with open(index_html_path) as f:
        return f.read()


# Map from element IDs to corresponding element values in currently executing
# context.
element_values: contextvars.ContextVar[Dict[str, Any]] = contextvars.ContextVar(
    "element_values", default={})


class _Element:
    """A UI element."""

    def __init__(
        self,
        tag_name: str,
        props: Dict[str, Any],
        children: Optional[List[Union[str, "_Element"]]] = None):
        """Constructs a new _Element.

        Args:
            tag_name: This element's JSX tag name.
            props: Props to be passed to underlying React element or component.
                The values in this dictionary must be JSON-serializable.
            children: This element's children, if any.
        """
        if children is None:
            children = []
        elif not isinstance(children, list):
            raise TypeError(f"children ({children}) must be a list, or None.")
        self._tag_name = tag_name
        self._props = props
        self._children = children

    def append_child(self, child: Union[str, "_Element"]):
        """Appends child to this element's children.

        Args:
            child: String or element to be appended to this element's children.
        """
        if self._children is None:
            self._children = []
        self._children.append(child)

    def to_json_dict(self) -> Dict[str, Any]:
        """Returns a JSON-serializable representation of this element.

        In particular, the returned Dict can be passed directly to json.dumps().
        """
        return {
            "t": self._tag_name,
            "p": self._props,
            "c": [
                e if isinstance(e, str) else e.to_json_dict()
                for e in self._children]
        }

    @property
    def tag_name(self) -> str:
        """Returns tag_name of this element."""
        return self._tag_name

    @property
    def props(self) -> Dict[str, Any]:
        """Returns props of this element."""
        return self._props


class DeferredElement:
    """A UI element whose display has been deferred."""

    def __init__(
        self,
        container_stack: "_ContainerStack",
        element: _Element,
        id: str,
        get_value: Callable[[Tuple[bool, Any]], Any]):
        """Constructs a new DeferredElement.
        
        Args:
            container_stack: The container stack onto which to append the
                element.
            element: The element to be deferred.
            id: The id of the element to be deferred.
            get_value: A function that returns the element's current value,
                given a tuple as returned by _ContainerStack._append().
        """
        self._container_stack = container_stack
        self._element = element
        self._id = id
        self._get_value = get_value

    def display(self):
        """Appends this element to the page."""
        # pylint: disable-next=protected-access
        self._container_stack._append(self._element, self._id)

    @property
    def value(self) -> Any:
        """Returns the element's current value."""
        # pylint: disable=protected-access
        return self._get_value(
            (self._id in self._container_stack._element_values,
             self._container_stack._element_values.get(self._id)))


class FormattedText(_Element):
    """A formatted text segment."""

    def __init__(self):
        """Constructs a new FormattedText."""
        super().__init__("FormattedText", {}, [])

    def __add__(self, other: Union[str, "FormattedText"]) -> "FormattedText":
        """Concatenates this FormattedText with another FormattedText or string.

        Args:
            other: Another FormattedText or string to be concatenated with this
                FormattedText.

        Returns:
            A new FormattedText instance containing the concatenation of this
            FormattedText with other.
        """
        if not isinstance(other, str) and not isinstance(other, FormattedText):
            raise TypeError("FormattedText can only be concatenated with "
                            "another FormattedText or a string")
        formatted_text = FormattedText()
        for child in self._children:
            formatted_text.append_child(child)
        formatted_text.append_child(other)
        return formatted_text

    def _append(
        self,
        text: str,
        link_url: Optional[str] = None,
        link_styled: bool = True,
        link_hot_keys: Optional[str] = None,
        bold: bool = False,
        italics: bool = False,
        color: Optional[Literal["gray", "grey", "blue", "green", "yellow",
                                "red"]] = None,
        badge: Union[bool, Literal["gray", "grey", "blue", "green", "yellow",
                                    "red"]] = False) -> "FormattedText":
        """Appends a text sub-segment based on arguments.

        Args:
            text: The text to be formatted.
            link_url: If provided, then the text will be formatted as a link
                referencing this URL.
            link_styled: If link_url is provided and link_styled is True, then
                renders link with underline and color change upon being visited
                (otherwise renders link without underline or color change upon
                being visited).  Ignored if link_url is not provided.
            link_hot_keys: Optional keyboard shortcut that can be used to
                navigate to link_url (e.g., "1", "command+g").  Ignored if
                link_url is not provided.
            bold: If True, then text is formatted in boldface.
            italics: If True, then text is formatted in italics.
            color: Optionally, color for text.
            badge: If True, then text is formatted as a badge with a default
                background color.  If a string is provided, then text is
                formatted as a badge with specified background color.

        Returns:
            This FormattedText instance with formatted text appended.
        """
        props = {}
        props["bold"] = bold
        props["italic"] = italics
        if color is not None:
            props["color"] = color
        element = _Element("FormattedTextSpan", props, [text])
        if link_url is not None:
            link_props = {"href": link_url, "simple": not link_styled}
            if link_hot_keys is not None:
                link_props["hotKeys"] = link_hot_keys
            element = _Element("Link", link_props, [element])
        if badge:
            badge_props = {}
            if isinstance(badge, str):
                badge_props["color"] = badge
            self.append_child(_Element("Badge", badge_props, [element]))
        else:
            self.append_child(element)
        return self

    def _unstyle_links(self) -> "FormattedText":
        """Makes all children links unstyled.

        Returns:
            This FormattedText instance with all links rendered without
            underline or color change upon being visited.
        """
        # pylint: disable=protected-access
        def unstyle_children_links(children: List[TextLike]):
            for child in children:
                if isinstance(child, _Element):
                    if child.tag_name == "Link":
                        child._props["simple"] = True
                    elif isinstance(child, FormattedText):
                        child._unstyle_links()
                    else:
                        unstyle_children_links(child._children)
        unstyle_children_links(self._children)
        # pylint: enable=protected-access
        return self

    def copy(self) -> "FormattedText":
        """Returns a copy of this FormattedText."""
        return copy.deepcopy(self)


# Type for entities that can be displayed inline like text.
TextLike = Union[str, FormattedText]


def format(
    text: str,
    *,
    link_url: Optional[str] = None,
    link_styled: bool = True,
    link_hot_keys: Optional[str] = None,
    bold: bool = False,
    italics: bool = False,
    color: Optional[Literal["gray", "grey", "blue", "green", "yellow",
                            "red"]] = None,
    badge: Union[bool, Literal["gray", "grey", "blue", "green", "yellow",
                                "red"]] = False
) -> FormattedText:
    """Formats text for display as specified by the given arguments.

    The returned FormattedText object can be passed to various Page functions
    (such as print() and heading()) for display.  Strings and other
    FormattedText instances can be concatenated to the returned FormattedText
    instance using the `+` operator.

    Args:
        text: The text to be formatted.
        link_url: If provided, then the text will be formatted as a link
            referencing this URL.
        link_styled: If link_url is provided and link_styled is True, then
            renders link with underline and color change upon being visited
            (otherwise renders link without underline or color change upon
            being visited).  Ignored if link_url is not provided.
        link_hot_keys: Optional keyboard shortcut that can be used to navigate
            to link_url (e.g., "1", "command+g").  Ignored if link_url is not
            provided.
        bold: If True, then text is formatted in boldface.
        italics: If True, then text is formatted in italics.
        color: Optionally, color for text.
        badge: If True, then text is formatted as a badge with a default
            background color.  If a string is provided, then text is formatted
            as a badge with specified background color.

    Returns:
        A FormattedText instance as specified by the given arguments.
    """
    # pylint: disable-next=protected-access
    return FormattedText()._append(text, link_url, link_styled, link_hot_keys,
                                   bold, italics, color, badge)


class ContainerStackContextManager(contextlib.AbstractContextManager):
    """Context manager for a nested container on a container stack.

    Pushes a container element onto the underlying container stack on entry,
    and pops the topmost container in the underlying container stack (which
    should be the previously pushed container element) on exit.
    """

    def __init__(
        self, container_element: _Element, container_stack: "_ContainerStack",
        append_element: bool = True):
        """Initializes this ContainerStackContextManager.

        Args:
            container_element: The container element to be pushed onto the
                stack on context entry.
            container_stack: The container stack onto which to push and from
                which to pop container_element.
            append_element: If True, container_element will be appended as a
                child of the first element in the stack (in addition to being
                pushed onto the stack); otherwise it will only be pushed onto
                the stack.  Defaults to True.
        """
        self._container_element = container_element
        self._container_stack = container_stack
        self._append_element = append_element

    def __enter__(self):
        """Pushes container element passed to constructor onto the stack."""
        if self._append_element:
            self._container_stack._append(self._container_element)
        self._container_stack._stack.append(self._container_element)

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]) -> bool:
        """Pops the topmost container in the underlying container stack.

        (This topmost container element should be the container element
        originally passed to the constructor).

        Returns:
            False, indicating that any exceptions raised in the execution
            context should be propagated.
        """
        if self._container_stack._stack[-1] is not self._container_element:
            raise RuntimeError(
                "Encountered unexpected container stack state: topmost "
                "container on context manager exit is not the same as "
                "container pushed on context manager entry.")
        self._container_stack._stack.pop()
        return False


class ModalContextManager(ContainerStackContextManager):
    """Context manager for a modal nested on a container stack.

    Pushes a modal component onto the underlying container stack on entry,
    and pops the topmost container in the underlying container stack (which
    should be the previously pushed modal component) on exit.
    """

    def __init__(
        self, props: Dict[str, Any], container_stack: "_ContainerStack"):
        """Initializes this ModalContextManager.

        Args:
            props: Props to be passed to underlying Modal React component. Props
                must include an "id" key.  The values in this dictionary must be
                JSON-serializable.
            container_stack: The container stack onto which to push and from
                which to pop the Modal component.
        """
        modal_element = _Element("Modal", props.copy())
        super().__init__(modal_element, container_stack)
        self._modal_element = modal_element
        self._id = props["id"]
        _, self._toggler = self._container_stack._append(
            self._modal_element, self._id)

    def __enter__(self) -> "ModalContextManager":
        """Pushes modal element onto the stack.

        Returns:
            `self`.
        """
        self._container_stack._stack.append(self._modal_element)
        return self

    def _trigger_state_update(self):
        """Triggers update of modal's open state."""
        self._modal_element.props["toggler"] = not self._toggler

    def _open(self):
        """Opens modal."""
        self._trigger_state_update()
        self._modal_element.props["isOpen"] = True

    def close(self):
        """Closes modal."""
        self._trigger_state_update()
        self._modal_element.props["isOpen"] = False


class _ContainerStack:
    """A stack of nested containers for UI elements.

    UI elements can be appended to the topmost container in the stack,
    and additional nested containers can be pushed onto the top of
    the stack.
    """

    def __init__(self, stack: List[_Element], element_ids: Set[str]):
        """Constructs a new _ContainerStack.

        Args:
            stack: This _ContainerStack's underlying stack of container
                elements.  Will be modified in place.  Must have length >= 1.
                Nested containers will be appended to this list (as well as to
                the children of the prior element in the list), and
                non-nested-container elements will be appended to the
                children of the final element in this list.  If length of stack
                is > 1, then each element in stack should be a child of the
                element that precedes it in stack.
            element_ids: Set of existing element IDs.  Will be modified in
                place: this _ContainerStack will add the IDs of new elements
                appended to it to this set.  Additionally, this _ContainerStack
                will not permit adding any new elements having IDs that already
                exist in this set.
        """
        if not stack:
            raise ValueError("stack must contain at least one element.")

        self._stack = stack
        self._element_ids = element_ids
        self._element_values = element_values.get({})

    def to_element(self) -> _Element:
        """Returns this _ContainerStack's root _Element."""
        return self._stack[0]

    def _append(
        self, element: _Element, id: Optional[str] = None) -> Tuple[bool, Any]:
        """Appends element to the children of this stack's topmost container.

        Args:
            element: Element to append.
            id: Optionally, a unique id for element.

        Returns:
            A tuple containing the following two values:
            - True if id is non-None and present as a key in
              self._element_values. Otherwise, False.
            - Value associated with id in self._element_values, if id is
              non-None and present as a key in self._element_values.
              Otherwise, None.
        """
        if id is not None and id in self._element_ids:
            raise ValueError(
                f"An element having given id ({id}) already exists.")
        if (self._stack[-1].tag_name == "Tabs"
                and element.tag_name != "Tab"):
            raise ValueError("Only a tab() can be directly added to a page "
                             "within a tabs context.")
        if (element.tag_name == "Tab"
                and self._stack[-1].tag_name != "Tabs"):
            raise ValueError("A tab can only be appended within a tabs() "
                             "context.")
        if (self._stack[-1].tag_name == "Columns"
                and element.tag_name != "Column"):
            raise ValueError("Only a column() can be directly added to a page "
                             "within a columns context.")
        if (element.tag_name == "Column"
                and self._stack[-1].tag_name != "Columns"):
            raise ValueError("A column can only be appended within a columns() "
                             "context.")
        self._stack[-1].append_child(element)
        if id is None:
            return (False, None)
        else:
            self._element_ids.add(id)
            return (id in self._element_values, self._element_values.get(id))

    def format(
        self,
        text: str,
        *,
        link_url: Optional[str] = None,
        link_styled: bool = True,
        link_hot_keys: Optional[str] = None,
        bold: bool = False,
        italics: bool = False,
        color: Optional[Literal["gray", "grey", "blue", "green", "yellow",
                                "red"]] = None,
        badge: Union[bool, Literal["gray", "grey", "blue", "green", "yellow",
                                   "red"]] = False
    ) -> FormattedText:
        """Formats text for display as specified by the given arguments.

        The returned FormattedText object can be passed to various Page
        functions (such as print() and heading()) for display.  Strings and
        other FormattedText instances can be concatenated to the returned
        FormattedText instance using the `+` operator.

        Args:
            text: The text to be formatted.
            link_url: If provided, then the text will be formatted as a link
                referencing this URL.
            link_styled: If link_url is provided and link_styled is True, then
                renders link with underline and color change upon being visited
                (otherwise renders link without underline or color change upon
                being visited).  Ignored if link_url is not provided.
            link_hot_keys: Optional keyboard shortcut that can be used to
                navigate to link_url (e.g., "1", "command+g").  Ignored if
                link_url is not provided.
            bold: If True, then text is formatted in boldface.
            italics: If True, then text is formatted in italics.
            color: Optionally, color for text.
            badge: If True, then text is formatted as a badge with a default
                background color.  If a string is provided, then text is
                formatted as a badge with specified background color.

        Returns:
            A FormattedText instance as specified by the given arguments.
        """
        # pylint: disable-next=protected-access
        return FormattedText()._append(text, link_url, link_styled,
                                       link_hot_keys, bold, italics, color,
                                       badge)

    def heading(self, content: TextLike, *, level: int = 1):
        """Appends a heading having given content (e.g., text).

        Args:
            content: Heading content (e.g., text).
            level: Heading level.  Must be an integer in [1, 6].
        """
        if not isinstance(level, int) or not 1 <= level <= 6:
            raise ValueError("level must be an integer in [1, 6].")
        self._append(_Element(f"H{level}", {}, [content]))

    def subheading(self, content: TextLike):
        """Alias for heading(content, level=2)."""
        self.heading(content, level=2)

    def subsubheading(self, content: TextLike):
        """Alias for heading(content, level=3)."""
        self.heading(content, level=3)

    def print(self, content: Any):
        """Appends given content (e.g., text).

        Args:
            content: Body content (e.g., text) to append.  If of type
                TextLike, then will be appended as is; otherwise,
                str(content) will be appended.
        """
        if not any(isinstance(content, t) for t in get_args(TextLike)):
            content = str(content)
        self._append(_Element("BodyText", {}, [content]))

    def divider(self):
        """Appends a horizontal divider."""
        self._append(_Element("HR", {}))

    def confetti(self, emojis: Optional[List[str]] = None):
        """Triggers a confetti animation.

        Args:
            emojis: Optionally, a list of emojis to use as confetti.  If None,
                then the confetti consists of "standard" multicolored shapes.
        """
        props = {"emojis": emojis} if emojis else {}
        self._append(_Element("Confetti", props))

    def markdown(self, markdown_text: str):
        """Appends rendering of given Markdown text.

        Args:
            markdown_text: Markdown text to be rendered and appended.
                Whitespace is trimmed via inspect.cleandoc(): "All leading
                whitespace is removed from the first line. Any leading
                whitespace that can be uniformly removed from the second line
                onwards is removed. Empty lines at the beginning and end are
                subsequently removed. Also, all tabs are expanded to spaces."
        """
        self._append(_Element(
            "Markdown", {}, [inspect.cleandoc(markdown_text)]))

    def _plotly_layout(
        self,
        title: Optional[str],
        xlabel: Optional[str],
        ylabel: Optional[str]) -> Dict:
        """Returns layout Dict for a Plotly plot.

        Args:
            title: Optional plot title text.
            xlabel: Optional X axis label text.
            ylabel: Optional Y axis label text.
        """
        layout = {
            "margin": {"b": 35, "t": 5, "l": 45, "r": 35}
        }
        if title:
            layout["margin"]["t"] = 42
            layout["title"] = {
                "text": title,
                "yref": "paper",
                "y": 1,
                "yanchor": "bottom",
                "pad": {"b": 15}
            }
        if xlabel:
            layout["margin"]["b"] = 60
            layout["xaxis"] = {"title": {
                "text": xlabel,
                "standoff": 15
            }}
        if ylabel:
            layout["margin"]["l"] = 65
            layout["yaxis"] = {"title": {
                "text": ylabel,
                "standoff": 10
            }}
        return layout

    def _plotly_config(self) -> Dict:
        """Returns config Dict for a Plotly plot."""
        return {"displayModeBar": False}

    def _plotly_style(self) -> Dict:
        """Returns style Dict for a React Plotly plot."""
        return {
            "position": "relative",  # React Plotly default setting
            "display": "inline-block",  # React Plotly default setting
            "max-width": "700px"
        }

    def line_plot(
        self, x: List[Number], y: List[Number], *, title: Optional[str] = None,
        xlabel: Optional[str] = None, ylabel: Optional[str] = None):
        """Appends a line plot.

        Args:
            x: X values.  Must have same length as y.
            y: Y values.  Must have same length as x.
            title: Optional plot title.
            xlabel: Optional X axis label.
            ylabel: Optional Y axis label.
        """
        if len(x) != len(y):
            raise ValueError(
                f"x (length {len(x)}) and y (length {len(y)}) "
                "must have the same length.")
        self._append(_Element("PlotlyPlot", {
            "data": [{"x": x, "y": y, "type": "scatter", "mode": "lines"}],
            "layout": self._plotly_layout(
                title=title, xlabel=xlabel, ylabel=ylabel),
            "config": self._plotly_config(),
            "style": self._plotly_style()
        }))

    def scatter_plot(
        self, x: List[Number], y: List[Number], *, title: Optional[str] = None,
        xlabel: Optional[str] = None, ylabel: Optional[str] = None):
        """Appends a scatter plot.

        Args:
            x: X values.  Must have same length as y.
            y: Y values.  Must have same length as x.
            title: Optional plot title.
            xlabel: Optional X axis label.
            ylabel: Optional Y axis label.
        """
        if len(x) != len(y):
            raise ValueError(
                f"x (length {len(x)}) and y (length {len(y)}) "
                "must have the same length.")
        self._append(_Element("PlotlyPlot", {
            "data": [{"x": x, "y": y, "type": "scatter", "mode": "markers"}],
            "layout": self._plotly_layout(
                title=title, xlabel=xlabel, ylabel=ylabel),
            "config": self._plotly_config(),
            "style": self._plotly_style()
        }))

    def bar_chart(
        self, categories: List[str], values: List[Number],
        *, title: Optional[str] = None, categories_label: Optional[str] = None,
        values_label: Optional[str] = None, horizontal: bool = False):
        """Appends a bar chart.

        Args:
            categories: Names of categories.  Must have same length as values.
            values: Values for all categories.  Must have same length as
                categories.
            title: Optional plot title.
            categories_label: Optional category axis label.
            values_label: Optional value axis label.
            horizontal: If True, displays a horizontal bar chart (i.e., having
                horizontal bars with values on the X axis).  Otherwise, displays
                a standard vertical bar chart (i.e., having vertical bars with
                values on the Y axis).
        """
        if len(categories) != len(values):
            raise ValueError(
                f"categories (length {len(categories)}) and values "
                f"(length {len(values)}) must have the same length.")
        if horizontal:
            self._append(_Element("PlotlyPlot", {
                "data": [{
                    "x": values, "y": categories,
                    "type": "bar", "orientation": "h"}],
                "layout": self._plotly_layout(
                    title=title, xlabel=values_label, ylabel=categories_label),
                "config": self._plotly_config(),
                "style": self._plotly_style()
            }))
        else:
            self._append(_Element("PlotlyPlot", {
                "data": [{"x": categories, "y": values, "type": "bar"}],
                "layout": self._plotly_layout(
                    title=title, xlabel=categories_label, ylabel=values_label),
                "config": self._plotly_config(),
                "style": self._plotly_style()
            }))

    def histogram(
        self, values: List[Number], *, title: Optional[str] = None,
        xlabel: Optional[str] = None, ylabel: Optional[str] = None):
        """Appends a histogram.

        Args:
            values: Values to be histogrammed; will be binned automatically.
            title: Optional plot title.
            xlabel: Optional X axis label.
            ylabel: Optional Y axis label.
        """
        self._append(_Element("PlotlyPlot", {
            "data": [{"x": values, "type": "histogram"}],
            "layout": self._plotly_layout(
                title=title, xlabel=xlabel, ylabel=ylabel),
            "config": self._plotly_config(),
            "style": self._plotly_style()
        }))

    def plotly_figure(
        self, fig: plotly.graph_objects.Figure, *,
        config: Optional[Dict] = None):
        """Appends the given Plotly figure.

        Arbitrary Plotly figures can, for example, be created using Plotly
        Express or Plotly's graph objects API.

        Args:
            fig: The Plotly figure to be appended.
            config: Optional [additional configuration options](https://plotly.com/python/configuration-options/) # pylint: disable=line-too-long
                for figure behavior, as would be passed to the config parameter
                of plotly.graph_objects.Figure.show().
        """
        if not isinstance(fig, plotly.graph_objects.Figure):
            raise TypeError(f"Unsupported fig type: {type(fig)}")

        fig_copy = plotly.graph_objects.Figure(fig)
        margin = self._plotly_layout(fig.layout.title.text,
                                     fig.layout.xaxis.title.text,
                                     fig.layout.yaxis.title.text).get("margin")
        if margin is not None:
            if (fig.data is not None and isinstance(fig.data[0].type, str)
                    and fig.data[0].type == "parcoords"):
                margin.update({"t": 90})

            margin.update(fig.layout.margin.to_plotly_json())
            fig_copy.update_layout(margin=margin)

        # Plotly dicts are not directly serializable to json. This dict is
        # created from plotly to_json() str
        fig_dict = json.loads(fig_copy.to_json())
        fig_dict["config"] = self._plotly_config()
        if config is not None:
            fig_dict["config"].update(config)
        max_width = {
            "max-width": fig.layout.width
        } if fig.layout.width is not None else {}
        fig_dict["style"] = {**self._plotly_style(), **max_width}

        self._append(_Element("PlotlyPlot", fig_dict))

    def image(
        self,
        img: Union[str, Image.Image, np.ndarray, bytes],
        *,
        max_width: Optional[Union[int, float]] = None,
        max_height: Optional[int] = None):
        """Appends an image.

        Args:
            img: The image to be displayed.  If `str`, must be a URL for an
                image. If `np.ndarray`, then should be convertible to
                PIL.Image.Image via its [fromarray()](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.fromarray) # pylint: disable=line-too-long
                method. If `bytes`, then should be the contents of an image
                file (e.g., as would be produced by PIL.Image.Image.save()).
            max_width: Optional maximum width for image; the image will be
                resized as necessary to respect this argument.  Must be
                positive if provided. If > 1, then interpreted as the maximum
                display width for the image in pixels. If <= 1, then
                interpreted as the maximum display width for the image as a
                fraction of its container's width.
            max_height: Optional maximum height for image, in pixels; the
                image will be resized as necessary to respect this argument.
                Must be positive if provided.
        """

        if (max_width is not None and max_width <= 0):
            raise ValueError("max_width must be positive.")
        if (max_height is not None and max_height <= 0):
            raise ValueError("max_height must be positive.")

        props = {}
        pil_img = None

        if isinstance(img, str):
            props["src"] = img
        elif isinstance(img, Image.Image):
            pil_img = img.copy()
            pil_img.format = img.format
        elif isinstance(img, np.ndarray):
            pil_img = Image.fromarray(img)
        elif isinstance(img, bytes):
            pil_img = Image.open(io.BytesIO(img))
        else:
            raise TypeError(f"Unsupported img type: {type(img)}")

        if pil_img is not None:
            if ((max_width is not None and pil_img.width > max_width > 1) or
                (max_height is not None and pil_img.height > max_height)):
                width = (max_width if max_width is not None and max_width > 1
                         else pil_img.width)
                height = (max_height if max_height is not None
                          else pil_img.height)
                pil_img.thumbnail((width, height), Image.Resampling.LANCZOS)

            buffer = io.BytesIO()
            if pil_img.format is None:
                pil_img.format = "PNG"
            pil_img.save(buffer, format=pil_img.format)
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            img_mime = Image.MIME[pil_img.format]
            props["src"] = f"data:{img_mime};base64,{img_base64}"

        style = {}
        if max_width is not None:
            if max_width > 1:
                style["maxWidth"] = str(max_width) + "px"
            else:
                style["maxWidth"] = str(max_width * 100) + "%"
        if max_height is not None:
            style["maxHeight"] = str(max_height) + "px"

        if style:
            props["style"] = style

        self._append(
            _Element("figure", {"style": {
                "maxWidth": "100%"
            }}, [_Element("img", props)]))

    def notify(
        self,
        content: TextLike,
        *,
        location: Optional[Literal["top_left", "top_center",
                                    "top_right", "bottom_left",
                                    "bottom_center", "bottom_right"]] = None,
        color: Literal["blue", "green", "yellow", "red"] = "blue",
        auto_hide_secs: Optional[int] = None):
        """Displays a notification having given content.

        Notifications are colored boxes which contain and highlight the given
        content (e.g., text, links), and that are either directly appended to
        the page or, if an explicit location is provided, overlaid on the page.
        They are often used to give users feedback after they take an action
        (e.g., "Settings saved!").

        Args:
            content: The content to be displayed within the notification box.
            location: The location at which the notification box should be
                displayed.  If None, then the notification box is appended
                directly to the page; otherwise, the notification box is
                overlaid on the page at the specified location.
            color: The background color for the notification box.
            auto_hide_secs: Optional number of seconds after which to
                automatically hide the notification box.  Must be positive if
                provided.
        """
        if auto_hide_secs is not None and auto_hide_secs < 1:
            raise ValueError("auto_hide_secs must be positive.")

        props = {"color": color}
        if location is not None:
            props["location"] = location
        if auto_hide_secs is not None:
            props["autoHideSecs"] = auto_hide_secs

        self._append(_Element("Notify", props, [content]))

    def code(
        self,
        content: str,
        *,
        lang: Optional[str] = None):
        """Displays given content as code.

        Args:
            content: The code to be displayed.  Whitespace is trimmed via
                inspect.cleandoc(): "All leading whitespace is removed from the
                first line. Any leading whitespace that can be uniformly removed
                from the second line onwards is removed. Empty lines at the
                beginning and end are subsequently removed. Also, all tabs are
                expanded to spaces."
            lang: Optionally, the name of the programming language to be used
                for syntax highlighting; see [list of available languages](https://github.com/react-syntax-highlighter/react-syntax-highlighter/blob/master/AVAILABLE_LANGUAGES_PRISM.MD). # pylint: disable=line-too-long
        """
        props = {}
        if lang is not None:
            props["language"] = lang
        self._append(_Element("Code", props, [inspect.cleandoc(content)]))

    def download(
        self,
        filename: str,
        content: Union[str, bytes, table.Table]):
        """Triggers download of a file containing content.

        If content is a Table, then its contents will automatically be
        converted to CSV format for download.

        Args:
            filename: Name for the file upon download.
            content: Content of the downloaded file.
        """
        props = {"filename": filename}
        if isinstance(content, table.Table):
            props["content"] = content.pandas_df().to_csv(index=False)
        elif isinstance(content, str):
            props["content"] = content
        elif isinstance(content, bytes):
            props["content"] = base64.b64encode(content).decode("utf-8")
            props["isBase64"] = True
        else:
            raise TypeError(f"Unsupported content type: {type(content)}")
        self._append(_Element("Download", props))

    def data_table(
        self,
        data: Union[table.Table, pd.DataFrame],
        *,
        out_of_row_count: Optional[int] = None,
        selectable: bool = False,
        id: Optional[str] = None,
        defer_display: bool = False
    ) -> Union[Optional[Dict[str, Any]], DeferredElement]:
        """Appends a data table.

        Args:
            data: The data to be displayed.
            out_of_row_count: Optionally, if data is a subset of a larger
                dataset, the total number of rows in the full dataset.
                If provided, then a "Displaying M out of N rows" note is
                displayed below the table.
            selectable: Enable interactively selecting individual rows in the
                data table?
            id: The data table's id within its Page; used only if selectable
                is True.  If selectable is True and id is not provided, then
                this data table's id is derived from the names of its columns.
                If selectable is True, then this table's id must be unique
                among the ids of data tables within this table's Page.
            defer_display: If False (the default), then this method appends the
                data table to the page and returns the currently selected row
                (if selectable is True).  If True, then this method does not
                itself append the data table to the page; rather, it returns an
                object whose `display()` method can subsequently be called to
                append the data table to the page, and whose `value` field
                provides the currently selected row (if selectable is True).

        Returns:
            If defer_display is False (the default):
                If selectable is True and a row has been selected, returns
                the contents of the currently selected row as a Dict mapping
                column name to column value.  Otherwise, returns None.

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this data table to the page, and whose `value` field
                provides the currently selected row, if selectable is True and
                a row has been selected (as would be returned if defer_display
                were False).
        """
        props = {}
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = data.pandas_df()
        # columnNames
        props["columnNames"] = list(df.columns)
        # columnTypes
        column_types = []
        for dtype in df.dtypes:
            if pd.api.types.is_numeric_dtype(dtype):
                column_types.append("numerical")
            else:
                column_types.append("string")
        props["columnTypes"] = column_types
        # rows
        rows = df.values.tolist()
        isnull = pd.isnull(df)
        for r, row in enumerate(rows):
            for c in range(len(row)):
                if isnull.iloc[r, c]:
                    row[c] = None
                elif column_types[c] == "string":
                    row[c] = str(row[c])
        props["rows"] = rows
        # Detect presence of long string values and update props["columnTypes"]
        # accordingly.  Also set props["maxTextLength"].
        props["maxTextLength"] = 70
        for i, column_type in enumerate(props["columnTypes"]):
            if column_type == "string":
                max_length = max(
                    len(row[i]) if row[i] else 0
                    for row in props["rows"])
                if max_length > props["maxTextLength"]:
                    props["columnTypes"][i] = "text"
        # outOfNumRows
        if out_of_row_count is not None:
            props["outOfNumRows"] = out_of_row_count
        # selectable
        props["selectable"] = selectable
        # id
        if selectable:
            if not id:
                id = ",".join(sorted(props["columnNames"]))
            id = "data_table:" + id
            props["id"] = id
        else:
            id = None
        def _get_value(values: Tuple[bool, Any]) -> Optional[Dict[str, Any]]:
            _, row = values
            return row if selectable else None
        element = _Element("DataTable", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            # Append to container
            return _get_value(self._append(element, id))

    def checkbox(
        self,
        label: Optional[str] = None,
        *,
        default_value: bool = False,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None,
        defer_display: bool = False) -> Union[bool, DeferredElement]:
        """Appends a checkbox and returns its current value.

        Args:
            label: The label to be displayed adjacent to the checkbox.  Must be
                provided if id is None, in which case label is used as this
                checkbox's id and must be unique among the ids of checkboxes
                in this container.
            default_value: The checkbox's initial default value (i.e., prior
                to user interaction with it).
            id: The checkbox's id within its Page.  Must be provided if label
                is None.  If provided, must be unique among the ids of
                checkboxes in this checkbox's Page; if not provided, then label
                is used as this checkbox's id.
            hot_keys: Optional keyboard shortcut that can be used to toggle this
                checkbox's value (e.g., "1", "command+g").
            defer_display: If False (the default), then this method appends the
                element to the page and returns its current value.  If True,
                then this method does not itself append the element to the page;
                rather, it returns an object whose `display()` method can
                subsequently be called to append the element to the page, and
                whose `value` field provides the element's current value.

        Returns:
            If defer_display is False (the default):
                default_value if the user has not interacted with this checkbox;
                otherwise, returns the value set by the user.

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this element to the page, and whose `value` field
                provides the current element value (as would be returned if
                defer_display were False).
        """
        if label is None and id is None:
            raise ValueError(
                "Both label and id are None; at least one must be provided.")
        id = "checkbox:" + (id if id is not None else label)
        props = {"id": id, "asToggle": False, "initialValue": default_value}
        if label is not None:
            props["label"] = label
        if hot_keys is not None:
            props["hotKeys"] = hot_keys
        def _get_value(values: Tuple[bool, Any]) -> bool:
            _, value = values
            return value if value is not None else default_value
        element = _Element("Checkbox", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            return _get_value(self._append(element, id))

    def toggle(
        self,
        label: Optional[str] = None,
        *,
        default_value: bool = False,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None,
        defer_display: bool = False) -> Union[bool, DeferredElement]:
        """Appends a toggle and returns its current value.

        Args:
            label: The label to be displayed adjacent to the toggle.  Must be
                provided if id is None, in which case label is used as this
                toggle's id and must be unique among the ids of toggles
                in this container.
            default_value: The toggle's initial default value (i.e., prior
                to user interaction with it).
            id: The toggle's id within its Page.  Must be provided if label
                is None.  If provided, must be unique among the ids of
                toggles in this toggle's Page; if not provided, then label is
                used as this toggle's id.
            hot_keys: Optional keyboard shortcut that can be used to toggle this
                toggle's value (e.g., "1", "command+g").
            defer_display: If False (the default), then this method appends the
                element to the page and returns its current value.  If True,
                then this method does not itself append the element to the page;
                rather, it returns an object whose `display()` method can
                subsequently be called to append the element to the page, and
                whose `value` field provides the element's current value.

        Returns:
            If defer_display is False (the default):
                default_value if the user has not interacted with this toggle;
                otherwise, returns the value set by the user.

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this element to the page, and whose `value` field
                provides the current element value (as would be returned if
                defer_display were False).
        """
        if label is None and id is None:
            raise ValueError(
                "Both label and id are None; at least one must be provided.")
        id = "toggle:" + (id if id is not None else label)
        props = {"id": id, "asToggle": True, "initialValue": default_value}
        if label is not None:
            props["label"] = label
        if hot_keys is not None:
            props["hotKeys"] = hot_keys
        def _get_value(values: Tuple[bool, Any]) -> bool:
            _, value = values
            return value if value is not None else default_value
        element = _Element("Checkbox", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            return _get_value(self._append(element, id))

    def date_picker(
        self,
        label: Optional[str] = None,
        *,  # all subsequent parameters are keyword-only
        default_value: Optional[Union[datetime.date, str]] = None,
        min: Optional[Union[datetime.date, str]] = None,
        max: Optional[Union[datetime.date, str]] = None,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None,
        defer_display: bool = False
    ) -> Union[Optional[datetime.date], DeferredElement]:
        """Appends a date picker and returns its current value.

        Args:
            label: The label to be displayed adjacent to the date picker.  Must
                be provided if id is None, in which case label is used as this
                date picker's id and must be unique among the ids of date
                pickers in this container.
            default_value: The date picker's initial default value (i.e., prior
                to user interaction with it).  If a string, must be in
                YYYY-MM-DD format.  If provided, must satisfy
                min <= default_value <= max if either min or max is provided.
            min: Optionally, the earliest date (inclusive) that can be selected.
                If a string, must be in YYYY-MM-DD format.
            max: Optionally, the latest date (inclusive) that can be selected.
                If a string, must be in YYYY-MM-DD format.
            id: The date picker's id within its Page.  Must be provided if
                label is None or if label is not unique among date picker
                labels in this date picker's Page.  If provided, must be unique
                among the ids of date pickers in this date picker's Page; if
                not provided, then label is used as this date picker's id.
            hot_keys: Optional keyboard shortcut that can be used to focus this
                date picker (e.g., "1", "Cmd+g").
            defer_display: If False (the default), then this method appends the
                element to the page and returns its current value.  If True,
                then this method does not itself append the element to the page;
                rather, it returns an object whose `display()` method can
                subsequently be called to append the element to the page, and
                whose `value` field provides the element's current value.

        Returns:
            If defer_display is False (the default):
                default_value if the user has not interacted with this date
                picker; otherwise, returns the value set by the user.

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this element to the page, and whose `value` field
                provides the current element value (as would be returned if
                defer_display were False).
        """
        if label is None and id is None:
            raise ValueError(
                "Both label and id are None; at least one must be provided.")
        id = "date_picker:" + (id if id is not None else label)
        props = {"id": id, "range": False}
        if min:
            if isinstance(min, str):
                # To ensure that min is well-formed
                min = datetime.date.fromisoformat(min)
            props["minDate"] = min.isoformat()
        if max:
            if isinstance(max, str):
                # To ensure that max is well-formed
                max = datetime.date.fromisoformat(max)
            props["maxDate"] = max.isoformat()
        if default_value:
            if isinstance(default_value, str):
                # To ensure that default_value is well-formed
                default_value = datetime.date.fromisoformat(default_value)
            if (min and default_value < min) or (max and default_value > max):
                raise ValueError(
                    "default_value must satisfy min <= default_value <= max.")
            props["initialValue"] = default_value.isoformat()
        if label is not None:
            props["label"] = label
        if hot_keys is not None:
            props["hotKeys"] = hot_keys
        def _get_value(values: Tuple[bool, Any]) -> Optional[datetime.date]:
            value_set, value = values
            if value_set:
                if value is None:
                    return None
                value = datetime.date.fromisoformat(value)
                if (min and value < min) or (max and value > max):
                    raise ValueError(
                        "Value received from frontend is unexpectedly outside "
                        "of the range given by min and/or max.")
                return value
            else:
                return default_value
        element = _Element("DatePicker", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            return _get_value(self._append(element, id))

    def date_range_picker(
        self,
        label: Optional[str] = None,
        *,  # all subsequent parameters are keyword-only
        default_value: Optional[
            Tuple[Union[datetime.date, str], Union[datetime.date, str]]] = None,
        min: Optional[Union[datetime.date, str]] = None,
        max: Optional[Union[datetime.date, str]] = None,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None,
        defer_display: bool = False
    ) -> Union[Optional[Tuple[datetime.date, datetime.date]], DeferredElement]:
        """Appends a date range picker and returns its current value.

        Args:
            label: The label to be displayed adjacent to the date range picker.
                Must be provided if id is None, in which case label is used as
                this date range picker's id and must be unique among the ids of
                date range pickers in this container.
            default_value: Optionally, a pair of dates giving the date range
                picker's initial default value (i.e., prior to user interaction
                with it).  If either date is a string, it must be in YYYY-MM-DD
                format.  If default_value is provided, then the first date must
                not be later than the second, and both dates must be >= min and
                <= max if either min or max is provided.
            min: Optionally, the earliest date (inclusive) that can be selected.
                If a string, must be in YYYY-MM-DD format.
            max: Optionally, the latest date (inclusive) that can be selected.
                If a string, must be in YYYY-MM-DD format.
            id: The date range picker's id within its Page.  Must be provided
                if label is None or if label is not unique among date range
                picker labels in this picker's Page.  If provided, must be
                unique among the ids of date range pickers in this picker's
                Page; if not provided, then label is used as this date range
                picker's id.
            hot_keys: Optional keyboard shortcut that can be used to focus this
                date range picker (e.g., "1", "Cmd+g").
            defer_display: If False (the default), then this method appends the
                element to the page and returns its current value.  If True,
                then this method does not itself append the element to the page;
                rather, it returns an object whose `display()` method can
                subsequently be called to append the element to the page, and
                whose `value` field provides the element's current value.

        Returns:
            If defer_display is False (the default):
                default_value if the user has not interacted with this date
                range picker; otherwise, returns the value set by the user.

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this element to the page, and whose `value` field
                provides the current element value (as would be returned if
                defer_display were False).
        """
        if label is None and id is None:
            raise ValueError(
                "Both label and id are None; at least one must be provided.")
        id = "date_range_picker:" + (id if id is not None else label)
        props = {"id": id, "range": True}
        if min:
            if isinstance(min, str):
                # To ensure that min is well-formed
                min = datetime.date.fromisoformat(min)
            props["minDate"] = min.isoformat()
        if max:
            if isinstance(max, str):
                # To ensure that max is well-formed
                max = datetime.date.fromisoformat(max)
            props["maxDate"] = max.isoformat()
        if default_value:
            start_date, end_date = default_value
            if isinstance(start_date, str):
                # To ensure that start_date is well-formed
                start_date = datetime.date.fromisoformat(start_date)
            if isinstance(end_date, str):
                # To ensure that end_date is well-formed
                end_date = datetime.date.fromisoformat(end_date)
            if start_date > end_date:
                raise ValueError(
                    "Within default_value, first date must not be later than "
                    "second date.")
            if (min and start_date < min) or (max and end_date > max):
                raise ValueError(
                    "Both dates in default_value must be >= min and <= max.")
            default_value = (start_date, end_date)
            props["initialValue"] = [d.isoformat() for d in default_value]
        if label is not None:
            props["label"] = label
        if hot_keys is not None:
            props["hotKeys"] = hot_keys
        def _get_value(
            values: Tuple[bool, Any]
        ) -> Optional[Tuple[datetime.date, datetime.date]]:
            value_set, value = values
            if value_set:
                if value is None:
                    return None
                start_date, end_date = [
                    datetime.date.fromisoformat(s) for s in value]
                if start_date > end_date:
                    raise ValueError(
                        "Start date received from frontend is unexpectedly "
                        "after end date.")
                if (min and start_date < min) or (max and end_date > max):
                    raise ValueError(
                        "Date range received from frontend is unexpectedly not "
                        "contained within range given by min and/or max.")
                return (start_date, end_date)
            else:
                return default_value
        element = _Element("DatePicker", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            return _get_value(self._append(element, id))

    def _append_select(
        self,
        values: List[str],
        *,  # all subsequent parameters are keyword-only
        multi: bool,
        default_value: Optional[Union[str, List[str]]] = None,
        label: Optional[str] = None,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None,
        defer_display: bool = False
    ) -> Union[Optional[Union[str, List[str]]], DeferredElement]:
        """Appends a (potentially multi) select and returns its current value.

        Args:
            values: The values among which to select.
            multi: Allow selecting more than one value?
            default_value: The select's initial default value (i.e., prior to
                user interaction with it).  Must be a string if multi is False;
                can be either a string or a list of strings if multi is True.
                Any values provided within default_value must be present in
                the values argument.
            label: The label to be displayed adjacent to the select.
            id: The select's id within its Page.  If id is not provided, then
                the select's id is derived from values, multi, and label.
                The select's id must be unique among all selects having the
                same value of multi in this select's Page.
            hot_keys: Optional keyboard shortcut that can be used to focus the
                select (e.g., "1", "Cmd+g").
            defer_display: If False (the default), then this method appends the
                element to the page and returns its current value.  If True,
                then this method does not itself append the element to the page;
                rather, it returns an object whose `display()` method can
                subsequently be called to append the element to the page, and
                whose `value` field provides the element's current value.

        Returns:
            If defer_display is False (the default):
                default_value if the user has not interacted with the select;
                otherwise, returns the value set by the user (a string if multi
                is False, otherwise a list of strings).

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this element to the page, and whose `value` field
                provides the current element value (as would be returned if
                defer_display were False).
        """
        id_prefix = ("multi" if multi else "") + "select:"
        if id is None:
            id = id_prefix + ",".join(values)
            if label is not None:
                id += ":" + label
        else:
            id = id_prefix + id
        props = {
            "id": id,
            "options": [{"value": v} for v in values],
            "multi": multi
        }
        values_set = set(values)
        if default_value:
            if isinstance(default_value, str):
                default_value = [default_value]
            if not multi and len(default_value) > 1:
                raise ValueError(
                    "default_value must contain only a single value if multi "
                    "is False.")
            if not all(v in values_set for v in default_value):
                raise ValueError(
                    "default_value must contain only values present in values "
                    "argument.")
            props["initialValue"] = [{"value": v} for v in default_value]
        if label is not None:
            props["label"] = label
        if hot_keys is not None:
            props["hotKeys"] = hot_keys
        def _get_value(
            values: Tuple[bool, Any]
        ) -> Optional[Union[str, List[str]]]:
            value_set, value = values
            if value_set:
                if value is None:
                    return None
                value = [v["value"] for v in value]
                if not all(v in values_set for v in value):
                    raise ValueError(
                        "Frontend unexpectedly returned a value not "
                        "present in the values argument.")
                if multi:
                    return value
                else:
                    if len(value) > 1:
                        raise ValueError(
                            "Frontend unexpectedly returned multiple selected "
                            "values (multi is False).")
                    return value[0] if value else None
            else:
                return (
                    default_value if multi or not default_value
                    else default_value[0])
        element = _Element("Select", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            return _get_value(self._append(element, id))

    def select(
        self,
        values: List[str],
        *,  # all subsequent parameters are keyword-only
        default_value: Optional[str] = None,
        label: Optional[str] = None,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None,
        defer_display: bool = False) -> Union[Optional[str], DeferredElement]:
        """Appends a dropdown select and returns its current value.

        Args:
            values: The values among which to select.
            default_value: The select's initial default value (i.e., prior to
                user interaction with it).  Any value provided must be present
                in the values argument.
            label: The label to be displayed adjacent to the select.
            id: The select's id within its Page.  If id is not provided, then
                the select's id is derived from values and label.  The select's
                id must be unique among all selects in this select's Page.
            hot_keys: Optional keyboard shortcut that can be used to focus the
                select (e.g., "1", "Cmd+g").
            defer_display: If False (the default), then this method appends the
                element to the page and returns its current value.  If True,
                then this method does not itself append the element to the page;
                rather, it returns an object whose `display()` method can
                subsequently be called to append the element to the page, and
                whose `value` field provides the element's current value.

        Returns:
            If defer_display is False (the default):
                default_value if the user has not interacted with the select;
                otherwise, returns the value set by the user.

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this element to the page, and whose `value` field
                provides the current element value (as would be returned if
                defer_display were False).
        """
        return self._append_select(
            values=values,
            multi=False,
            default_value=default_value,
            label=label,
            id=id,
            hot_keys=hot_keys,
            defer_display=defer_display)

    def multiselect(
        self,
        values: List[str],
        *,  # all subsequent parameters are keyword-only
        default_value: Optional[Union[str, List[str]]] = None,
        label: Optional[str] = None,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None,
        defer_display: bool = False
    ) -> Union[Optional[List[str]], DeferredElement]:
        """Appends a dropdown multiselect and returns its current value.

        Args:
            values: The values among which to select.
            default_value: The multiselect's initial default value (i.e., prior
                to user interaction with it).  Any values provided must be
                present in the values argument.
            label: The label to be displayed adjacent to the multiselect.
            id: The multiselect's id within its Page.  If id is not provided,
                then the multiselect's id is derived from values and label.  The
                multiselect's id must be unique among all multiselects in this
                multiselect's Page.
            hot_keys: Optional keyboard shortcut that can be used to focus the
                multiselect (e.g., "1", "Cmd+g").
            defer_display: If False (the default), then this method appends the
                element to the page and returns its current value.  If True,
                then this method does not itself append the element to the page;
                rather, it returns an object whose `display()` method can
                subsequently be called to append the element to the page, and
                whose `value` field provides the element's current value.

        Returns:
            If defer_display is False (the default):
                default_value if the user has not interacted with the
                multiselect; otherwise, returns the value(s) set by the user.

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this element to the page, and whose `value` field
                provides the current element value (as would be returned if
                defer_display were False).
        """
        return self._append_select(
            values=values,
            multi=True,
            default_value=default_value,
            label=label,
            id=id,
            hot_keys=hot_keys,
            defer_display=defer_display)

    def radio(
        self,
        values: List[str],
        *,  # all subsequent parameters are keyword-only
        default_value: Optional[str] = None,
        label: Optional[str] = None,
        id: Optional[str] = None,
        horizontal: bool = False,
        hot_keys: Optional[List[Optional[str]]] = None,
        defer_display: bool = False) -> Union[Optional[str], DeferredElement]:
        """Appends a radio button group and returns its current value.

        Args:
            values: The values among which to select.  One radio button is
                rendered for each element of values, with the corresponding
                value displayed adjacent to each radio button.
            default_value: The initially selected (default) value (i.e., prior
                to user interaction with the radio button group).  If provided,
                must be present in the values argument.
            label: The label to be displayed adjacent to the radio button group.
            id: The radio button group's id within its Page.  If id is not
                provided, then the radio button group's id is derived from
                values and label.  The radio button group's id must be unique
                among all radio button groups in this radio button group's Page.
            hot_keys: Optional list of keyboard shortcuts that can be used to
                select each corresponding value in this radio button group
                (e.g., ["Cmd+a", "Cmd+b"]).  If provided, this list must have
                the same length as values.  Elements of hot_keys can be None to
                indicate that the corresponding radio buttons should not have
                keyboard shortcuts.
            defer_display: If False (the default), then this method appends the
                radio button group to the page and returns its current value.
                If True, then this method does not itself append the radio
                button group to the page; rather, it returns an object whose
                `display()` method can subsequently be called to append the
                radio button group to the page, and whose `value` field provides
                the radio button group's current value.

        Returns:
            If defer_display is False (the default):
                default_value if the user has not interacted with the radio
                button group; otherwise, returns the value of the currently
                selected radio button.

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this radio button group to the page, and whose `value`
                field provides the current value of the radio button group (as
                would be returned if defer_display were False).
        """
        id_prefix = "radio:"
        if id is None:
            id = id_prefix + ",".join(values)
            if label is not None:
                id += ":" + label
        else:
            id = id_prefix + id
        props = {
            "id": id,
            "options": [{"value": v} for v in values],
            "horizontal": horizontal
        }
        if default_value:
            if default_value not in values:
                raise ValueError(
                    "If provided, default_value must be present in the values "
                    "argument.")
            props["initialValue"] = default_value
        if label is not None:
            props["label"] = label
        if hot_keys is not None:
            if len(hot_keys) != len(values):
                raise ValueError(
                    "hot_keys is non-None but does not have the same length "
                    "as values.")
            for keys, option in zip(hot_keys, props["options"]):
                if keys:
                    option["hotKeys"] = keys
        def _get_value(values: Tuple[bool, Any]) -> Optional[str]:
            value_set, value = values
            if value_set:
                if value is None:
                    return None
                if value not in values:
                    raise ValueError(
                        "Frontend unexpectedly returned a value not "
                        "present in the values argument.")
                return value
            else:
                return default_value
        element = _Element("RadioButtons", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            return _get_value(self._append(element, id))

    def button(
        self,
        label: str,
        *,
        color: Optional[Literal["gray", "grey", "blue",
                                "green", "yellow", "red"]] = None,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None,
        defer_display: bool = False) -> Union[bool, DeferredElement]:
        """Appends a button and returns True if button was just pressed.

        Args:
            label: The label to be displayed within the button.  If id is None,
                label is used as this button's id and must be unique among the
                ids of buttons in this container.
            color: Optional color for this button.
            id: The button's id within its Page.  If provided, must be unique
                among the ids of buttons within this button's Page; if not
                provided, then label is used as this button's id.
            hot_keys: Optional keyboard shortcut that can be used to trigger
                this button (e.g., "1", "Cmd+g").
            defer_display: If False (the default), then this method appends the
                button to the page and returns True if it was just pressed.
                If True, then this method does not itself append the button to
                the page; rather, it returns an object whose `display()` method
                can subsequently be called to append the button to the page, and
                whose `value` field is True if this button was just pressed (and
                False otherwise).

        Returns:
            If defer_display is False (the default):
                True if the user's last action was pressing this button, and
                False otherwise.

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this button to the page, and whose `value` field is True
                if and only if the user's last action was pressing this button
                (as would be returned if defer_display were False).
        """
        id = "button:" + (id if id is not None else label)
        props = {"id": id, "label": label}
        if color is not None:
            props["color"] = color
        if hot_keys is not None:
            props["hotKeys"] = hot_keys
        def _get_value(values: Tuple[bool, Any]) -> bool:
            _, value = values
            return value if value is not None else False
        element = _Element("Button", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            return _get_value(self._append(element, id))

    def input(
        self,
        placeholder: Optional[str] = None,
        label: Optional[str] = None,
        *,
        default_value: Optional[str] = None,
        num_lines: int = 1,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None,
        defer_display: bool = False) -> Union[Optional[str], DeferredElement]:
        """Appends a text input field and returns its current value.

        Calls to update the page are not triggered by modifications of the
        input field's contents. If num_lines == 1, then a call to update the
        page is triggered if `Enter` is pressed while the input field is
        focused. If num_lines > 1, then a call to update the page is triggered
        if `Cmd/Ctrl + Enter` is pressed while the input field is focused.

        Args:
            placeholder: Placeholder text to be displayed in the input if
                its current value is None.
            label: The label to be displayed immediately above this input
                field.
            default_value: The input's initial default value (i.e., prior to
                user interaction with it).
            num_lines: Number of text lines that this input should visibly span.
                Must be positive. If 1, then a single-line text input
                field is displayed. If greater than 1, then a multi-line
                input area is displayed (which visibly spans num_lines
                lines but permits entering arbitrarily many lines of text).
            id: The input's id within its Page.  Must be provided if neither
                placeholder nor label is provided. If id is not provided, then
                the input's id is derived from placeholder and label.  The
                input's id must be unique among all inputs in this input's Page.
            hot_keys: Optional keyboard shortcut that can be used to focus the
                input (e.g., "1", "command+g").
            defer_display: If False (the default), then this method appends the
                element to the page and returns its current value.  If True,
                then this method does not itself append the element to the page;
                rather, it returns an object whose `display()` method can
                subsequently be called to append the element to the page, and
                whose `value` field provides the element's current value.

        Returns:
            If defer_display is False (the default):
                default_value if the user has not interacted with this input;
                otherwise, returns the value inputted by the user.

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this element to the page, and whose `value` field
                provides the current element value (as would be returned if
                defer_display were False).
        """
        if placeholder is None and label is None and id is None:
            raise ValueError(
                "Placeholder, label and id are None; at least one must be "
                "provided.")
        if num_lines < 1:
            raise ValueError("num_lines must be positive.")
        if num_lines == 1:
            if (placeholder is not None and
                ("\n" in placeholder or "\r" in placeholder)):
                raise ValueError(
                    "If num_lines is 1, placeholder must not have line breaks.")
            if (default_value is not None and
                ("\n" in default_value or "\r" in default_value)):
                raise ValueError(
                    "If num_lines is 1, default_value must not have line "
                    "breaks.")

        id_prefix = "input:"
        if id is None:
            id = id_prefix
            id += ("" if placeholder is None else placeholder) + ":"
            id += ("" if label is None else label)
        else:
            id = id_prefix + id

        props = {
            "id": id,
            "numLines": num_lines
        }
        if placeholder is not None:
            props["placeholder"] = placeholder
        if label is not None:
            props["label"] = label
        if default_value is not None:
            props["defaultValue"] = default_value
        if hot_keys is not None:
            props["hotKeys"] = hot_keys
        def _get_value(values: Tuple[bool, Any]) -> Optional[str]:
            _, value = values
            return value if value is not None else default_value
        element = _Element("Input", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            return _get_value(self._append(element, id))

    def number_input(
        self,
        label: Optional[str] = None,
        *,
        allow_float: bool = False,
        default_value: Optional[Union[int, float]] = None,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None,
        defer_display: bool = False
    ) -> Union[Optional[Union[int, float]], DeferredElement]:
        """Appends a number input field and returns its current value.

        Calls to update the page are not triggered by modifying the number input
        field's contents.  Pressing `Enter` while the field is focused triggers
        a call to update the page.

        Args:
            label: The label to be displayed immediately above this number input
                field.  If not provided, then the id argument must be provided.
            allow_float: If True, then this number input field allows float
                values to be entered.  If False, then only integers can be
                entered.
            default_value: This field's initial default value (i.e., prior to
                user interaction with it).  Must be an integer if allow_float is
                False.
            id: This number input field's id within its Page.  Must be provided
                if label is not provided.  If id is not provided, then this
                field's id is derived from label.  The field's id must be unique
                among all number input fields in this number input field's Page.
            hot_keys: Optional keyboard shortcut that can be used to focus this
                number input field (e.g., "1", "command+g").
            defer_display: If False (the default), then this method appends the
                element to the page and returns its current value.  If True,
                then this method does not itself append the element to the page;
                rather, it returns an object whose `display()` method can
                subsequently be called to append the element to the page, and
                whose `value` field provides the element's current value.

        Returns:
            If defer_display is False (the default):
                default_value if the user has not interacted with this number
                input field; otherwise, returns the value inputted by the user.

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this element to the page, and whose `value` field
                provides the current element value (as would be returned if
                defer_display were False).
        """
        if (not allow_float and default_value is not None
                and isinstance(default_value, float)):
            raise ValueError("default_value must be an integer if allow_float "
                             "is False.")

        id = "number_input:" + (id if id is not None else label)
        props = {"id": id, "allowFloat": allow_float}
        if label is not None:
            props["label"] = label
        if default_value is not None:
            props["defaultValue"] = default_value
        if hot_keys is not None:
            props["hotKeys"] = hot_keys
        def _get_value(values: Tuple[bool, Any]) -> Optional[Union[int, float]]:
            _, value = values
            if value is not None:
                if not isinstance(value, int) and not isinstance(value, float):
                    raise ValueError("Frontend unexpectedly returned a value "
                                    "that is not a number.")
                if not allow_float and isinstance(value, float):
                    raise ValueError("Frontend unexpectedly returned a value "
                                     "that is not an integer.")
            return value if value is not None else default_value
        element = _Element("NumberInput", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            return _get_value(self._append(element, id))

    def file_upload(
        self,
        initial_message: str,
        *,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None,
        defer_display: bool = False
    ) -> Union[Optional[Tuple[bytes, str]], DeferredElement]:
        """Appends a file selector; returns uploaded contents of selected file.

        The file selector interface enables selection (and upload) of a file via
        both drag-and-drop and the browser-local native filesystem browser.

        Args:
            initial_message: The initial message to be displayed within the file
                selector interface, prior to selection of a file (e.g., "Drop a
                file here to upload...").
            id: The file selector's id within its Page.  If id is not provided,
                then the file selector's id is derived from initial_message.
                The file selector's id must be unique among all file selectors
                within this file selector's Page.
            hot_keys: Optional keyboard shortcut that can be used to open the
                browser's native file selection interface (e.g., "1", "Cmd+g").
            defer_display: If False (the default), then this method appends the
                element to the page and returns its current value.  If True,
                then this method does not itself append the element to the page;
                rather, it returns an object whose `display()` method can
                subsequently be called to append the element to the page, and
                whose `value` field provides the element's current value.

        Returns:
            If defer_display is False (the default):
                None if no file has been selected by the user; otherwise,
                returns a tuple containing (the uploaded contents of the
                selected file as bytes, the browser-local path of the
                selected file).

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this element to the page, and whose `value` field
                provides the current element value (as would be returned if
                defer_display were False).
        """
        id = "file_upload:" + (id if id is not None else initial_message)
        props = {"id": id, "initialMessage": initial_message}
        if hot_keys is not None:
            props["hotKeys"] = hot_keys
        def _get_value(values: Tuple[bool, Any]) -> Optional[Tuple[bytes, str]]:
            _, value = values
            if (value is not None and
                ("bytes" not in value or "path" not in value)):
                raise ValueError(
                    "Value received from frontend is unexpectedly in the wrong "
                    "format.")
            if value is not None:
                base64_bytes = value["bytes"].encode("utf-8")
                value = (base64.decodebytes(base64_bytes), value["path"])
            return value
        element = _Element("FileUpload", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            return _get_value(self._append(element, id))

    def slider(
        self,
        min_max: Tuple[int, int],
        label: Optional[str] = None,
        *,
        range: bool = False,
        default_value: Union[int, Tuple[int, int], None] = None,
        id: Optional[str] = None,
        defer_display: bool = False
    ) -> Union[int, Tuple[int, int], DeferredElement]:
        """Appends a numeric slider input and returns its current value.

        Args:
            min_max: The minimum and maximum numeric values that can be selected
                via this slider.
            label: The label to be displayed immediately above the slider.
            range: If True, then the slider can be used to select a pair of
                numeric values.  If False, then the slider can be used to select
                a single numeric value.
            default_value: This slider's initial default value (i.e., prior to
                user interaction with it).  Must be an integer if range is
                False, and a pair of integers otherwise.  If not provided,
                then the slider's initial default value will be min_max[0]
                if range is False, or min_max if range is True.
            id: This slider's id within its Page.  If id is not provided, then
                this slider's id is derived from min_max, as well as label if
                provided.  The slider's id must be unique among all sliders in
                this slider's Page.
            defer_display: If False (the default), then this method appends the
                element to the page and returns its current value.  If True,
                then this method does not itself append the element to the page;
                rather, it returns an object whose `display()` method can
                subsequently be called to append the element to the page, and
                whose `value` field provides the element's current value.

        Returns:
            If defer_display is False (the default):
                If the user has not yet interacted with this slider:
                    default_value, if provided; otherwise, min_max[0] if range
                    is False, or min_max if range is True.
                If the user has interacted with this slider:
                    The value(s) selected by the user (i.e., a single integer
                    if range is False, and a pair of integers otherwise).

            If defer_display is True:
                An object whose `display()` method can subsequently be called to
                append this element to the page, and whose `value` field
                provides the current element value (as would be returned if
                defer_display were False).
        """
        if len(min_max) != 2:
            raise ValueError("min_max must be a tuple of length 2.")
        if not isinstance(min_max[0], int) or not isinstance(min_max[1], int):
            raise ValueError("min_max must be a tuple of integers.")
        if min_max[0] >= min_max[1]:
            raise ValueError("min_max must be a tuple of the form (min, max) "
                             "where min < max.")
        id_prefix = "slider:"
        if id is None:
            id = f"{min_max[0]},{min_max[1]}"
            id += "" if label is None else f":{label}"
        id = id_prefix + id
        props = {"id": id, "min": min_max[0], "max": min_max[1], "range": range}
        if default_value is not None:
            if range:
                if (len(default_value) != 2 or
                    not isinstance(default_value[0], int) or
                    not isinstance(default_value[1], int)):
                    raise ValueError("default_value must be a pair of integers "
                                     "if range is True.")
                if default_value[0] >= default_value[1]:
                    raise ValueError("default_value must be a tuple of the "
                                    "form (min, max) where min < max.")
            elif not isinstance(default_value, int):
                raise ValueError("default_value must be an integer if range is "
                                "False.")
            props["initialValue"] = default_value if range else [default_value]
        else:
            props["initialValue"] = min_max if range else [min_max[0]]
            default_value = min_max if range else min_max[0]
        if label is not None:
            props["label"] = label

        def _get_value(
            values: Tuple[bool, Any]
        ) -> Optional[Union[int, Tuple[int, int]]]:
            _, value = values
            if value is not None:
                if range:
                    return (value[0], value[1])
                else:
                    return value[0]
            return default_value
        element = _Element("Slider", props)
        if defer_display:
            return DeferredElement(self, element, id, _get_value)
        else:
            return _get_value(self._append(element, id))

    def form(self) -> ContainerStackContextManager:
        """Returns a context manager for a new form.

        Input elements (such as checkbox, select, radio, etc.) added to a
        page within the returned form context do not trigger calls to update
        the page.  Within a form context, only button presses trigger
        page updates.
        """
        return ContainerStackContextManager(_Element("Form", {}), self)

    def horizontal(
        self,
        align: Literal["left", "center", "right"] = "left"
    ) -> ContainerStackContextManager:
        """Returns a context manager for horizontal layout.

        Elements added to a page within the returned context are displayed
        horizontally from left to right (rather than being appended vertically
        to the bottom of the page).  If the elements added to the page
        within the returned context cannot all fit horizontally on the page,
        then the layout will overflow to one or more new lines.

        Args:
            align: The horizontal alignment within this horizontal layout's
                container for elements added to this horizontal layout.
        """
        return ContainerStackContextManager(
            _Element("Horizontal", {"align": align}), self)

    def tabs(self) -> ContainerStackContextManager:
        """Returns a context manager for a tab bar.

        Only tabs can be directly added to a page within the returned context.
        For example (where p is a Page object):

        with p.tabs():
            with p.tab("First Tab's Label"):
                p.print("Content in first tab")
            with p.tab("Second Tab's Label"):
                p.print("Content in second tab")
        p.print("Content after tabs")
        """
        return ContainerStackContextManager(_Element("Tabs", {}), self)

    def tab(self, label: str, *,
        hot_keys: Optional[str] = None) -> ContainerStackContextManager:
        """Returns a context manager for a tab within a tab bar.

        Elements added to a page within the returned context are appended within
        a tab having the given label.  In conjunction with the tabs() method,
        this method can be used to create tabbed layouts as follows (where p is
        a Page object):

        with p.tabs():
            with p.tab("First Tab's Label"):
                p.print("Content in first tab")
            with p.tab("Second Tab's Label"):
                p.print("Content in second tab")
        p.print("Content after tabs")

        Args:
            label: The label for this tab (which will be displayed in the tab
                bar).
            hot_keys: Optional keyboard shortcut that can be used to display
                this tab (e.g., "1", "command+g").
        """
        props = {"label": label}
        if hot_keys is not None:
            props["hotKeys"] = hot_keys

        return ContainerStackContextManager(_Element("Tab", props), self)

    def columns(self) -> ContainerStackContextManager:
        """Returns a context manager for a columnar layout.

        Only columns can be directly added to a page within the returned
        context.  For example (where p is a Page object):

        with p.columns():
            with p.column():
                p.heading("Column 1")
            with p.column():
                p.heading("Column 2")
                p.print("Content in second column")
        p.print("Content after columns")
        """
        return ContainerStackContextManager(_Element("Columns", {}), self)

    def column(
        self,
        width: Optional[float] = None,
        align: Literal["left", "center", "right"] = "left"
    ) -> ContainerStackContextManager:
        """Returns a context manager for a column within a columnar layout.

        Elements added to a page within the returned context are appended
        vertically, with widths constrained to be at most the width of this
        column.  In conjunction with the columns() method, this method can be
        used to create multi-column layouts as follows (where p is a Page
        object):

        with p.columns():
            with p.column():
                p.heading("Column 1")
            with p.column():
                p.heading("Column 2")
                p.print("Content in second column")
        p.print("Content after columns")

        Args:
            width: Optionally, the width of this column, as a fraction of its
                container's width.  If not provided, then this column will
                occupy all width not occupied by other columns having explicitly
                specified widths in the same columnar layout.  If multiple
                columns in the same columnar layout do not have widths
                specified, then these columns will evenly split any width not
                occupied by columns that do have widths explicitly specified.
            align: The alignment, within this column's width, for elements
                added to this column.
        """
        props = {"align": align}

        if width is not None:
            if width <= 0 or width > 1:
                raise ValueError("width must be a fraction of its container "
                                 "width (must satisfy 0 < width <= 1).")
            props["width"] = str(width * 100) + "%"
        return ContainerStackContextManager(_Element("Column", props), self)

    def modal(
        self,
        trigger_open: bool,
        title: Optional[str],
        *,
        id: Optional[str] = None,
        hot_keys: Optional[str] = None) -> ModalContextManager:
        """Returns a context manager for a modal.

        If the modal is not already open and trigger_open is True, then the
        modal is displayed.  Elements added to a page within the returned
        context are appended within the body of the modal.  The returned
        context manager also provides a close() method that can be used to
        close the modal if it is currently displayed.  For example:
        ```
        with p.modal(p.button("Start training"), "Train a new model") as m:
            name = p.input("Name for training run")
            if p.button("Start"):
                ...
                m.close()
        ```

        Args:
            trigger_open: If the modal is not already open and trigger_open is
                True, then the modal is displayed.  Otherwise (i.e., if the
                modal is already open or trigger_open is False), this argument
                has no effect.
            title: Optionally, the title to be displayed at the top of this
                modal.
            id: The modal's id within its Page.  If not provided, then title is
                used as this modal's id; title must be provided if id is not
                provided.  This modal's id must be unique among all modals in
                this modal's Page.
            hot_keys: Optional keyboard shortcut that can be used to trigger
                this modal to open or close (e.g., "1", "Cmd+g").

        Returns:
            Context manager that can be used to populate the modal, as well as
            close it if it is currently displayed.
        """
        if id is None and title is None:
            raise ValueError("id or title must be provided.")
        id = "modal:" + (id if id is not None else title)
        props = {"id": id}
        if title is not None:
            props["title"] = title
        if hot_keys is not None:
            props["hotKeys"] = hot_keys
        context_manager = ModalContextManager(props, self)
        if trigger_open:
            context_manager._open()  # pylint: disable=protected-access
        return context_manager

    def collapsible(
        self,
        title: str,
        *,
        start_collapsed: bool = True) -> ContainerStackContextManager:
        """Returns a context manager for a collapsible card.

        Elements added to a page within the returned context are appended within
        a collapsible card having the given title.  When the card is collapsed,
        only the title and an icon that can be used to expand the card are
        visible (clicking on either the title or the icon will expand the card).
        When the card is expanded, all of the content that has been appended
        within it is also visible.

        Args:
            title: The title for the collapsible card.
            start_collapsed: If True, then the card will initially display in
                its collapsed configuration; otherwise, the card will initially
                display in its expanded configuration.
        """
        return ContainerStackContextManager(
            _Element("Collapsible", {
                "title": title,
                "startCollapsed": start_collapsed
            }), self)

    def card(self, title: Optional[str]) -> ContainerStackContextManager:
        """Returns a context manager for a card.

        Elements added to a page within the returned context are appended within
        a card (i.e., a box with a visible border), optionally having the given
        title.  The card spans the width of its container.

        Args:
            title: Optionally, the title for the card.
        """
        return ContainerStackContextManager(
            _Element("Card", {"title": title}), self)


class Page(_ContainerStack):
    """A web page."""

    def __init__(
        self,
        title: str,
        *,
        vertical_align: Literal["top", "center"] = "top"):
        """Constructs a new Page.

        Args:
            title: The page title to be displayed in the browser.
            vertical_align: The vertical alignment for content added to the
                page body.
        """
        super().__init__(
            [_Element("PageBody", {"verticalAlign": vertical_align})], set())
        self._title = title
        self._redirect_url: Optional[str] = None
        self._navbar: Optional[_Element] = None
        self._sidebar: Optional[_Element] = None
        self._state = copy.deepcopy(self._element_values.get("state", {}))

    @property
    def state(self) -> Dict[str, Any]:
        """Dict that persists across interactions with this Page.

        This dict provides the ability to maintain arbitrary state
        across interactions with a Page.  It can be updated or
        modified at will, with the sole constraint that its contents
        must be JSON-serializable.  The contents of the dict will
        then be available during the next server call triggered by
        an interaction with the Page.
        """
        return self._state

    def to_element(self) -> _Element:
        """Returns an _Element instance representing this page."""
        if self._redirect_url:
            return _Element("Redirect", {"url": self._redirect_url})
        else:
            props = {"title": self._title, "state": self._state}
            if self._navbar is not None:
                props["navbar"] = self._navbar.to_json_dict()
            if self._sidebar is not None:
                props["sidebar"] = self._sidebar.to_json_dict()
            return _Element("Page", props, [self._stack[0]])

    def redirect(self, url: str):
        """Redirects the user's browser to the given url.

        If redirect() is called on a Page, then that Page's contents (if any)
        are ignored.  Can only be called once on a given Page instance.

        Args:
            url: URL to which to redirect the user's browser.

        Raises:
            RuntimeError if redirect() has been called previously on this
            Page.
        """
        if self._redirect_url:
            raise RuntimeError(
                "Attempted to call redirect() more than once on this Page.")
        self._redirect_url = url

    def navbar(
        self,
        logo: TextLike,
        left: Optional[List[TextLike]] = None,
        center: Optional[List[TextLike]] = None,
        right: Optional[List[TextLike]] = None):
        """Prepends a navbar to this page.

        Args:
            logo: Content (e.g., text or link) to display in the most prominent
                leftmost position in the navbar.
            left: Content (e.g., text or links) to display immediately after
                the logo.
            center: Content (e.g., text or links) to display in the horizontal
                center of the navbar.
            right: Content (e.g., text or links) to display on the righthand
                side of the navbar.
        """
        def convert_text_like(text_like: TextLike) -> _Element:
            if isinstance(text_like, str):
                return _Element("Fragment", {}, [text_like])
            elif isinstance(text_like, FormattedText):
                text_copy = text_like.copy()
                # pylint: disable-next=protected-access
                return text_copy._unstyle_links()
            else:
                return text_like
        props = {"logo": convert_text_like(logo).to_json_dict()}
        if left:
            props["leftChildren"] = [
                convert_text_like(c).to_json_dict() for c in left]
        if center:
            props["centerChildren"] = [
                convert_text_like(c).to_json_dict() for c in center]
        if right:
            props["rightChildren"] = [
                convert_text_like(c).to_json_dict() for c in right]
        self._navbar = _Element("Navbar", props)

    def sidebar(self) -> ContainerStackContextManager:
        """Returns a context manager for a sidebar.

        Elements added to a page within the returned context are appended
        and displayed within a collapsible sidebar on the lefthand side of the
        page.
        """
        if self._sidebar is None:
            self._sidebar = _Element("Sidebar", {})
        return ContainerStackContextManager(self._sidebar, self, False)

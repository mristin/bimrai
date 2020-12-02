"""Visualize the semantically-annotated scenarios to different formats."""

import dataclasses
import itertools
import os
import pathlib
import sys
import textwrap
import uuid
import xml.etree.ElementTree as ET
from typing import List

import marko

# Don't forget to update the version in setup.py and CHANGELOG.rst!
__version__ = '0.0.0'
__author__ = 'Marko Ristin'
__copyright__ = 'Copyright 2020 ZHAW'
__license__ = 'MIT'
__status__ = 'Production'


def process(source_path: pathlib.Path, target_path: pathlib.Path) -> int:
    """
    Parse the markdown from the source and render it as HTML to target.

    :return: exit code
    """

    def printerr(text: str) -> None:
        """Print to stderr."""
        print(text, file=sys.stderr)

    if not source_path.exists():
        if not source_path.is_absolute():
            printerr(
                f"The input path does not exist: {source_path}; "
                f"the current working directory is {os.getcwd()}")
        else:
            printerr(f"The input path does not exist: {source_path}")

        return -1

    html_text = (
        "<html>"
        "<body>"
        f"{marko.convert(source_path.read_text())}"
        "</body>"
        "</html>")

    root = ET.fromstring(html_text)

    # Validate title

    h1_count = sum(1 for _ in root.iter('h1'))
    if h1_count == 0:
        printerr(f"No title could be identified in the scenario: {source_path}; "
                 f"is your title annotated with `#`?")
        return -1
    elif h1_count > 1:
        printerr(
            f"You specified more than one title in the scenario: {source_path}; "
            f"make sure only one heading is annotated with `#`.")
        return -1
    else:
        pass

    # Validate that all <def>, <ref>, <phase> and <level> have
    # the name attribute

    for element in itertools.chain(
            root.iter('def'), root.iter('ref'),
            root.iter('model'), root.iter('modelref'),
            root.iter('phase'), root.iter('level')):
        if 'name' not in element.attrib:
            printerr(
                f'A <{element.tag}> lacks the `name` attribute in: {source_path}')

    assert h1_count == 1
    title_h1 = next(root.iter('h1'))

    # Replace <def> tags with proper HTML
    for element in root.iter("def"):
        anchor_name = element.attrib.get('name')

        # Transform
        element.tag = "div"
        element.attrib = {'class': 'definition'}

        anchor_id = f'def-{anchor_name}'

        link_el = ET.Element(
            'a', attrib={'href': f'#{anchor_id}', 'class': 'anchor'})
        link_el.append(ET.Element('a', attrib={'id': anchor_id}))
        link_el.text = '🔗'
        link_el.tail = anchor_name

        heading_el = ET.Element('h3')
        heading_el.insert(0, link_el)

        element.insert(0, heading_el)

    # Replace <model> tags with proper HTML
    for element in root.iter("model"):
        anchor_name = element.attrib.get('name')

        # Transform
        element.tag = "div"
        element.attrib = {'class': 'model'}

        heading_el = ET.Element('h3')
        heading_el.text = anchor_name

        anchor_id = f'model-{anchor_name}'

        link_el = ET.Element(
            'a', attrib={'href': f'#{anchor_id}', 'class': 'anchor'})
        link_el.append(ET.Element('a', attrib={'id': anchor_id}))
        link_el.text = '🔗'
        link_el.tail = anchor_name

        heading_el = ET.Element('h3')
        heading_el.insert(0, link_el)

        element.insert(0, heading_el)

    # Replace <ref> tags with proper HTML
    for element in root.iter("ref"):
        anchor_name = element.attrib['name']

        element.tag = "a"
        element.attrib = {'href': f"#def-{anchor_name}",
                          'class': 'ref'}

        if len(element) == 0 and not element.text:
            element.text = anchor_name

    # Replace <modelref> tags with proper HTML
    for element in root.iter("modelref"):
        anchor_name = element.attrib['name']

        element.tag = "a"
        element.attrib = {'href': f"#model-{anchor_name}",
                          'class': 'modelref'}

        if len(element) == 0 and not element.text:
            element.text = anchor_name

    # Replace <phase> tags with proper HTML

    @dataclasses.dataclass
    class PhaseAnchor:
        identifier: str
        phase: str

    phase_anchors = []  # type: List[PhaseAnchor]

    for element in root.iter("phase"):
        name = element.attrib['name']

        element.tag = 'span'
        element.attrib = {'class': 'phase', 'data-text': name}

        sup_el = ET.Element('sup')
        sup_el.text = name
        element.append(sup_el)

        anchor = f'phase-anchor-{uuid.uuid4()}'
        anchor_el = ET.Element('a', attrib={"id": anchor})
        element.insert(0, anchor_el)
        phase_anchors.append(PhaseAnchor(identifier=anchor, phase=name))

    # Replace <level> tags with proper HTML

    @dataclasses.dataclass
    class LevelAnchor:
        identifier: str
        level: str

    level_anchors = []  # type: List[LevelAnchor]

    for element in root.iter("level"):
        name = element.attrib['name']

        element.tag = 'span'
        element.attrib = {'class': 'level', 'data-text': name}

        sup_el = ET.Element('sup')
        sup_el.text = name
        element.append(sup_el)

        anchor = f'level-anchor-{uuid.uuid4()}'
        anchor_el = ET.Element('a', attrib={"id": anchor})
        element.insert(0, anchor_el)
        level_anchors.append(LevelAnchor(identifier=anchor, level=name))

    # Append phase index

    if phase_anchors:
        body = next(root.iter('body'))

        heading_el = ET.Element('h2')
        heading_el.text = "Phase Index"
        body.append(heading_el)

        list_el = ET.Element('ul')
        for anch in phase_anchors:
            link_el = ET.Element('a', attrib={'href': f'#{anch.identifier}'})
            link_el.text = anch.phase

            item_el = ET.Element('li')
            item_el.append(link_el)

            list_el.append(item_el)

        body.append(list_el)

    # Append level index

    if level_anchors:
        body = next(root.iter('body'))

        heading_el = ET.Element('h2')
        heading_el.text = "Level Index"
        body.append(heading_el)

        list_el = ET.Element('ul')
        for anch in level_anchors:
            link_el = ET.Element('a', attrib={'href': f'#{anch.identifier}'})
            link_el.text = anch.level

            item_el = ET.Element('li')
            item_el.append(link_el)

            list_el.append(item_el)

        body.append(list_el)

    # Construct <head>

    head_el = ET.Element('head')
    title_el = ET.Element('title')
    title_el.text = title_h1.text
    head_el.append(title_el)

    style_el = ET.Element('style')
    style_el.text = textwrap.dedent(
        '''\
        body {
            margin-right: 5%;
            margin-left: 5%;
            margin-top: 5%;
            margin-bottom: 5%;
            padding: 1%;
            border: 1px solid black;
        }

        a.anchor {
            text-decoration: none;
            font-size: x-small;
            margin-right: 1em;
        }

        span.phase {
            background-color: #eefbfb;
        }

        span.level {
            background-color: #eefbee;
        }

        pre {
            background-color: #eeeefb;
            padding: 1em;
        }
        ''')
    head_el.append(style_el)

    root.insert(0, head_el)

    target_path.write_bytes(ET.tostring(root, encoding='utf-8'))
    print(f"Saved to: {target_path}")
    return 0

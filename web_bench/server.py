#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from time import sleep

import bjoern
from flask import Flask

five_paragraphs = """
Lorem ipsum dolor sit amet, consectetur
adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Diam sit amet nisl suscipit adipiscing bibendum est
ultricies. Egestas quis ipsum suspendisse ultrices gravida dictum. Sit
amet venenatis urna cursus eget nunc scelerisque viverra
mauris. Eleifend mi in nulla posuere sollicitudin aliquam
ultrices. Donec adipiscing tristique risus nec feugiat in. Sapien
faucibus et molestie ac feugiat. Cursus euismod quis viverra nibh cras
pulvinar mattis nunc sed. Amet mauris commodo quis imperdiet. Semper
auctor neque vitae tempus quam. Elementum integer enim neque volutpat
ac tincidunt vitae semper. Nisi porta lorem mollis aliquam ut
porttitor leo. Quisque non tellus orci ac auctor augue. Amet facilisis
magna etiam tempor orci eu lobortis elementum nibh. Interdum velit
euismod in pellentesque massa placerat. Vel orci porta non pulvinar
neque.

Fringilla urna porttitor rhoncus dolor purus non enim. Sollicitudin
nibh sit amet commodo nulla facilisi nullam vehicula. Varius vel
pharetra vel turpis nunc eget. Viverra suspendisse potenti nullam
ac. Ut consequat semper viverra nam. Diam quam nulla porttitor massa
id neque. Amet porttitor eget dolor morbi. Turpis egestas integer eget
aliquet nibh praesent tristique. Felis eget nunc lobortis mattis
aliquam faucibus purus in. Pellentesque id nibh tortor id aliquet
lectus proin nibh nisl. Mauris rhoncus aenean vel elit
scelerisque. Nascetur ridiculus mus mauris vitae ultricies
leo. Aliquam purus sit amet luctus. Arcu risus quis varius quam. Elit
eget gravida cum sociis natoque penatibus et magnis. Blandit cursus
risus at ultrices mi tempus imperdiet nulla.

Varius morbi enim nunc faucibus a pellentesque sit amet. Purus viverra
accumsan in nisl nisi scelerisque eu. Turpis cursus in hac habitasse
platea dictumst quisque sagittis purus. Risus pretium quam vulputate
dignissim. Sed adipiscing diam donec adipiscing tristique. Odio eu
feugiat pretium nibh ipsum consequat. Pellentesque nec nam aliquam
sem. Tellus pellentesque eu tincidunt tortor aliquam. Tellus elementum
sagittis vitae et leo. Eget duis at tellus at urna condimentum
mattis. Quisque non tellus orci ac auctor augue mauris augue. Donec
pretium vulputate sapien nec sagittis aliquam. Tellus in hac habitasse
platea dictumst. Suspendisse ultrices gravida dictum fusce ut placerat
orci nulla. Urna id volutpat lacus laoreet non curabitur
gravida. Ultrices neque ornare aenean euismod elementum. Nisl vel
pretium lectus quam id leo in. Vulputate mi sit amet mauris. Magna
etiam tempor orci eu lobortis elementum nibh. Integer feugiat
scelerisque varius morbi enim nunc.

Etiam dignissim diam quis enim lobortis scelerisque fermentum. Non
arcu risus quis varius quam quisque id diam vel. Ac ut consequat
semper viverra nam libero justo laoreet sit. Pharetra et ultrices
neque ornare aenean. Sed risus ultricies tristique nulla aliquet enim
tortor at. Nibh venenatis cras sed felis eget velit aliquet
sagittis. Molestie nunc non blandit massa. Id aliquet lectus proin
nibh nisl condimentum id venenatis. Diam ut venenatis tellus in
metus. Adipiscing elit duis tristique sollicitudin nibh.  Elementum
tempus egestas sed sed. Enim neque volutpat ac tincidunt vitae semper
quis. Egestas sed tempus urna et pharetra. Sed enim ut sem
viverra. Placerat duis ultricies lacus sed turpis tincidunt id aliquet
risus. Feugiat pretium nibh ipsum consequat nisl vel pretium
lectus. Enim sit amet venenatis urna cursus eget nunc. Viverra aliquet
eget sit amet tellus cras adipiscing enim eu. Sagittis eu volutpat
odio facilisis. Proin fermentum leo vel orci porta non pulvinar. Nulla
facilisi cras fermentum odio eu feugiat pretium. Viverra aliquet eget
sit amet tellus. Feugiat in ante metus dictum at tempor commodo
ullamcorper. Velit dignissim sodales ut eu sem integer
vitae. Sollicitudin aliquam ultrices sagittis orci a. Nunc sed blandit
libero volutpat sed. Ut sem viverra aliquet eget.  Pellentesque
habitant morbi tristique senectus et netus. Quis risus sed vulputate
odio ut enim blandit volutpat.
"""

app = Flask(__name__)


@app.route("/")  # type:ignore [misc]
def hello_world() -> str:
    sleep(1e-6)
    return "Hello world!\n" + five_paragraphs


if __name__ == "__main__":
    assert 4080 == len(five_paragraphs)

    bjoern.run(app, "127.0.0.1", 8000)

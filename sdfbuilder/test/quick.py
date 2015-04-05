"""
Tests basic features through visual inspection, real tests
to follow later.
"""
from ..base import Model, Link, PosableGroup, SDF
from ..math import Vector3
from math import pi


model = Model("temp_bot")
link = Link("my_link")
minibox = Link("my_minibox")

# Link one is a vertical box
link.make_box(1.0, 2, 2, 4)

# Minibox is... well, a mini box
minibox.make_box(0.1, 0.2, 0.2, 0.2)

minibox.align(
    # Bottom of minibox
    Vector3(0, 0, -0.1),

    # Normal vector
    Vector3(0, 0, -1),

    # Tangent vector
    Vector3(1, 0, 0),

    # Top left of link 1
    Vector3(-0.9, -0.9, 2),

    # Normal vector
    Vector3(0, 0, 1),

    # Tangent vector
    Vector3(1, 0, 0),

    # Link to align with
    link
)

# Add link and minibox to a posable group so we can move
# them around together.
group = PosableGroup()
group.add_element(link)
group.add_element(minibox)

# Create a new, larger box called link 2
link2 = Link("my_link_2")
link2.make_box(2.0, 4, 3, 3)

# Now align the group so its right center lands at
# the top center of link 2
group.align(
    # Center of the right face of box 1
    Vector3(1, 0, 0),

    # Vector normal to box 2 right face
    Vector3(1, 0, 0),

    # Vector normal to box 2 top face should align with...(*)
    Vector3(0, 0, 1),

    # Center of the top face of box 2
    Vector3(0, 0, 1.5),

    # Vector normal to box 2 top face
    Vector3(0, 0, 1),

    # (*)...vector normal to box 2 right face
    Vector3(1, 0, 0),

    # the link to align with
    link2
)

model.add_element(group)
model.add_element(link2)
model.rotate_around(Vector3(0, 1, 0), 0.2 * pi)

sdf = SDF()
sdf.add_element(model)
print(str(sdf))
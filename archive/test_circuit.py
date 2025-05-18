# This file will be deleted at some point
#
# Describes a simple circuit with an input, output, and. This wouldnt really do anyhing lol

from circuit import *   

generator = ComponentIDGenerator()

c = Circuit()
a = Component(generator.gen_id(), "AND", ["A", "B"], ["OUT"])
i = InputPin("IN1", ["OUT"])
o = OutputPin("OUT1", ["IN"])

c.add_component(i)
c.add_component(o)

w = Wire("IN1", "OUT", "OUT1", "IN")
c.connect(w)

i.set_output("OUT", True)

print(c.components)
print(c.components["IN1"].id)
print(c.components["IN1"].type)
print(c.components["IN1"].inputs)
print(c.components["IN1"].outputs)
print(c.components["IN1"].connections)

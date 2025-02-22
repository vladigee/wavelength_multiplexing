#%%
import gdsfactory as gf

from cspdk.si220 import PDK, cells, tech
import jax.numpy as jnp
import matplotlib.pyplot as plt
import sax
#%% Building the circuit

c = gf.Component()

ref1 = c.add_ref(gf.components.rectangle(size=(6000, 3000), layer=(1, 0)))
#ref2 = c.add_ref(gf.components.text("Hello", size=10, layer=(2, 0)))
#ref3 = c.add_ref(gf.components.text("world", size=10, layer=(2, 0)))

#ref1.xmax = ref2.xmin - 5
#ref3.xmin = ref2.xmax + 2
#ref3.rotate(30)

gc_input = c << cells.grating_coupler_elliptical()
gc2 = c << cells.grating_coupler_elliptical()
gc3 = c << cells.grating_coupler_elliptical()
gc4 = c << cells.grating_coupler_elliptical()
mmi1 = c << cells.mmi1x2()
mmi2 = c << cells.mmi2x2()
mmi_ring1 = c << cells.coupler_ring_sc()
mmi_ring2 = c << cells.coupler_ring_sc()


gc_input.dmove((-100,-1400))
gc_input.drotate(180)
gc2.dmove((5500,100))
gc3.dmove((5500,1400))
gc4.dmove((5500,2900))
mmi1.dmove((200,1400))
#mmi1.drotate(90)
mmi2.dmove((3000,1400))
#mmi2.drotate(-90)
mmi_ring1.dmove((5000,1800))
mmi_ring2.dmove((5000,1800))

route = tech.route_bundle(c,[mmi1.ports["o2"]], [mmi2.ports["o2"]])
route2 = tech.route_bundle(c,[mmi1.ports["o3"]], [mmi2.ports["o1"]])

route3 = tech.route_bundle(c,[gc_input.ports["o1"]], [mmi1.ports["o1"]])
route4 = tech.route_bundle(c,[mmi2.ports["o3"]], [gc3.ports["o1"]])

route5 = tech.route_bundle(c,[mmi2.ports["o4"]], [gc2.ports["o1"]])

#c.add_port(name="m1", port=mmi1.ports["o1"])
#c.add_port(name="m2", port=mmi2.ports["o3"])

c.show()

# %% Simulation

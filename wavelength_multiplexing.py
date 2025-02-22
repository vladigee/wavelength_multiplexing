#%%
import gdsfactory as gf

from cspdk.si220 import PDK, cells, tech
import jax.numpy as jnp
import matplotlib.pyplot as plt
import sax
#%% only for reference, remove in the end

c = gf.Component()

ref1 = c.add_ref(gf.components.rectangle(size=(6000, 3000), layer=(1, 0)))

#adding the components
gc_input = c << cells.grating_coupler_elliptical()
gc2 = c << cells.grating_coupler_elliptical()
gc3 = c << cells.grating_coupler_elliptical()
gc4 = c << cells.grating_coupler_elliptical()
gc5 = c << cells.grating_coupler_elliptical()
mzi_rc = c << cells.mzi_rc(delta_length=18.3114)
straight = c << cells.coupler_straight(length=20.0, gap=0.27, cross_section='xs_rc').dup()
ring = c <<  cells.ring_single_sc(0.2,26.9238, 50, 50)

#placing the components
gc_input.dmove((-200,-1400))
gc_input.drotate(180)
gc2.dmove((5500,300))
gc3.dmove((5500,2000))
gc4.dmove((3600,2700))
gc5.dmove((4200,2105.15))
mzi_rc.dmove((2000,1400))
#mmi_ring.dmove((4000,2000))
ring.dmove((4000,2000))

#connecting the component
route1 = gf.routing.route_single(c, port1=gc_input.ports["o1"], port2=mzi_rc.ports["o1"], cross_section="xs_sc", allow_width_mismatch=True)
route2 = tech.route_bundle(c,[mzi_rc.ports["o3"]], [gc2.ports["o1"]])
route3 = tech.route_bundle(c,[mzi_rc.ports["o2"]], [ring.ports["o1"]])
route4 = tech.route_bundle(c,[ring.ports["o2"]], [gc3.ports["o1"]])
route5 = tech.route_bundle(c,[gc5.ports["o1"]], [gc4.ports["o1"]])

c.show()
# %% Simulation

#c.add_port(name="m1_input", port=gc_input.ports["o2"])
#c.add_port(name="m2_output", port=gc2.ports["o2"])
#c.add_port(name="m3_output", port=gc3.ports["o1"])
#c.add_port(name="m4_output", port=gc4.ports["o1"])
#c.add_port(name="m5_output", port=gc5.ports["o1"])

models = PDK.models

netlist = c.get_netlist(recursive=True)

circuit, _ = sax.circuit(netlist,models=models)

wl =  jnp.linspace(1.5, 1.6, 256)
S = circuit(wl=wl)

plt.figure(figsize=(14,4))
plt.title("MZI")
plt.plot(1e3*wl,  jnp.abs(S["m1_input",  "m2_output"]) **2)
plt.xlabel("λ [nm]")
plt.ylabel("T")
plt.grid(True)
plt.show()
# %%

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:56:15 2025

@author: AdrianRomero
"""

#Ring desing


import gdsfactory as gf
import sax
import jax.numpy as jnp
import matplotlib.pyplot as plt

from cspdk.si220 import PDK,cells, tech

c=gf.Component()
gc1 = c<< cells.grating_coupler_elliptical(cross_section="xs_rc")
#gc2 = c<< cells.grating_coupler_elliptical()
gc3 = c<< cells.grating_coupler_elliptical(cross_section="xs_rc")
gc4= c<< cells.grating_coupler_elliptical(cross_section="xs_rc")
gc5= c<< cells.grating_coupler_elliptical(cross_section="xs_rc")
gc6= c<< cells.grating_coupler_elliptical(cross_section="xs_rc")

#cou= c<<cells.coupler()
#cou_ring=c<<cells.coupler_ring_sc(0,10,4)

st_line=c<<cells.straight(1600,cross_section="xs_rc")
ring=c<<cells.ring_single_sc(0.2,26.838,50,50,cross_section="xs_rc")
mzi_rc=c<<cells.mzi_rc(18.3114)

#mmi1=c << cells.mmi1x2()
#mmi2= c <<cells.mmi2x2()
#bend_s= c<<cells.bend_s((10,5))
#bend_s2=c<<cells.bend_s((10,-5))



gc1.drotate(180)
gc1.dmove((-100,200))

#cou_ring.rotate(180)
#cou_ring.dmove((70,0))
#gc2.drotate(180)
#gc2.dmove((-100,-50))


mzi_rc.dmove((400,0))
st_line.dmove((700,-40))
ring.dmove((1700,-145.15))
gc3.dmove((4000,-1200))
gc4.rotate(180)
gc4.dmove((-100,-500))
gc5.dmove((4000,1200))
gc6.dmove((4000,100))

#mmi2.move((100,20))
#18.31 um  output 1.547   other 1.53 1.56

#Connect both MMI
route = tech.route_bundle_rc(c,[gc1.ports["o1"]],[mzi_rc.ports["o1"]],cross_section="xs_rc")
#route2=tech.route_bundle(c,[gc2.ports["o1"]],[mzi_rc.ports["o2"]],cross_section="xs_rc")
route3 =tech.route_bundle_rc(c,[mzi_rc.ports["o2"]],[gc5.ports["o1"]],cross_section="xs_rc")
route4=tech.route_bundle_rc(c,[gc3.ports["o1"]],[ring.ports["o2"]],cross_section="xs_rc")
route5=tech.route_bundle_rc(c,[gc4.ports["o1"]],[ring.ports["o1"]],cross_section="xs_rc")
route6=tech.route_bundle_rc(c,[mzi_rc.ports["o3"]],[st_line.ports["o1"]],cross_section="xs_rc")
route7=tech.route_bundle_rc(c,[st_line.ports["o2"]],[gc6.ports["o1"]],cross_section="xs_rc")


#Create input and output ports

#c.add_port(name="lambda0",port=mzi_rc.ports["o1"])
#c.add_port(name="lambda1",port=mzi_rc.ports["o2"])
#c.add_port(name="lambda23",port=mzi_rc.ports["o3"])
#c.add_port(name="Lambda 3",port=ring.ports["o2"])




#c.write_gds(r"C:\Users\AdrianRomero\Documents\demo.gds")  # write it to a GDS file. You can open it in klayout.
c.show()  # show it in klayout
'''
models= PDK.models

netlist= c.get_netlist(recursive= True)
circuit,_ = sax.circuit(netlist,models=models)
wl=jnp.linspace(1.530,1.565,256)

s = circuit(wl=wl)

plt.figure()
plt.rcParams['figure.dpi'] = 300
plt.plot(wl,jnp.abs(s['lambda0','lambda1'])**2,label='First Output')
plt.plot(wl,jnp.abs(s['lambda0','lambda23'])**2,label='Second Output')
plt.xlabel('λ /um')
plt.ylabel('T/a.u.')
plt.title('Mach-Zender Interferometer')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

'''


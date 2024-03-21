# Motivation
The RP2040 boasts a dual-core ARM Cortex M0+ setup, each clocked at a maximum speed of 133MHz.

How effective could we make use of this architecture by dedicating one core to delta-sigma modulation and the other to the control loop?

Additionally, the RP2040 offers intriguing features like interpolators and PIO, which could greatly assist in implementing the modulator.
.cpu cortex-m0
.syntax unified
.thumb
.thumb_func
.global mash3
.section .text

mash3:
    movs r0, #0         @ Initialize s[0] = 0
    movs r1, #0         @ Initialize s[1] = 0
    movs r2, #0         @ Initialize s[2] = 0
    movs r3, #0         @ Initialize f[0] = 0
    movs r4, #0         @ Initialize f[1] = 0
    movs r5, #0         @ Initialize f[2] = 0
    @ r6 is input
    movs r7, #0         @ Always 0

    ldr r6, =0xd0000000
loop:
    @wfe
    
    @ldr r6, [r6, #88]	    @ r6 = input
    rsbs r3, r4, 0	    @ f[0] = -f[1]
    rsbs r4, r5, 0	    @ f[1] = -f[2]
    movs r5, #0         @ f[2] = 0
    
    adds r0, r6, r0	    @ s[0] = input + s[0]. carry bit updated
    adcs r3, r3, r7	    @ f[0] = f[0] + C
    adds r1, r0, r1	    @ s[1] = s[0] + s[1]
    adcs r4, r4, r7	    @ f[1] = f[1] + C
    adds r2, r1, r2	    @ s[2] = s[1] + s[2]
    adcs r5, r5, r7	    @ f[2] = C

    @ Noise cancellation logic
    adds r4, r4, r5	    @ f[1] = f[1] + f[2]
    adds r3, r3, r4	    @ f[0] = f[0] + f[1]

    @ Output = f[0] + 3
    adds r3, r3, 3      @ Add 3 to f[0], result in r3 (output)
    @ldr r6, =0x50200000
    @str r3, [r6, #0x10]

    b loop              @ Loop indefinitely

#!/usr/bin/python3

from vcd.gtkw import GTKWSave

def gen_gtkw_group(gtkw, gname, bit_signals, multibit_signals, nbits):

    with gtkw.group( gname ):
        multibit_signals_o = []
        for s in multibit_signals:
            multibit_signals_o.append( s + '[%d:0]' % (nbits-1) )

        signals = bit_signals + multibit_signals_o
        for s in signals:
            gtkw.trace( gname + s)

def gen_gtkw(fname = 'tb.gtkw', groups = [], nbits = 4):
    """
    groups = []

    # pwm mod
    groups.append(
        {
        'gname'            : 'tb.pwm.',
        'bit_signals'      : ['clk', 'resetn', 'pwm_o'],
        'multibit_signals' : ['inval', 'count']
        }
    )
    """

    fh = open(fname, "w")
    gtkw = GTKWSave(fh)

    for g in groups:
        gen_gtkw_group(gtkw, g['gname'], g['bit_signals'], g['multibit_signals'], nbits)

    pass

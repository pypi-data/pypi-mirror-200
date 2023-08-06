import argparse, os, re, platform, glob
import matplotlib.pyplot as plt
import numpy as np
from rescupybs import plots, functions
from rescupy.utils import read_field
from rescupybs import __version__

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams["mathtext.fontset"] = 'cm'

def main():
    parser = argparse.ArgumentParser(description='Plot the band structure from rescuplus calculation result *.json file',
                                     epilog='''
Example:
rescupybs -y -0.5 0.5 -b
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version",    action="version",      version="rescupybs "+__version__+" from "+os.path.dirname(__file__)+' (python'+platform.python_version()+')')
    parser.add_argument('-s', "--size",       type=float, nargs=2,   help='figure size: width, height')
    parser.add_argument('-b', "--divided",    action='store_true',   help="plot the up and down spin in divided subplot")
    parser.add_argument('-y', "--vertical",   type=float, nargs=2,   help="vertical axis")
    parser.add_argument('-g', "--legend",     type=str,  nargs=1,    help="legend labels")
    parser.add_argument('-a', "--location",   type=str.lower,        default='best',
                                                                     choices=['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center'],
                                                                     help="arrange the legend location, default best")
    parser.add_argument('-k', "--linestyle",  type=str, nargs='+',   default=['-'],
                                                                     help="linestyle: solid, dashed, dashdot, dotted or tuple; default solid")
    parser.add_argument('-W', "--linewidth",  type=str, nargs='+',   default=['0.8'], help="linewidth, default 0.8")
    parser.add_argument('-c', "--color",      type=str,              nargs='+', default=[],
                                                                     help="plot colors: b, blue; g, green; r, red; c, cyan; m, magenta; y, yellow; k, black; w, white")
    parser.add_argument('-m', "--modify",     type=int, nargs=2,     help='modify the bands overlap, the up or nonispin bands to exchange values')
    parser.add_argument('-n', "--nbands",     type=int, nargs=2,     help='the down bands to exchange values')
    parser.add_argument('-i', "--input",      type=str,              nargs='+', default=[], help="plot figure from .json or .dat file")
    parser.add_argument('-o', "--output",     type=str,              default="BAND.png", help="plot figure filename")
    parser.add_argument('-K', "--kpt",        type=int,              default=0, help="The kpoint in wavefunctions")
    parser.add_argument('-B', "--band",       type=int,              default=0, help="The band in wavefunctions")
    parser.add_argument('-S', "--spin",       type=int,              default=1, help="The up or down spin in wavefunctions")
    parser.add_argument('-l', "--labels",     type=str.upper,        nargs='+', default=[], help='labels for high-symmetry points')
    parser.add_argument('-f', "--font",       type=str,              default='STIXGeneral', help="font to use")

    args = parser.parse_args()

    labels_f = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', re.sub('^GA[A-Z]+$|^G$', 'Γ', i))) for i in args.labels]
    linestyle = []
    for i in args.linestyle:
        if len(i) > 2 and i[0] == '(' and i[-1] == ')':
            linestyle.append(eval(i))
        elif len(i.split('*')) == 2:
            j = i.split('*')
            linestyle = linestyle + [j[0]] * int(j[1])
        else:
            linestyle.append(i)

    linewidth = []
    for i in args.linewidth:
        if len(i.split('*')) == 2:
            j = i.split('*')
            linewidth = linewidth + [float(j[0])] * int(j[1])
        else:
            linewidth.append(float(i))

    color = []
    for i in args.color:
        j = i.split('*')
        if len(j) == 2:
            color = color + [j[0]] * int(j[1])
        else:
            color.append(i)

    if not args.vertical:
        vertical = [-5.0, 5.0]
    else:
        vertical = args.vertical

    plt.rcParams['font.family'] = '%s'%args.font
    pltname = os.path.split(os.getcwd())[-1]
    if not args.input:
        input = ['nano_bs_out.json']
        if not os.path.exists(input[0]):
            raise Exception("The input file does not exist.")
    else:
        input = [f for i in args.input for f in glob.glob(i)]
        if not input:
            raise Exception("The input file does not exist.")

    if len(input) == 1:
        if input[0].rsplit('.', 1)[-1].lower() == 'json':
            if 'bs' in input[0].split('_'):
                bs_file = input[0]
                eigenvalues, chpts, labels = functions.bs_json_read(bs_file)
                if labels_f:
                    labels = labels_f
                legend = args.legend
                if not legend:
                    legend = [pltname]
                if len(chpts) > len(labels):
                    labels = labels + [''] * (len(chpts) - len(labels))
                elif len(chpts) < len(labels):
                    labels = labels[:len(chpts)]
                if len(eigenvalues) == 1:
                    plots.Nispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)
                elif len(eigenvalues) == 2 and not args.divided:
                    plots.Ispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)
                elif len(eigenvalues) == 2 and args.divided:
                    plots.Dispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)
            elif 'wvf' in input[0].split('_'):
                functions.isosurfaces_wf(input[0], args.kpt, args.band, args.spin)

        elif input[0].rsplit('.', 1)[-1].lower() == 'dat':
            eigenvalues = functions.bs_dat_read(input)
            chpts, labels, vbm_cbm = functions.labels_read("LABELS")
            if labels_f:
                labels = labels_f
            legend = args.legend
            if not legend:
                legend = [pltname]
            if len(chpts) > len(labels):
                labels = labels + [''] * (len(chpts) - len(labels))
            elif len(chpts) < len(labels):
                labels = labels[:len(chpts)]
            if args.modify:
                if args.modify[0] != args.modify[1]:
                    functions.exchange(eigenvalues[0,:,args.modify[0]], eigenvalues[0,:,args.modify[1]])
                    np.savetxt(input[0], eigenvalues[0])
                plots.Mnispin(args.output, args.size, vertical, eigenvalues, chpts, labels, vbm_cbm, linestyle, linewidth)
            else:
                plots.Nispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)

    else:
        Extension = [f.rsplit('.', 1)[-1].lower() for f in input]
        if all(x == Extension[0] for x in Extension):
            if len(input) == 2 and Extension[0] == 'dat':
                eigenvalues = functions.bs_dat_read(input)
                chpts, labels, vbm_cbm = functions.labels_read("LABELS")
                if labels_f:
                    labels = labels_f
                legend = args.legend
                if not legend:
                    legend = [pltname]
                if len(chpts) > len(labels):
                    labels = labels + [''] * (len(chpts) - len(labels))
                elif len(chpts) < len(labels):
                    labels = labels[:len(chpts)]
                if args.modify or args.nbands:
                    if args.modify and args.modify[0] != args.modify[1]:
                        functions.exchange(eigenvalues[0,:,args.modify[0]], eigenvalues[0,:,args.modify[1]])
                        np.savetxt(input[0], eigenvalues[0])
                    if args.nbands and args.nbands[0] != args.nbands[1]:
                        functions.exchange(eigenvalues[0,:,args.nbands[0]], eigenvalues[0,:,args.nbands[1]])
                        np.savetxt(input[1], eigenvalues[1])
                    plots.Mispin(args.output, args.size, vertical, eigenvalues, chpts, labels, vbm_cbm, linestyle, linewidth)
                else:
                    if len(eigenvalues) == 2 and not args.divided:
                        plots.Ispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)
                    elif len(eigenvalues) == 2 and args.divided:
                        plots.Dispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)
            elif Extension[0] == 'json' and all('bs' in f.split('_') for f in input):
                eigenvalues, chpts, labels = functions.bs_json_read_all(input)
                if labels_f:
                    labels = labels_f
                legend = args.legend
                if not legend:
                    legend = [pltname]
                if len(chpts) > len(labels):
                    labels = labels + [''] * (len(chpts) - len(labels))
                elif len(chpts) < len(labels):
                    labels = labels[:len(chpts)]
                if len(eigenvalues) == 1:
                    plots.Nispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)
                elif len(eigenvalues) == 2 and not args.divided:
                    plots.Ispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)
                elif len(eigenvalues) == 2 and args.divided:
                    plots.Dispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)
        else:
            raise Exception("The input files mismatch.")



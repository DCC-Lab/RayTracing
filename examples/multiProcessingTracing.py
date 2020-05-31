import envexamples
import time
import numpy

from raytracing import *
from matplotlib import pyplot, patches

fobj, backaperture = 5., 5.

if __name__ == "__main__":

    reps = 1
    processes = None

    path = ImagingPath()

    # Objective
    space = fobj
    path.append(Space(d=space))
    path.append(Lens(f=fobj, diameter=backaperture))
    path.append(Space(d=fobj))
    path.append(Space(d=space))
    path.append(Lens(f=fobj, diameter=backaperture))
    path.append(Space(d=fobj))
    path.append(Space(d=space))
    path.append(Lens(f=fobj, diameter=backaperture))
    path.append(Space(d=fobj))
    path.append(Space(d=space))
    path.append(Lens(f=fobj, diameter=backaperture))
    path.append(Space(d=fobj))
    path.append(Space(d=space))
    path.append(Lens(f=fobj, diameter=backaperture))
    path.append(Space(d=fobj))
    path.append(Space(d=space))
    path.append(Lens(f=fobj, diameter=backaperture))
    path.append(Space(d=fobj))
    path.append(Space(d=space))
    path.append(Lens(f=fobj))
    path.append(Space(d=fobj))

    test_functions = {
        "naive" : path.traceManyThrough,
        "chunks-multiprocessing" : path.traceManyThroughInParallel,
        "one-block-multiprocessing" : path.traceManyThroughInParallelNoChunks
    }

    fig, ax = pyplot.subplots()
    width = 1 / (len(test_functions) + 1)
    possible_rays = [1e+2, 1e+3, 1e+4,1e+5]
    for i, nRays in enumerate(possible_rays):
        nRays = int(nRays)
        inputRays = RandomUniformRays(yMax=0, maxCount=nRays)
        output = {}
        for name, func in test_functions.items():
            times = []
            for _ in range(reps):
                start = time.time()
                try:
                    outputRays = func(inputRays, processes=processes)
                except TypeError:
                    outputRays = func(inputRays)
                times.append(time.time() - start)
            output[name] = times
        xs = i + numpy.arange(len(test_functions)) / (len(test_functions) + 1)
        ax.bar(xs, [numpy.mean(values) for values in output.values()],
                yerr=[numpy.std(values) for values in output.values()],
                width=width, align="edge", color=["tab:blue", "tab:orange", "tab:green", "tab:red"])
    ax.set(
        xticks = numpy.arange(len(possible_rays)) + len(test_functions) * width / 2,
        xticklabels = [f"{int(nRays)}" for nRays in possible_rays],
        xlabel = "Number of propagated rays",
        ylabel = "Calculation time (s)"
    )
    ax.legend(handles = [patches.Patch(facecolor=color, label='Color Patch') for color in ["tab:blue", "tab:orange", "tab:green", "tab:red"]],
                labels = list(test_functions.keys()))
    fig.savefig("parallel_time_smallcounts.pdf", transparent=True, bbox_inches="tight")
    pyplot.show()

    ######################################################################
    # Uncomment the following lines to calculate for more rays
    ######################################################################

    # fig, ax = pyplot.subplots()
    # width = 1 / (len(test_functions) + 1)
    # possible_rays = [1e+5, 1e+6]
    # for i, nRays in enumerate(possible_rays):
    #     nRays = int(nRays)
    #     inputRays = RandomUniformRays(yMax=0, maxCount=nRays)
    #     output = {}
    #     for name, func in test_functions.items():
    #         times = []
    #         for _ in range(reps):
    #             start = time.time()
    #             outputRays = func(inputRays)
    #             times.append(time.time() - start)
    #         output[name] = times
    #     xs = i + numpy.arange(len(test_functions)) / (len(test_functions) + 1)
    #     ax.bar(xs, [numpy.mean(values) for values in output.values()],
    #             yerr=[numpy.std(values) for values in output.values()],
    #             width=width, align="edge", color=["tab:blue", "tab:orange", "tab:green", "tab:red"])
    # ax.set(
    #     xticks = numpy.arange(len(possible_rays)) + len(test_functions) * width / 2,
    #     xticklabels = [f"{int(nRays)}" for nRays in possible_rays],
    #     xlabel = "Number of propagated rays",
    #     ylabel = "Calculation time (s)"
    # )
    # ax.legend(handles = [patches.Patch(facecolor=color, label='Color Patch') for color in ["tab:blue", "tab:orange", "tab:green", "tab:red"]],
    #             labels = list(test_functions.keys()))
    # fig.savefig("parallel_time.pdf", transparent=True, bbox_inches="tight")
    # pyplot.show()

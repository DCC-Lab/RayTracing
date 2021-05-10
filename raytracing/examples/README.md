# RayTracing examples

by Prof. [Daniel Côté](mailto:dccote@cervo.ulaval.ca?subject=Raytracing%20python%20module) and his group http://www.dcclab.ca

The publication is available here:

> ["Tools and tutorial on practical ray tracing for microscopy"](https://doi.org/10.1117/1.NPh.8.1.010801) 
>
> by V. Pineau Noël*, S. Masoumi*, E. Parham*, G. Genest, L. Bégin, M.-A. Vigneault, D. C. Côté, 
> Neurophotonics, 8(1), 010801 (2021). 
> *Equal contributions.
> Permalink: https://doi.org/10.1117/1.NPh.8.1.010801

## Listing the examples

The present directory contains a large number of examples.  Some are short and show how to use the raytracing module for simple tasks.  They start with the prefix `ex`. Others are longer and perform more than just a simple trace and display a graph: they use Monte Carlo, the get values from functions and perform other calculations, etc... Finally, the scripts that generated the figures from the article cited above start with the prefix `fig` and end with `.py`. Finally, some files are simply the actual figures (`.png`) if they were not calculated.

This will show you a list of examples of things you can do:

```shell
python -m raytracing -l           # List examples
python -m raytracing -e all       # Run all of them
python -m raytracing -e 1,2,4,6   # Only run 1,2,4 and 6
python -m raytracing -f 5,6,7.    # Run scripts that generated figures 5,6 and 7 in article
```

or request help with:

```shell
python -m raytracing -h
```

## Licence

This code is provided under the [MIT License](./LICENSE).
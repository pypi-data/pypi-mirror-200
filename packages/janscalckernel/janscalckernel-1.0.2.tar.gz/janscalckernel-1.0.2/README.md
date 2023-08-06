# janscalckernel

![Logo](https://raw.githubusercontent.com/jans-code/janscalckernel/main/janscalckernel/logo-svg.svg)

A simple and robust jupyter kernel implementation of [calc](http://www.isthe.com/chongo/tech/comp/calc/), because sometimes you just want to calculate.

## Installation

- install calc from your distro's package manager or from [here](https://github.com/lcn2/calc/releases).
- get the kernel module via pip
- `pip install janscalckernel`
- then install kernelspec
- `janscalckernel`

## Dev Installation

- download/clone this project
- open shell in project folder
- `pip install -e ./`
- `jupyter kernelspec install --user janscalckernel`

## Uninstall

- `jupyter kernelspec uninstall janscalckernel`
- `pip uninstall janscalckernel`

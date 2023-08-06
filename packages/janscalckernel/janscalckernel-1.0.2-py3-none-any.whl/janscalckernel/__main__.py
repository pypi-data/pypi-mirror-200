#!/usr/bin/env python
# *_* coding: utf-8 *_*

"""calc kernel main"""

from ipykernel.kernelapp import IPKernelApp
from .kernel import janscalckernel
IPKernelApp.launch_instance(kernel_class=janscalckernel)

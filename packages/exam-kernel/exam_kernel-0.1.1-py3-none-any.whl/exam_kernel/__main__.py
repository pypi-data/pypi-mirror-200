from ipykernel.kernelapp import IPKernelApp
from . import ExamKernel

IPKernelApp.launch_instance(kernel_class=ExamKernel)

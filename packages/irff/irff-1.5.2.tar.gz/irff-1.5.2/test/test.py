#!/usr/bin/env python
from train import train_reax
from GeometryOptimization import geo_opt
from md import moleculardynamics
from StaticCompress import static_compress

geo_opt()
moleculardynamics()
# static_compress()
train_reax(step=1000)

from congen.layers.rasterLayers import SimplexNoiseLayer
from congen.layers.graphLayers.FullGraphLayer import FullGraphLayer
from congen.layers.graphLayers.GraphLayer import GraphLayer
from congen.layers.pointLayers.clustered.KMeansClusteredPointLayer import KMeansClusteredPointLayer
from src.congen.layers.graphLayers.RandomGraphLayer import RandomGraphLayer
from congen.layers.rasterLayers.SimplexNoiseLayer import SimplexNoiseLayer
from congen.layers.rasterLayers.PerlinNoiseLayer import PerlinNoiseLayer
from congen.layers.rasterLayers.PointRasterLayer import PointRasterLayer
from congen.layers.pointLayers.RasterPointLayer import RasterPointLayer
from congen.layers.pointLayers.SimpleRandomPointLayer import SimpleRandomPointLayer
from congen.layers.pointLayers.StratifiedRandomPointLayer import StratifiedRandomPointLayer
from congen.layers.rasterLayers.ImportedRasterLayer import ImportedRasterLayer


def create_multilayer_class(*superclasses):
    class MultilayerClass(*superclasses):
        def __init__(self, **kwargs):
            for superclass in superclasses:
                superclass.__init__(self, **kwargs)
        def calculate(self):
            self.generator = None
            for superclass in superclasses:
                superclass.calculate(self)

        def draw(self, axes):
            for superclass in superclasses:
                if hasattr(superclass, "draw"):
                    superclass.draw(self, axes)

    return MultilayerClass


layer_names = {
    "Perlin": PerlinNoiseLayer,
    "Simplex": SimplexNoiseLayer,
    "SimpleRandomPointLayer": SimpleRandomPointLayer,
    "StratifiedRandomPointLayer": StratifiedRandomPointLayer,
    "RasterPointLayer": RasterPointLayer,
    "KMeansClusteredPointLayer": KMeansClusteredPointLayer,
    "FullGraphLayer": FullGraphLayer,
    "RandomGraphLayer": RandomGraphLayer,
    "ImportedRasterLayer": ImportedRasterLayer,
}

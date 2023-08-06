from src.congen.importers import GeoTIFFImporter

importer_names = {importer.__name__: importer for importer in [GeoTIFFImporter]}
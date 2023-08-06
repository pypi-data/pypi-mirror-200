from numpy import array
from dataclasses import dataclass

@dataclass
class ProcessedFamily:
    fid: str
    is_mother_phased: bool
    mother: array
    maternal_haplotypes: array

from peptides import Peptide


class Pep:
    def __init__(self, seq: str) -> None:
        self.peptide = Peptide(seq)

    @property
    def vhse_scales(self):
        return self.peptide.vhse_scales()

    @property
    def z_scales(self):
        return self.peptide.z_scales()

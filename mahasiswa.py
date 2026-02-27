class Mahasiswa:
    def __init__(self, nama, nilai):
        self.nama = nama
        self.nilai = nilai

    def cek_lulus(self):
        return "Lulus" if self.nilai >= 75 else "Tidak Lulus"

    def __str__(self):
        return f"{self.nama} - {self.nilai} - {self.cek_lulus()}"
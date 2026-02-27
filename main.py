from mahasiswa_model import MahasiswaModel

while True:
    print("\n=== menu ===")
    print("1. Tambah Mahasiswa")
    print("2. Lihat Data")
    print("3. Hapus Data")
    print("4. Keluar")

    pilih = input("pilih")

    if pilih == "1":
        nama = input("nama: ")
        nilai = int(input("nilai: "))
        MahasiswaModel.tambah(nama, nilai)

    elif pilih == "2":
        data = MahasiswaModel.semua()
        for mhs in data:
            print(f"{mhs['id']}" - 
                  {mhs['nama']} - {mhs['nilai']})

    elif pilih == "3":
        id = input("ID yang dihapus: ")
        MahasiswaModel.hapus(id)

    elif pilih == "4":
        break

    else:
        print("pilihan tidak valid") 
            
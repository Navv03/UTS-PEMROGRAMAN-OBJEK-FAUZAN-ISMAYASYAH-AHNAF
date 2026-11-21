# =====================================================================
# PROJECT SISTEM RENTAL KENDARAAN (PYTHON OOP)
# =====================================================================


# ---------------------------------------------------------------------
# CLASS 1: Kendaraan (Kelas Utama Unit Rental)
# ---------------------------------------------------------------------
class Kendaraan:
    # Class Attribute (berlaku untuk semua objek Kendaraan)
    pajak_ppn = 0.11  # PPN 11%

    # 1. Constructor __init__()
    def __init__(self, kode: str, nama: str, plat_nomor: str, harga_per_hari: int):
        # Public Attributes
        self.kode = kode
        self.nama = nama
        self.plat_nomor = plat_nomor

        # 2. Encapsulation (Private Attributes dengan awalan __)
        self.__harga_per_hari = harga_per_hari
        self.__tersedia = True

    # 3. @property (Getter) & Setter untuk harga_per_hari
    @property
    def harga_per_hari(self) -> int:
        return self.__harga_per_hari

    @harga_per_hari.setter
    def harga_per_hari(self, harga_baru: int):
        if harga_baru <= 0:
            raise ValueError("Harga sewa harus lebih besar dari Rp0!")
        self.__harga_per_hari = harga_baru

    # @property (Getter) & Setter untuk status tersedia
    @property
    def tersedia(self) -> bool:
        return self.__tersedia

    @tersedia.setter
    def tersedia(self, status_baru: bool):
        if not isinstance(status_baru, bool):
            raise ValueError("Status ketersediaan harus berupa True atau False!")
        self.__tersedia = status_baru

    # 4. Instance Methods (Perilaku Objek)
    def hitung_biaya_sewa(self, jumlah_hari: int) -> int:
        subtotal = self.__harga_per_hari * jumlah_hari
        total = int(subtotal + (subtotal * self.pajak_ppn))
        return total

    def info_kendaraan(self) -> str:
        status_teks = "Tersedia" if self.__tersedia else "Sedang Disewa"
        harga_terformat = self.format_rupiah(self.__harga_per_hari)
        return (
            f"[{self.kode}] {self.nama} ({self.plat_nomor}) | "
            f"{harga_terformat}/hari | Status: {status_teks}"
        )

    # 5. @classmethod (Berinteraksi dengan Class 'cls')
    @classmethod
    def dari_string(cls, data_teks: str):
        """Alternative constructor untuk membuat objek dari string dipisah tanda '|'."""
        kode, nama, plat, harga = data_teks.split("|")
        return cls(kode.strip(), nama.strip(), plat.strip(), int(harga.strip()))

    @classmethod
    def ubah_pajak_ppn(cls, tarif_baru: float):
        """Mengubah tarif PPN untuk seluruh unit kendaraan sekaligus."""
        if tarif_baru < 0:
            raise ValueError("Tarif pajak tidak boleh negatif!")
        cls.pajak_ppn = tarif_baru

    # 6. @staticmethod (Fungsi bantuan tanpa akses ke 'self' maupun 'cls')
    @staticmethod
    def format_rupiah(nominal: int) -> str:
        return f"Rp{nominal:,.0f}".replace(",", ".")

    @staticmethod
    def validasi_hari(jumlah_hari: int) -> bool:
        return jumlah_hari >= 1


# ---------------------------------------------------------------------
# CLASS 2: Mobil (Pewarisan / Inheritance dari Kendaraan)
# ---------------------------------------------------------------------
class Mobil(Kendaraan):
    def __init__(self, kode: str, nama: str, plat_nomor: str, harga_per_hari: int, jumlah_kursi: int):
        super().__init__(kode, nama, plat_nomor, harga_per_hari)
        self.jumlah_kursi = jumlah_kursi

    def info_kendaraan(self) -> str:
        info_dasar = super().info_kendaraan()
        return f"{info_dasar} | Kapasitas: {self.jumlah_kursi} Kursi"


# ---------------------------------------------------------------------
# CLASS 3: SistemRental (Pengelola Daftar Unit & Transaksi)
# ---------------------------------------------------------------------
class SistemRental:
    def __init__(self, nama_usaha: str):
        self.nama_usaha = nama_usaha
        # Encapsulation pada daftar unit
        self.__daftar_unit: list[Kendaraan] = []

    def tambah_unit(self, unit: Kendaraan):
        self.__daftar_unit.append(unit)

    def cari_unit(self, kode: str) -> Kendaraan | None:
        for unit in self.__daftar_unit:
            if unit.kode.upper() == kode.upper():
                return unit
        return None

    def tampilkan_katalog(self):
        ppn_persen = int(Kendaraan.pajak_ppn * 100)
        print(f"\n=== KATALOG {self.nama_usaha.upper()} (PPN {ppn_persen}%) ===")
        if not self.__daftar_unit:
            print("Belum ada unit kendaraan terdaftar.")
            return
        for unit in self.__daftar_unit:
            print(unit.info_kendaraan())

    def proses_sewa(self, nama_penyewa: str, kode_unit: str, lama_sewa: int):
        # Memanggil @staticmethod
        if not Kendaraan.validasi_hari(lama_sewa):
            print("Error: Lama sewa minimal 1 hari.")
            return

        unit = self.cari_unit(kode_unit)
        if unit is None:
            print("Error: Kode kendaraan tidak ditemukan.")
            return

        # Memanggil @property tersedia
        if not unit.tersedia:
            print("Maaf, unit tersebut sedang disewa oleh pelanggan lain.")
            return

        total_bayar = unit.hitung_biaya_sewa(lama_sewa)
        # Memanggil @tersedia.setter
        unit.tersedia = False

        print("\n--- STRUK PENYEWAAN BERHASIL ---")
        print(f"Penyewa     : {nama_penyewa}")
        print(f"Unit        : {unit.nama} ({unit.plat_nomor})")
        print(f"Durasi Sewa : {lama_sewa} hari")
        print(f"Total Bayar : {Kendaraan.format_rupiah(total_bayar)} (termasuk PPN)")
        print("--------------------------------")

    def proses_pengembalian(self, kode_unit: str):
        unit = self.cari_unit(kode_unit)
        if unit is None:
            print("Error: Kode kendaraan tidak ditemukan.")
            return

        if unit.tersedia:
            print("Info: Unit ini berstatus tersedia (tidak sedang disewa).")
            return

        # Memanggil @tersedia.setter
        unit.tersedia = True
        print(f"Berhasil: {unit.nama} [{unit.kode}] telah dikembalikan.")


# =====================================================================
# PROGRAM UTAMA (PEMBUATAN OBJECT & INTERAKSI MENU)
# =====================================================================
def main():
    # Membuat Object dari Class SistemRental
    rental = SistemRental("Nusantara Rent")

    # Membuat Object dari Class Mobil & Kendaraan
    unit1 = Mobil("MBL-01", "Toyota Avanza", "B 1024 KLA", 350000, 7)
    unit2 = Mobil("MBL-02", "Honda Brio", "B 2048 XYZ", 300000, 5)

    # Membuat Object menggunakan @classmethod (dari_string)
    unit3 = Kendaraan.dari_string("MTR-01 | Yamaha NMAX | B 3099 ABC | 120000")

    # Mendaftarkan object ke sistem rental
    rental.tambah_unit(unit1)
    rental.tambah_unit(unit2)
    rental.tambah_unit(unit3)

    while True:
        print("\n==========================================")
        print("      APLIKASI SISTEM RENTAL PYTHON       ")
        print("==========================================")
        print("1. Lihat Daftar Kendaraan")
        print("2. Sewa Kendaraan")
        print("3. Kembalikan Kendaraan")
        print("4. Ubah Harga Sewa Unit (Demo Setter)")
        print("5. Ubah Tarif PPN (Demo Class Method)")
        print("6. Keluar")

        pilihan = input("Pilih menu (1-6): ").strip()

        if pilihan == "1":
            rental.tampilkan_katalog()

        elif pilihan == "2":
            rental.tampilkan_katalog()
            nama = input("\nNama penyewa: ").strip()
            kode = input("Kode kendaraan (contoh: MBL-01): ").strip()
            try:
                hari = int(input("Lama sewa (hari): "))
                rental.proses_sewa(nama, kode, hari)
            except ValueError:
                print("Error: Lama sewa harus berupa angka bulat.")

        elif pilihan == "3":
            kode = input("Masukkan kode kendaraan yang dikembalikan: ").strip()
            rental.proses_pengembalian(kode)

        elif pilihan == "4":
            kode = input("Masukkan kode kendaraan: ").strip()
            unit = rental.cari_unit(kode)
            if unit:
                print(f"Harga saat ini: {Kendaraan.format_rupiah(unit.harga_per_hari)}")
                try:
                    harga_baru = int(input("Masukkan harga sewa baru: "))
                    # Memanggil @harga_per_hari.setter
                    unit.harga_per_hari = harga_baru
                    print("Harga sewa berhasil diperbarui!")
                except ValueError as e:
                    print(f"Gagal mengubah harga: {e}")
            else:
                print("Error: Kode kendaraan tidak ditemukan.")

        elif pilihan == "5":
            try:
                ppn_baru = float(input("Masukkan tarif PPN baru (contoh: 0.12 untuk 12%): "))
                # Memanggil @classmethod ubah_pajak_ppn
                Kendaraan.ubah_pajak_ppn(ppn_baru)
                print(f"Tarif PPN berhasil diubah menjadi {int(Kendaraan.pajak_ppn * 100)}%.")
            except ValueError as e:
                print(f"Gagal mengubah PPN: {e}")

        elif pilihan == "6":
            print("Program selesai. Terima kasih!")
            break

        else:
            print("Pilihan tidak valid. Silakan pilih angka 1 sampai 6.")


if __name__ == "__main__":
    main()
import sqlite3
import os

# Bakkal sınıfı tanımlanıyor
# TODO ürün listeleme özelliğine şekillendirme yapılacak

class Bakkal:
    # Veritabanı adı alınarak bir bağlantı oluşturuluyor ve cursor oluşturuluyor
    # Eğer "urunler" tablosu yoksa oluşturuluyor
    def __init__(self, veritabani_adi):
        self.veritabani_adi = veritabani_adi
        self.conn = sqlite3.connect(veritabani_adi)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS urunler (
                urun_ad TEXT,
                fiyat REAL,
                stok_adet INTEGER
            );
        """)

    # Yeni bir ürün eklemek için kullanılan fonksiyon
    def urun_ekle(self, urun_ad, fiyat, stok_adet):
        # Yeni ürünün veritabanına eklenmesi
        self.cursor.execute("INSERT INTO urunler (urun_ad, fiyat, stok_adet) VALUES (?, ?, ?)",
                            (urun_ad, fiyat, stok_adet))
        # Kullanıcıya ekleme işleminin başarılı olduğu bilgisi veriliyor
        print(f"{urun_ad} ürünü başarıyla eklendi.")
        # Veritabanı güncelleniyor
        self.conn.commit()

    # Var olan bir ürünü silmek için kullanılan fonksiyon
    def urun_sil(self, urun_ad):
        # Veritabanından ürün siliniyor
        self.cursor.execute("DELETE FROM urunler WHERE urun_ad=?", (urun_ad,))
        # Kullanıcıya silme işleminin başarılı olduğu bilgisi veriliyor
        print(f"{urun_ad} ürünü başarıyla silindi.")
        # Veritabanı güncelleniyor
        self.conn.commit()

    # Var olan bir ürüne stok eklemek için kullanılan fonksiyon
    def stok_ekle(self, urun_ad, eklenecek_stok):
        # Mevcut stok adeti alınıyor
        self.cursor.execute(
            "SELECT stok_adet FROM urunler WHERE urun_ad=?", (urun_ad,))
        mevcut_stok_miktari = self.cursor.fetchone()[0]
        # Yeni stok adeti hesaplanıyor ve veritabanına kaydediliyor
        yeni_stok_miktari = mevcut_stok_miktari + eklenecek_stok
        self.cursor.execute(
            "UPDATE urunler SET stok_adet=? WHERE urun_ad=?", (yeni_stok_miktari, urun_ad))
        # Kullanıcıya stok güncelleme işleminin başarılı olduğu bilgisi veriliyor
        print(f"{urun_ad} ürününün stok adeti {eklenecek_stok} kadar arttırıldı.")
        # Veritabanı güncelleniyor
        self.conn.commit()

    def stok_guncelle(self, urun_ad, yeni_stok_miktari):
        # Veritabanında ilgili ürünün stok adetini güncellemek için SQL sorgusu oluşturulur
        self.cursor.execute(
            "UPDATE urunler SET stok_adet=? WHERE urun_ad=?", (yeni_stok_miktari, urun_ad))
        # Kullanıcıya güncelleme işleminin tamamlandığına dair bir mesaj gösterilir
        print(f"{urun_ad} ürününün stok adeti {yeni_stok_miktari} olarak güncellendi.")
        # Yapılan güncelleme işleminin veritabanına yansıması için işlem tamamlanır
        self.conn.commit()

    def urunleri_listele(self):
        # Tüm ürünleri veritabanından seç ve al
        self.cursor.execute("SELECT * FROM urunler")
        urunler = self.cursor.fetchall()
        # Eğer hiç ürün yoksa, bilgi mesajı yazdır
        if len(urunler) == 0:
            print("Mevcut ürün bulunmamaktadır.")
        else:
            # Tüm ürünlerin listesini yazdır
            print("Mevcut ürünler:")
            for urun in urunler:
                print(
                    f" Ürün Adı: {urun[0]}\n Fiyat: {urun[1]} TL\n Stok Adeti: {urun[2]}\n")

    def fiyat_guncelle(self, urun_ad, yeni_fiyat):
        # Veritabanında ilgili ürünün fiyatını güncellemek için SQL sorgusu oluşturuluyor
        self.cursor.execute(
            "UPDATE urunler SET fiyat=? WHERE urun_ad=?", (yeni_fiyat, urun_ad))
        # Kullanıcıya güncelleme işleminin tamamlandığına dair bir mesaj gösterilir
        print(f"{urun_ad} ürününün fiyatı {yeni_fiyat} olarak güncellendi.")
        # Yapılan güncelleme işleminin veritabanına yansıması için işlem tamamlanır
        self.conn.commit()

    def konsol_temizle(self):
        # Windows işletim sistemi için
        if os.name == 'nt':
            os.system('cls')
        # Mac/Linux işletim sistemleri için
        else:
            os.system('clear')

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    bakkalim = Bakkal("bakkal.db")
    bakkalim.konsol_temizle()
    while True:
        print(
            """
            Lütfen yapmak istediğiniz işlemi seçiniz:
            1 - Ürün ekle
            2 - Ürün sil
            3 - Stok ekle
            4 - Stok güncelle
            5 - Fiyat güncelle
            6 - Ürünleri Listele
            0 - Çıkış yap
            """
        )
        islem = input("Yapmak istediğiniz işlemin numarasını girin: ")
        if islem == "1":
            urun_ad = input("Eklemek istediğiniz ürünün adı: ")
            fiyat = float(input(f"{urun_ad} ürününün fiyatı: "))
            stok_adet = int(
                input(f"{urun_ad} ürününden kaç adet eklemek istiyorsunuz: "))
            bakkalim.konsol_temizle()
            bakkalim.urun_ekle(urun_ad, fiyat, stok_adet)
        elif islem == "2":
            urun_ad = input("Silmek istediğiniz ürünün adı: ")
            bakkalim.konsol_temizle()
            bakkalim.urun_sil(urun_ad)
        elif islem == "3":
            urun_ad = input("Stok eklemek istediğiniz ürünün adı: ")
            eklenecek_stok = int(
                input(f"{urun_ad} ürününe kaç adet stok eklemek istiyorsunuz: "))
            bakkalim.konsol_temizle()
            bakkalim.stok_ekle(urun_ad, eklenecek_stok)
        elif islem == "4":
            urun_ad = input("Güncellemek istediğiniz ürünün adı: ")
            yeni_stok_miktari = int(
                input(f"{urun_ad} ürününün yeni stok miktarı: "))
            bakkalim.konsol_temizle()
            bakkalim.stok_guncelle(urun_ad, yeni_stok_miktari)
        elif islem == "5":
            urun_ad = input("Güncellemek istediğiniz ürünün adı: ")
            urun_fiyat = input("Güncellemek istediğiniz ürünün yeni fiyatı: ")
            bakkalim.konsol_temizle()
            bakkalim.fiyat_guncelle(urun_ad, urun_fiyat)
        elif islem == "6":
            bakkalim.konsol_temizle()
            bakkalim.urunleri_listele()
        elif islem == "0":
            print("Program kapatılıyor...")
            break
        else:
            print("Lütfen geçerli bir işlem numarası girin.")

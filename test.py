"""
Basit Yapılacaklar Listesi (To-Do) Uygulaması
Görevleri ekleyebilir, listeleyebilir, tamamlayabilir ve silebilirsiniz.
Veriler todo_data.json dosyasında saklanır.
"""

import json
import os
from datetime import datetime

DOSYA_ADI = "todo_data.json"


def gorevleri_yukle():
    """JSON dosyasından görevleri yükler."""
    if not os.path.exists(DOSYA_ADI):
        return []
    try:
        with open(DOSYA_ADI, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def gorevleri_kaydet(gorevler):
    """Görevleri JSON dosyasına kaydeder."""
    with open(DOSYA_ADI, "w", encoding="utf-8") as f:
        json.dump(gorevler, f, ensure_ascii=False, indent=2)


def gorev_ekle(gorevler, baslik):
    """Yeni görev ekler."""
    yeni_gorev = {
        "id": len(gorevler) + 1,
        "baslik": baslik,
        "tamamlandi": False,
        "olusturulma": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }
    gorevler.append(yeni_gorev)
    gorevleri_kaydet(gorevler)
    print(f"✓ '{baslik}' eklendi.")


def gorevleri_listele(gorevler):
    """Tüm görevleri ekrana yazdırır."""
    if not gorevler:
        print("\n📋 Henüz görev yok. Yeni bir tane ekle!\n")
        return

    print("\n" + "=" * 50)
    print("📋 YAPILACAKLAR LİSTESİ")
    print("=" * 50)
    for gorev in gorevler:
        durum = "✅" if gorev["tamamlandi"] else "⬜"
        print(f"{gorev['id']:>2}. {durum} {gorev['baslik']}")
        print(f"     📅 {gorev['olusturulma']}")
    print("=" * 50 + "\n")


def gorev_tamamla(gorevler, gorev_id):
    """Görevi tamamlandı olarak işaretler."""
    for gorev in gorevler:
        if gorev["id"] == gorev_id:
            gorev["tamamlandi"] = True
            gorevleri_kaydet(gorevler)
            print(f"✓ '{gorev['baslik']}' tamamlandı.")
            return
    print(f"⚠ {gorev_id} numaralı görev bulunamadı.")


def gorev_sil(gorevler, gorev_id):
    """Görevi listeden siler."""
    for i, gorev in enumerate(gorevler):
        if gorev["id"] == gorev_id:
            silinen = gorevler.pop(i)
            # ID'leri yeniden düzenle
            for j, g in enumerate(gorevler, start=1):
                g["id"] = j
            gorevleri_kaydet(gorevler)
            print(f"🗑 '{silinen['baslik']}' silindi.")
            return
    print(f"⚠ {gorev_id} numaralı görev bulunamadı.")


def menu_goster():
    """Ana menüyü gösterir."""
    print("\n--- MENÜ ---")
    print("1. Görevleri listele")
    print("2. Yeni görev ekle")
    print("3. Görevi tamamla")
    print("4. Görevi sil")
    print("5. Çıkış")


def main():
    """Ana program döngüsü."""
    gorevler = gorevleri_yukle()
    print("👋 Yapılacaklar Listesi'ne hoş geldiniz!")

    while True:
        menu_goster()
        secim = input("Seçiminiz (1-5): ").strip()

        if secim == "1":
            gorevleri_listele(gorevler)

        elif secim == "2":
            baslik = input("Görev başlığı: ").strip()
            if baslik:
                gorev_ekle(gorevler, baslik)
            else:
                print("⚠ Boş görev eklenemez.")

        elif secim == "3":
            gorevleri_listele(gorevler)
            if gorevler:
                try:
                    gorev_id = int(input("Tamamlanacak görev numarası: "))
                    gorev_tamamla(gorevler, gorev_id)
                except ValueError:
                    print("⚠ Geçerli bir sayı girin.")

        elif secim == "4":
            gorevleri_listele(gorevler)
            if gorevler:
                try:
                    gorev_id = int(input("Silinecek görev numarası: "))
                    gorev_sil(gorevler, gorev_id)
                except ValueError:
                    print("⚠ Geçerli bir sayı girin.")

        elif secim == "5":
            print("👋 Görüşürüz!")
            break

        else:
            print("⚠ Geçersiz seçim. 1-5 arası bir sayı girin.")


if __name__ == "__main__":
    main()
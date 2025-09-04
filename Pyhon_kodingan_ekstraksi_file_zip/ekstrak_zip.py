import zipfile
from pathlib import Path

def extract_zips_to_folder(source_dir: Path, dest_dir: Path) -> None:
    """
    Mengekstrak semua file .zip dari direktori sumber ke direktori tujuan.
    Setiap file di dalam zip akan diekstrak sebagai file terpisah dengan nama unik.

    Args:
        source_dir (Path): Path ke folder yang berisi file .zip.
        dest_dir (Path): Path ke folder tujuan untuk menyimpan hasil ekstraksi.
    """
    # 1. Buat folder tujuan jika belum ada
    dest_dir.mkdir(parents=True, exist_ok=True)
    print(f"Folder tujuan '{dest_dir}' siap digunakan.")

    # 2. Iterasi semua file di dalam folder sumber
    for zip_path in source_dir.glob('*.zip'):
        print(f"\nMemproses file: {zip_path.name}...")

        try:
            # 3. Buka file zip untuk dibaca
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # 4. Iterasi semua file di dalam arsip zip
                for inner_file_info in zip_ref.infolist():
                    if inner_file_info.is_dir():
                        continue # Lewati direktori

                    # Membuat nama file baru untuk menghindari tumpang tindih
                    # Contoh: 'Chat 1.zip' berisi '_chat.txt' -> 'Chat 1__chat.txt'
                    base_zip_name = zip_path.stem
                    # Mengambil hanya nama file, bukan path lengkap di dalam zip
                    inner_filename = Path(inner_file_info.filename).name
                    new_filename = f"{base_zip_name}__{inner_filename}"
                    output_path = dest_dir / new_filename

                    # 5. Ekstrak dan tulis konten ke file baru (mode biner)
                    # Ini lebih efisien dan aman daripada decode/encode manual
                    with zip_ref.open(inner_file_info) as source_file:
                        with open(output_path, 'wb') as dest_file:
                            dest_file.write(source_file.read())
                        print(f"  -> Berhasil mengekstrak '{inner_file_info.filename}' ke '{output_path}'")

        except zipfile.BadZipFile:
            print(f"  -> GAGAL: File '{zip_path.name}' bukan file zip yang valid atau rusak.")
        except Exception as e:
            print(f"  -> ERROR: Terjadi kesalahan pada '{zip_path.name}': {e}")

if __name__ == "__main__":
    # Konfigurasi folder menggunakan pathlib.Path untuk best practice
    sumber_folder = Path("Data malam ini")
    tujuan_folder = Path("Hasil Ekstraksi Teks")

    # Periksa apakah folder sumber ada
    if not sumber_folder.is_dir():
        print(f"Error: Folder sumber '{sumber_folder}' tidak ditemukan!")
        print(f"Pastikan skrip ini dijalankan di direktori yang sama dengan folder '{sumber_folder}'.")
    else:
        extract_zips_to_folder(sumber_folder, tujuan_folder)
        print(f"\n✅ Proses ekstraksi selesai. Silakan periksa folder '{tujuan_folder}'.")

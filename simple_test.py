import time
import os
import datetime
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService

# --- KONFIGURASI AWAL ---
# List untuk menampung hasil pengujian
list_hasil_test = []

print("=== Memulai Proses Otomatisasi Pengujian Website ===")
print("Status: Menyiapkan driver browser...")

# Pengecekan driver Microsoft Edge
if os.path.exists("msedgedriver.exe"):
    service_driver = EdgeService("msedgedriver.exe")
else:
    # Menggunakan driver default sistem jika file tidak ditemukan
    service_driver = EdgeService()

# Inisialisasi browser
driver = webdriver.Edge(service=service_driver)
driver.maximize_window()
driver.implicitly_wait(10) # Waktu tunggu toleransi 10 detik

# Membuat direktori penyimpanan laporan jika belum tersedia
if not os.path.exists('reports'):
    os.makedirs('reports')
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# ==========================================
# SKENARIO 1: Pengujian Akses Menu "Who We Are"
# ==========================================
nama_skenario = "Akses Menu Navigasi 'Who We Are'"
print(f"\n[1/3] Sedang menjalankan: {nama_skenario}")

try:
    # Membuka halaman utama
    driver.get("https://indonesiaindicator.com/home")
    time.sleep(3) # Memberi jeda waktu loading
    
    # Mencari elemen menu berdasarkan teks parsial dan melakukan klik
    elemen_menu = driver.find_element(By.PARTIAL_LINK_TEXT, "Who We Are")
    elemen_menu.click()
    time.sleep(3)
    
    # Validasi URL halaman saat ini
    url_aktual = driver.current_url
    if "who" in url_aktual.lower():
        status_test = "PASS"
        keterangan = "Berhasil menavigasi ke halaman Who We Are."
        print("   -> Hasil: SUKSES")
    else:
        status_test = "FAIL"
        keterangan = f"Gagal navigasi. URL saat ini: {url_aktual}"
        print("   -> Hasil: GAGAL")

    # Pengambilan bukti tangkapan layar (Screenshot)
    waktu_skr = time.strftime("%H%M%S")
    path_gambar = f"screenshots/bukti_who_we_are_{waktu_skr}.png"
    driver.save_screenshot(path_gambar)
    
    # Menyimpan data hasil pengujian
    data_log = {
        "nama": nama_skenario,
        "status": status_test,
        "pesan": keterangan,
        "path_img": path_gambar
    }
    list_hasil_test.append(data_log)

except Exception as e:
    print(f"   -> Terjadi kesalahan sistem: {str(e)}")
    data_log = {"nama": nama_skenario, "status": "ERROR", "pesan": str(e), "path_img": ""}
    list_hasil_test.append(data_log)


# ==========================================
# SKENARIO 2: Pengujian Akses Menu "News"
# ==========================================
nama_skenario = "Akses Menu Navigasi 'News'"
print(f"\n[2/3] Sedang menjalankan: {nama_skenario}")

try:
    # Kembali ke halaman beranda untuk reset posisi
    driver.get("https://indonesiaindicator.com/home")
    time.sleep(2)

    # Mencari menu News
    elemen_menu = driver.find_element(By.PARTIAL_LINK_TEXT, "News")
    elemen_menu.click()
    time.sleep(3)
    
    # Validasi URL
    if "news" in driver.current_url.lower():
        status_test = "PASS"
        keterangan = "Berhasil menavigasi ke halaman News."
        print("   -> Hasil: SUKSES")
    else:
        status_test = "FAIL"
        keterangan = "Gagal navigasi ke halaman News."
        print("   -> Hasil: GAGAL")
        
    # Pengambilan bukti tangkapan layar
    waktu_skr = time.strftime("%H%M%S")
    path_gambar = f"screenshots/bukti_news_{waktu_skr}.png"
    driver.save_screenshot(path_gambar)
    
    data_log = {
        "nama": nama_skenario,
        "status": status_test,
        "pesan": keterangan,
        "path_img": path_gambar
    }
    list_hasil_test.append(data_log)

except Exception as e:
    print(f"   -> Terjadi kesalahan sistem: {str(e)}")
    data_log = {"nama": nama_skenario, "status": "ERROR", "pesan": str(e), "path_img": ""}
    list_hasil_test.append(data_log)


# ==========================================
# SKENARIO 3: Pengujian Ikon Sosial Media (Footer)
# ==========================================
nama_skenario = "Akses Link Sosial Media di Footer"
print(f"\n[3/3] Sedang menjalankan: {nama_skenario}")

try:
    driver.get("https://indonesiaindicator.com/home")
    time.sleep(2)
    
    # Melakukan scroll halaman hingga paling bawah (Footer)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    # Mencari ikon sosial media (Instagram atau LinkedIn) di area footer
    # Menggunakan XPATH yang fleksibel untuk mencari link href
    tombol_sosmed = driver.find_element(By.XPATH, "//a[contains(@href, 'instagram') or contains(@href, 'linkedin')]")
    
    # Klik menggunakan JavaScript untuk memastikan elemen merespons
    driver.execute_script("arguments[0].click();", tombol_sosmed)
    time.sleep(3)
    
    # Memeriksa apakah tab baru terbuka
    jendela_browser = driver.window_handles
    if len(jendela_browser) > 1:
        # Berpindah fokus ke tab baru
        driver.switch_to.window(jendela_browser[1])
        status_test = "PASS"
        keterangan = f"Tab baru berhasil terbuka: {driver.current_url}"
        print("   -> Hasil: SUKSES (Tab Baru Terbuka)")
        
        # Screenshot halaman sosial media
        waktu_skr = time.strftime("%H%M%S")
        path_gambar = f"screenshots/bukti_sosmed_open_{waktu_skr}.png"
        driver.save_screenshot(path_gambar)
        
        # Menutup tab sosial media dan kembali ke utama
        driver.close()
        driver.switch_to.window(jendela_browser[0])
    else:
        status_test = "PASS"
        keterangan = "Link diklik namun tidak membuka tab baru (Direct Link)."
        print("   -> Hasil: SUKSES (Link Terklik)")
        path_gambar = f"screenshots/bukti_sosmed_click_{time.strftime('%H%M%S')}.png"
        driver.save_screenshot(path_gambar)

    data_log = {
        "nama": nama_skenario,
        "status": status_test,
        "pesan": keterangan,
        "path_img": path_gambar
    }
    list_hasil_test.append(data_log)

except Exception as e:
    print(f"   -> Terjadi kesalahan sistem: {str(e)}")
    data_log = {"nama": nama_skenario, "status": "ERROR", "pesan": str(e), "path_img": ""}
    list_hasil_test.append(data_log)


# --- PENYELESAIAN ---
print("\n=== Pengujian Selesai. Menutup Browser... ===")
driver.quit()


# --- GENERASI LAPORAN HTML (PORTABLE) ---
print("Sedang menyusun laporan hasil pengujian...")

# Template dasar HTML
konten_html = """
<html>
<head>
<title>Laporan Hasil Pengujian Otomatis</title>
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 30px; background-color: #f4f4f4; }
    h2 { color: #333; text-align: center; }
    .info { text-align: center; color: #666; margin-bottom: 20px; }
    table { border-collapse: collapse; width: 100%; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
    th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
    th { background-color: #0078d7; color: white; }
    tr:nth-child(even) { background-color: #f9f9f9; }
    .PASS { color: green; font-weight: bold; }
    .FAIL { color: red; font-weight: bold; }
    .ERROR { color: orange; font-weight: bold; }
    img { width: 100px; transition: width 0.3s; cursor: pointer; border: 1px solid #ccc; }
    img:hover { width: 400px; z-index: 100; position: relative; } 
</style>
</head>
<body>

<h2>Laporan Pengujian Fungsionalitas Website</h2>
<p class="info">Target: indonesiaindicator.com | Tanggal: """ + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + """</p>

<table>
<tr>
    <th>Skenario Pengujian</th>
    <th>Status</th>
    <th>Keterangan Detail</th>
    <th>Bukti Layar</th>
</tr>
"""

# Loop data hasil untuk dimasukkan ke tabel
for item in list_hasil_test:
    # Proses konversi gambar ke Base64 (Embed)
    tag_gambar = "-"
    if item['path_img'] != "" and os.path.exists(item['path_img']):
        try:
            with open(item['path_img'], "rb") as file_img:
                baca_byte = file_img.read()
                # Encode ke base64 agar menjadi string
                string_base64 = base64.b64encode(baca_byte).decode('utf-8')
                tag_gambar = f'<img src="data:image/png;base64,{string_base64}" alt="Bukti">'
        except:
            tag_gambar = "Gagal memuat gambar"

    # Menyusun baris tabel
    baris_baru = f"""
    <tr>
        <td>{item['nama']}</td>
        <td class='{item['status']}'>{item['status']}</td>
        <td>{item['pesan']}</td>
        <td>{tag_gambar}</td>
    </tr>
    """
    konten_html += baris_baru

# Penutup HTML
konten_html += """
</table>
<p style="text-align:center; margin-top:20px; font-size:12px;">Generated by Python Selenium Script</p>
</body>
</html>
"""

# Menyimpan file HTML
nama_file_laporan = f"reports/Laporan_Pengujian_{time.strftime('%Y%m%d_%H%M%S')}.html"
file_handler = open(nama_file_laporan, "w")
file_handler.write(konten_html)
file_handler.close()

print(f"Laporan berhasil dibuat: {nama_file_laporan}")
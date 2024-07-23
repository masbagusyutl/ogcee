import requests
import time
import threading

# Fungsi untuk membaca data dari data.txt
def read_data():
    with open('data.txt', 'r') as file:
        lines = file.readlines()
    accounts = []
    for i in range(0, len(lines), 2):
        captcha = lines[i].strip()
        cookie = lines[i+1].strip()
        accounts.append({
            'captcha': captcha,
            'cookie': cookie
        })
    return accounts

# Fungsi untuk melakukan login harian
def daily_login(account):
    url_init = "https://app.ogcom.xyz/api/daily-reward/init"
    url_reward = "https://app.ogcom.xyz/api/daily-reward"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "0",
        "Cookie": account['cookie'],
        "Origin": "https://app.ogcom.xyz",
        "Pragma": "no-cache",
        "Referer": "https://app.ogcom.xyz/",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
    
    payload = {
        "captcha": account['captcha']
    }
    
    # Permintaan untuk inisiasi login harian
    response_init = requests.post(url_init, headers=headers)
    if response_init.status_code == 200:
        print(f"Login harian berhasil untuk akun: {account['captcha'][:10]}...")  # Menampilkan sebagian captcha untuk identifikasi
    else:
        print(f"Login harian gagal untuk akun: {account['captcha'][:10]}...")
    
    # Permintaan untuk mengambil hadiah
    response_reward = requests.put(url_reward, json=payload, headers=headers)
    if response_reward.status_code == 200:
        print(f"Hadiah berhasil diambil untuk akun: {account['captcha'][:10]}...")
    else:
        print(f"Gagal mengambil hadiah untuk akun: {account['captcha'][:10]}...")

# Fungsi untuk menampilkan hitung mundur
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        hours, mins = divmod(mins, 60)
        timer = f'{hours:02d}:{mins:02d}:{secs:02d}'
        print(f"\rWaktu hingga reset: {timer}", end="")
        time.sleep(1)
        t -= 1
    print("\nWaktu hitung mundur selesai. Memulai ulang proses...")

# Fungsi utama untuk menjalankan proses
def main():
    accounts = read_data()
    total_accounts = len(accounts)
    print(f"Jumlah akun: {total_accounts}")
    
    for i, account in enumerate(accounts):
        print(f"Memproses akun {i+1}/{total_accounts}: {account['captcha'][:10]}...")
        daily_login(account)
        time.sleep(5)  # jeda 5 detik antar akun
    
    # Hitung mundur 17 jam (17 * 3600 detik)
    countdown_thread = threading.Thread(target=countdown, args=(17 * 3600,))
    countdown_thread.start()
    countdown_thread.join()  # tunggu hingga hitung mundur selesai

    # Memulai ulang proses
    main()

if __name__ == "__main__":
    main()

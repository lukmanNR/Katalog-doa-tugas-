import streamlit as st
from database_logic import load_data, save_data
import time
import requests # Tambahan untuk ambil data web
from bs4 import BeautifulSoup # Tambahan untuk bedah HTML

# python -m streamlit run app.py
# Konfigurasi Dasar
st.set_page_config(page_title="Katalog Doaku", layout="centered", page_icon="🌙")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    
    /* Smooth Scroll */
    html { scroll-behavior: smooth; }

    div.stFormSubmitButton > button {
        background-color: #D4AF37 !important;
        color: #121212 !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
        height: 3.5em !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }

    .doa-card {
        background: #1E1E1E; 
        padding: 25px; 
        border-radius: 15px;
        border-left: 5px solid #D4AF37; 
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    .arab-text {
        font-size: 28px; color: #D4AF37; text-align: right;
        direction: rtl; margin: 15px 0; font-family: 'serif';
    }
    
    .latin-text { font-style: italic; color: #9E9E9E; font-size: 14px; margin-bottom: 10px; }
    .arti-text { color: #FFFFFF; font-size: 16px; border-top: 1px solid #333; padding-top: 10px; }

    .source-link {
        display: inline-block;
        padding: 5px 12px;
        background: #252525;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37;
        border-radius: 5px;
        text-decoration: none;
        font-size: 12px;
        margin-top: 15px;
    }

    /* Gaya Navigasi Ikon */
    .nav-button {
        display: flex;
        align-items: center;
        justify-content: center;
        background: #1E1E1E;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        text-decoration: none;
        font-size: 24px;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    .nav-button:hover {
        background: #D4AF37;
        color: #121212 !important;
    }

    .status-msg {
        padding: 15px; border-radius: 10px; text-align: center;
        font-weight: bold; margin-bottom: 15px;
    }
    .msg-save { background: rgba(212, 175, 55, 0.1); color: #D4AF37; border: 1px solid #D4AF37; }
    .msg-del { background: rgba(255, 75, 75, 0.1); color: #FF4B4B; border: 1px solid #FF4B4B; }
    </style>
""", unsafe_allow_html=True)

# --- ANCHOR ATAS ---
st.markdown('<div id="atas"></div>', unsafe_allow_html=True)

st.title("🌙 Katalog Doaku")
data = load_data()

# --- SIDEBAR: NAVIGASI & FORM ---
with st.sidebar:
    st.header("🚀 Navigasi Cepat")
    # Tombol Ikon Menarik
    cols_nav = st.columns(2)
    with cols_nav[0]:
        st.markdown('<a href="#atas" class="nav-button">⬆</a>', unsafe_allow_html=True)
        st.caption("Ke Atas")
    with cols_nav[1]:
        st.markdown('<a href="#bawah" class="nav-button">⬇</a>', unsafe_allow_html=True)
        st.caption("Ke Bawah")
    
    st.divider()

    # ================= FITUR BARU: AUTOMATED SCRAPING =================
    st.header("🤖 Data Ingestion (Otomatis)")
    with st.expander("Klik untuk Scraping Otomatis"):
        target_url = st.text_input("Input Link (URL)", placeholder="https://contoh-situs-doa.com")
        tema_scrap = st.selectbox("Pilih Tema", ["Rezeki", "Safar", "Syukur", "Harian", "Perlindungan"])
        jumlah_minta = st.slider("Jumlah Doa", 1, 25, 5)
        
        btn_scrap = st.button("🚀 Mulai Scraping")
        
        if btn_scrap:
            if target_url:
                with st.spinner("Sedang mengambil data asli..."):
                    try:
                        headers = {'User-Agent': 'Mozilla/5.0'}
                        response = requests.get(target_url, headers=headers, timeout=10)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Inisialisasi variabel agar tidak error 'not defined'
                        count = 0
                        
                        # Mencari semua paragraf untuk mendeteksi teks Arab
                        paragraphs = soup.find_all('p')
                        
                        found_data = []
                        for p in paragraphs:
                            # Cek apakah paragraf mengandung karakter Arab
                            if any("\u0600" <= c <= "\u06FF" for c in p.text):
                                teks_arab = p.text.strip()
                                
                                # Mencari arti (biasanya di paragraf setelah teks Arab)
                                next_p = p.find_next_sibling('p')
                                teks_arti = next_p.text.strip() if next_p else "Arti tidak ditemukan"
                                
                                # Ambil judul dari tag H1 website
                                judul_web = soup.find('h1').text.strip() if soup.find('h1') else f"Doa {tema_scrap}"
                                
                                item_baru = {
                                    "judul": f"{judul_web} ({count + 1})",
                                    "arab": teks_arab,
                                    "latin": "-", 
                                    "arti": teks_arti,
                                    "link": target_url,
                                    "fav": False
                                }
                                found_data.append(item_baru)
                                count += 1
                            
                            # Berhenti jika sudah mencapai jumlah yang diminta slider
                            if count >= jumlah_minta:
                                break

                        if found_data:
                            data.extend(found_data)
                            save_data(data)
                            st.success(f"Alhamdulillah! Berhasil mengambil {count} doa asli.")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.warning("Tidak menemukan teks Arab di link tersebut. Coba link lain.")
                            
                    except Exception as e:
                        st.error(f"Gagal mengambil data: {e}")
            else:
                st.warning("Masukkan URL tujuan terlebih dahulu!")
                
    st.divider()
    # =================================================================

    st.header("✨ Tambah Doa Baru")
    st.markdown('<p style="color: #9E9E9E; font-size: 12px;">Ketik - jika tak ada yang diinput di box(atau akan eror jika ada yang kosong). Abaikan tulisan "Press enter/Ctrl + Enter to submit form" saat mengetik, cukup isi data lalu klik tombol "Tambahkan ke Katalogku" di bawah...</p>', unsafe_allow_html=True)
    
    with st.form("form_doa", clear_on_submit=True):
        in_judul = st.text_input("Judul Doa")
        in_arab = st.text_area("Teks Arab")
        in_latin = st.text_input("Teks Latin (Ketik - jika tak ada)")
        in_arti = st.text_area("Arti/Terjemahan")
        in_link = st.text_input("Link Referensi (Ketik - jika tak ada)")
        
        submit = st.form_submit_button("➕ Tambahkan ke Katalogku")
        
        if submit:
            if in_judul and in_arab and in_arti:
                link_val = in_link.strip()
                if link_val and not link_val.startswith(('http://', 'https://')) and link_val != "-":
                    link_val = "https://" + link_val
                
                new_entry = {
                    "judul": in_judul, 
                    "arab": in_arab, 
                    "latin": in_latin, 
                    "arti": in_arti, 
                    "link": link_val, 
                    "fav": False
                }
                data.append(new_entry)
                save_data(data)
                
                st.balloons()
                msg = st.empty()
                msg.markdown('<div class="status-msg msg-save">✨ ALHAMDULILLAH!<br>Doa Berhasil Disimpan</div>', unsafe_allow_html=True)
                time.sleep(2)
                st.rerun()
            else:
                st.error("Mohon isi Judul, Arab, dan Arti.")

# --- MAIN UI ---
search = st.text_input("🔍 Cari doa...", placeholder="Ketik judul atau arti...").strip().lower()

filtered = [
    d for d in data 
    if search in d.get('judul', '').lower() 
    or search in d.get('arti', '').lower()
    or search in d.get('latin', '').lower()
]

sorted_data = sorted(filtered, key=lambda x: x.get('fav', False), reverse=True)


# --- LOOPING TAMPILAN ---
for index, item in enumerate(sorted_data):
    judul_doa = item.get("judul", "Tanpa Judul")
    teks_arab = item.get("arab", "")
    teks_arti = item.get("arti", "")
    is_fav = item.get("fav", False)

    # Filter Latin
    teks_latin = item.get("latin", "")
    latin_html = f'<div class="latin-text">{teks_latin.strip()}</div>' if teks_latin and teks_latin.strip() != "-" else ""

    # Filter Link
    url_link = item.get("link", "")
    link_html = f'<a href="{url_link.strip()}" target="_blank" class="source-link">🔗 Lihat Sumber</a>' if url_link and url_link.strip() != "-" else ""
    
    st.markdown(f"""
        <div class="doa-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 20px; font-weight: bold; color: #D4AF37;">{judul_doa}</span>
                <div style="display: flex; gap: 10px;">
                    <span style="color: #D4AF37; font-size: 20px;">{'★' if is_fav else ''}</span>
                </div>
            </div>
            <div class="arab-text">{teks_arab}</div>
            {latin_html}
            <div class="arti-text"><b>Artinya:</b> {teks_arti}</div>
            {link_html}
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([4, 1, 1]) # Tambah kolom untuk tombol edit
    with c1:
        txt = "⭐ Hapus dari Favorit" if is_fav else "☆ Tandai Favorit"
        if st.button(txt, key=f"f_{index}"):
            orig_idx = data.index(item)
            data[orig_idx]['fav'] = not data[orig_idx].get('fav', False)
            save_data(data)
            st.rerun()
    with c2:
        # TOMBOL EDIT MANUAL (IKON PENCIL)
        if st.button("📝", key=f"e_{index}", help="Edit Doa Ini"):
            st.info(f"Fitur Edit: Silakan gunakan form 'Tambah Doa' di samping untuk input baru, atau edit langsung di file database_doa.json untuk versi ini.")
    with c3:
        if st.button("🗑️", key=f"d_{index}"):
            st.snow()
            orig_idx = data.index(item)
            data.pop(orig_idx)
            save_data(data)
            msg_del = st.empty()
            msg_del.markdown('<div class="status-msg msg-del">🗑️ Doa Dihapus</div>', unsafe_allow_html=True)
            time.sleep(2.5)
            st.rerun()

# ================= ANALYTICS SEDERHANA =================
st.divider()
st.header("📊 Insight Data")
total_doa = len(data)
st.write("📚 Total jumlah doa:", total_doa)
jumlah_favorit = sum(1 for d in data if d.get('fav'))
st.write("⭐ Jumlah doa favorit:", jumlah_favorit)

# --- ANCHOR BAWAH ---
st.markdown('<div id="bawah"></div>', unsafe_allow_html=True)
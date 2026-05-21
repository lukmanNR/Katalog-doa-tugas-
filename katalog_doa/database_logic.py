import json
import os

DB_FILE = 'database_doa.json'

def load_data():
    if not os.path.exists(DB_FILE):
        # Data awal 5 doa sahih
        initial_data = [
            {"judul": "Doa Sapu Jagat", "arab": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", "latin": "Rabbana atina fiddunya hasanah wa fil akhirati hasanah wa qina 'adzabannar", "arti": "Ya Tuhan kami, berilah kami kebaikan di dunia dan kebaikan di akhirat dan peliharalah kami dari siksa neraka.", "fav": True},
            {"judul": "Doa Keluar Rumah", "arab": "بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ لا حَوْلَ وَلا قُوَّةَ إِلاَّ بِاللَّهِ", "latin": "Bismillahi tawakkaltu 'alallah, laa hawla wa laa quwwata illa billah", "arti": "Dengan nama Allah, aku bertawakal kepada Allah, tiada daya dan upaya kecuali dengan kekuatan Allah.", "fav": False},
            {"judul": "Doa Masuk Masjid", "arab": "اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ", "latin": "Allahummaftahli abwaba rahmatik", "arti": "Ya Allah, bukalah pintu-pintu rahmat-Mu untukku.", "fav": False},
            {"judul": "Doa Memohon Ilmu Bermanfaat", "arab": "اللَّهُمَّ انْفَعْنِي بِمَا عَلَّمْتَنِي وَعَلِّمْنِي مَا يَنْفَعُنِي وَزِدْنِي عِلْمًا", "latin": "Allahummanfa'ni bima 'allamtani wa 'allimni ma yanfa'uni wa zidni 'ilman", "arti": "Ya Allah, berilah manfaat atas apa yang Engkau ajarkan kepadaku, ajarilah aku apa yang bermanfaat bagiku, dan tambahkanlah ilmu kepadaku.", "fav": False},
            {"judul": "Doa Keteguhan Hati", "arab": "يَا مُقَلِّبَ الْقُلُوبِ ثَبِّتْ قَلْبِي عَلَى دِينِكَ", "latin": "Ya Muqallibal qulubi thabbit qalbi 'ala dinika", "arti": "Wahai Dzat yang membolak-balikkan hati, teguhkanlah hatiku di atas agama-Mu.", "fav": True}
        ]
        save_data(initial_data)
        return initial_data
    
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
def get_obesity_info(label_name):
    """
    Returns the mapped category name, reasoning, and suggestion based on the prediction label.
    """
    info = {
        'Insufficient_Weight': {
            'golongan': 'Kekurangan Berat Badan',
            'alasan': 'Indeks Massa Tubuh (IMT) berada di bawah ambang batas fisiologis normal. Kondisi ini umumnya berkorelasi dengan defisit asupan kalori kronis, malabsorpsi nutrisi, atau tingkat laju metabolisme basal (BMR) yang hiperaktif.',
            'saran': 'Direkomendasikan untuk menerapkan program peningkatan asupan (surplus kalori) secara terstruktur. Fokus pada asupan makronutrien padat gizi—termasuk protein tanpa lemak, asam lemak tak jenuh, dan karbohidrat kompleks. Pemantauan klinis oleh ahli gizi (dietitian) sangat dianjurkan guna meminimalisasi risiko defisiensi mikronutrien dan atrofi otot.'
        },
        'Normal_Weight': {
            'golongan': 'Berat Badan Normal',
            'alasan': 'Indeks Massa Tubuh (IMT) menunjukkan proporsi yang optimal terhadap tinggi badan. Profil antropometri ini mengindikasikan keseimbangan termodinamika yang baik antara asupan energi dan aktivitas fisik.',
            'saran': 'Pertahankan homeostasis tubuh melalui pola makan gizi seimbang dan aktivitas fisik aerobik maupun resistensi secara konsisten. Langkah preventif ini esensial untuk menjaga fungsi kardiovaskular dan mitigasi risiko sindrom metabolik di masa mendatang.'
        },
        'Overweight_Level_I': {
            'golongan': 'Kelebihan Berat Badan (Overweight) Tingkat 1',
            'alasan': 'Akumulasi massa adiposa Anda mulai melampaui rasio ideal, menandakan fase pre-obesitas. Patogenesis utamanya kerap diakibatkan oleh surplus kalori berkepanjangan yang disertai gaya hidup sedenter.',
            'saran': 'Disarankan untuk menginisiasi protokol defisit kalori moderat. Restriksi asupan karbohidrat sederhana dan lemak trans harus segera dilakukan. Integrasikan aktivitas kardiovaskular intensitas sedang (LISS) minimal 150 menit per minggu untuk merangsang oksidasi lemak.'
        },
        'Overweight_Level_II': {
            'golongan': 'Kelebihan Berat Badan (Overweight) Tingkat 2',
            'alasan': 'Kelebihan jaringan lemak (adiposa) telah mencapai tahap yang signifikan, menempatkan Anda pada titik klinis kritis sebelum bertransisi menjadi obesitas derajat pertama.',
            'saran': 'Diperlukan intervensi manajemen berat badan yang komprehensif. Implementasikan pola makan tinggi serat dan protein untuk meningkatkan thermic effect of food (TEF), serta pembatasan ketat terhadap makanan berindeks glikemik tinggi. Latihan fisik gabungan mutlak direkomendasikan.'
        },
        'Obesity_Type_I': {
            'golongan': 'Obesitas Tipe I',
            'alasan': 'Status fisik Anda secara klinis diklasifikasikan sebagai obesitas derajat pertama. Terdapat eskalasi risiko yang nyata terhadap patologi komorbid, termasuk resistensi insulin, dislipidemia, dan hipertensi esensial.',
            'saran': 'Modifikasi gaya hidup secara fundamental bersifat preskriptif. Terapkan strategi pengaturan porsi makan (hipokalorik) di bawah pengawasan tenaga profesional, minimalisasi produk ultra-proses, dan mulai terapi aktivitas fisik bertahap. Pemeriksaan laboratorium dasar amat direkomendasikan.'
        },
        'Obesity_Type_II': {
            'golongan': 'Obesitas Tipe II',
            'alasan': 'Profil adipositas Anda telah mencapai level risiko tinggi (obesitas derajat dua). Tingkat akumulasi lemak sistemik ini berkorelasi kuat dengan inflamasi kronis derajat rendah dan gangguan biomekanik pada persendian penyangga tubuh.',
            'saran': 'Dibutuhkan intervensi medis multidisiplin secara segera. Jadwalkan konsultasi dengan ahli endokrinologi atau dokter gizi klinik untuk perancangan pola makan restriktif yang aman, dan terapi fisik low-impact guna meminimalisasi beban osteoartikular.'
        },
        'Obesity_Type_III': {
            'golongan': 'Obesitas Tipe III (Ekstrem)',
            'alasan': 'Klasifikasi ini merepresentasikan obesitas morbid, yang menimbulkan ancaman imanen terhadap fungsi organ vital. Terdapat risiko komplikasi fatal seperti sleep apnea obstruktif, gagal jantung kongestif, dan steatosis hepatik.',
            'saran': 'Intervensi medis tingkat lanjut bersifat darurat (urgen). Evaluasi klinis komprehensif wajib dilakukan di rumah sakit, termasuk pengkajian kriteria kelayakan untuk prosedur bedah bariatrik sebagai opsi manajemen definitif selain terapi nutrisi medis super-ketat.'
        }
    }
    
    # Return default info if label not found
    return info.get(label_name, {
        'golongan': 'Tidak Diketahui',
        'alasan': 'Tidak dapat memproses hasil.',
        'saran': 'Silakan periksa input Anda kembali.'
    })

def generate_recommendation(input_data, financial_risk_label, behavior_segment_label):
    saving_rate = input_data.get("saving_rate", 0)
    expense_trend = input_data.get("expense_trend", 0)
    net_cashflow = input_data.get("net_cashflow", 0)

    if financial_risk_label == "At Risk":
        if net_cashflow < 0:
            return {
                "title": "Cashflow perlu segera diperbaiki",
                "message": "Pengeluaran kamu lebih besar daripada pemasukan. Coba kurangi pengeluaran non-prioritas dan fokus pada kebutuhan utama terlebih dahulu."
            }

        if saving_rate < 0.10:
            return {
                "title": "Tingkat tabungan masih rendah",
                "message": "Saving rate kamu masih rendah. Coba sisihkan sebagian pemasukan di awal bulan sebelum digunakan untuk pengeluaran lain."
            }

        return {
            "title": "Kondisi keuangan perlu perhatian",
            "message": "Beberapa indikator keuangan kamu menunjukkan risiko. Coba evaluasi pengeluaran dan susun ulang anggaran bulanan."
        }

    if behavior_segment_label == "High Food Spender":
        return {
            "title": "Pengeluaran makanan cukup tinggi",
            "message": "Porsi pengeluaran makanan kamu cukup besar. Coba tetapkan batas budget makanan mingguan agar cashflow tetap aman."
        }

    if behavior_segment_label == "Shopping Heavy":
        return {
            "title": "Belanja perlu dikontrol",
            "message": "Porsi pengeluaran belanja kamu cukup tinggi. Coba bedakan kebutuhan dan keinginan sebelum melakukan pembelian."
        }

    if behavior_segment_label == "Entertainment Heavy":
        return {
            "title": "Pengeluaran hiburan cukup besar",
            "message": "Pengeluaran hiburan kamu cukup dominan. Coba buat batas pengeluaran hiburan bulanan agar tidak mengganggu rencana tabungan."
        }

    if behavior_segment_label == "Increasing Spender":
        return {
            "title": "Pengeluaran sedang meningkat",
            "message": "Pengeluaran kamu cenderung meningkat. Coba bandingkan pengeluaran bulan ini dengan bulan sebelumnya dan cari kategori yang paling banyak naik."
        }

    if behavior_segment_label == "Negative Cashflow":
        return {
            "title": "Cashflow negatif",
            "message": "Pengeluaran kamu lebih besar daripada pemasukan. Coba kurangi pengeluaran non-prioritas dan susun ulang anggaran bulanan."
        }

    if behavior_segment_label == "Good Saver":
        return {
            "title": "Kebiasaan menabung sudah baik",
            "message": "Kamu memiliki pola keuangan yang baik. Pertahankan kebiasaan menabung dan pertimbangkan untuk mulai membuat target finansial jangka panjang."
        }

    if financial_risk_label == "Watchlist":
        if expense_trend > 500000:
            return {
                "title": "Pengeluaran mulai meningkat",
                "message": "Pengeluaran kamu menunjukkan kenaikan dibanding periode sebelumnya. Coba evaluasi kategori pengeluaran terbesar agar kondisi keuangan tetap terkendali."
            }

        if saving_rate < 0.20:
            return {
                "title": "Tingkat tabungan perlu ditingkatkan",
                "message": "Kondisi keuangan kamu masih cukup aman, tetapi saving rate masih rendah. Coba sisihkan sebagian pemasukan di awal bulan."
            }

        return {
            "title": "Keuangan perlu dipantau",
            "message": "Kondisi keuangan kamu masih dalam batas aman, tetapi ada beberapa indikator yang perlu diperhatikan agar tidak menjadi risiko di bulan berikutnya."
        }

    return {
        "title": "Keuangan relatif stabil",
        "message": "Kondisi keuangan kamu terlihat cukup stabil. Tetap pantau pengeluaran rutin dan pertahankan kebiasaan mencatat transaksi."
    }
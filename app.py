import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Warung Sejahtera · Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CUSTOM CSS (UI Enhancement + Perbaikan Alignment)
# =============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        border: 1px solid #F0F2F5;
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    div[data-testid="metric-container"] label {
        font-weight: 600 !important;
        color: #6B7280 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #1F2937 !important;
    }
    
    button[kind="primary"] {
        background-color: #3B82F6 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
        border: none !important;
    }
    button[kind="primary"]:hover {
        background-color: #2563EB !important;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E5E7EB;
    }
    
    .streamlit-expanderHeader {
        background-color: #F9FAFB;
        border-radius: 12px;
        font-weight: 600;
    }
    
    hr {
        margin: 2rem 0;
        border: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, #CBD5E1, transparent);
    }
    
    /* Perbaikan Alignment Kolom Dashboard */
    div[data-testid="column"] {
        display: flex;
        flex-direction: column;
    }
    div[data-testid="column"] > div:first-child {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

def load_products():
    file_path = "data/products.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=["id", "name", "buy_price", "sell_price", "stock", "exp_date"])
        df.to_csv(file_path, index=False)
        return df

def save_products(df):
    df.to_csv("data/products.csv", index=False)

def generate_product_id(df):
    if df.empty:
        return "BRG001"
    last_id = df["id"].iloc[-1]
    num = int(last_id[3:]) + 1
    return f"BRG{num:03d}"

def load_transactions():
    file_path = "data/transactions.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    else:
        df = pd.DataFrame(columns=["id", "product_id", "product_name", "qty", "total_price", "profit", "timestamp"])
        df.to_csv(file_path, index=False)
        return df

def save_transaction(product_id, product_name, qty, total_price, profit):
    df = load_transactions()
    
    if df.empty:
        new_id = "TRX001"
    else:
        last_id = df["id"].iloc[-1]
        num = int(last_id[3:]) + 1
        new_id = f"TRX{num:03d}"
    
    new_row = pd.DataFrame([{
        "id": new_id,
        "product_id": product_id,
        "product_name": product_name,
        "qty": qty,
        "total_price": total_price,
        "profit": profit,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("data/transactions.csv", index=False)

# =============================================
# SIDEBAR
# =============================================
st.sidebar.title("Warung Sejahtera v2.2")
st.sidebar.caption("✨ Tema dapat diubah di Settings (⚙️ pojok kanan atas)")
menu = st.sidebar.radio("Menu", ["🏠 Dashboard", "📦 Kelola Barang", "💰 Kasir / Penjualan", "📋 Riwayat Transaksi"])

st.sidebar.markdown("---")
st.sidebar.caption("v2.2 · Dibuat dengan ❤️ untuk belajar SDLC")
st.sidebar.caption("© 2025 Warung Sejahtera")

# =============================================
# DASHBOARD
# =============================================
if menu == "🏠 Dashboard":
    st.title("Dashboard Warung Sejahtera v2.2")
    
    df_products = load_products()
    df_trans = load_transactions()
    
    total_produk = len(df_products)
    total_nilai_stok = 0
    if not df_products.empty:
        total_nilai_stok = (df_products['stock'] * df_products['buy_price']).sum()
    
    today = datetime.now().date()
    laba_hari_ini = 0
    if not df_trans.empty:
        mask_today = df_trans['timestamp'].dt.date == today
        laba_hari_ini = df_trans.loc[mask_today, 'profit'].sum()
    
    with st.container():
        st.markdown("### 📈 Ringkasan Hari Ini")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Jenis Produk", total_produk)
            st.caption("SKU Aktif")
        with col2:
            st.metric("Total Nilai Stok", f"Rp {total_nilai_stok:,.0f}")
            st.caption("Berdasarkan Harga Beli")
        with col3:
            st.metric("Laba Hari Ini", f"Rp {laba_hari_ini:,.0f}")
            st.caption("Keuntungan Kotor")
    
    st.divider()
    
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.subheader("📊 Top 5 Produk Terlaris (Klik Bar untuk Detail)")
        if not df_trans.empty:
            import altair as alt
            top_products = df_trans.groupby('product_name')['qty'].sum().nlargest(5).reset_index()
            
            selection = alt.selection_point(fields=['product_name'])
            chart = alt.Chart(top_products).mark_bar(
                color='#3B82F6',
                cornerRadiusTopLeft=8,
                cornerRadiusTopRight=8,
                size=40
            ).encode(
                x=alt.X('qty:Q', title='Total Terjual', axis=alt.Axis(grid=False)),
                y=alt.Y('product_name:N', sort='-x', title=None, axis=alt.Axis(labelFontSize=13, labelFontWeight='medium')),
                tooltip=['product_name', 'qty'],
                opacity=alt.condition(selection, alt.value(1), alt.value(0.4))
            ).add_params(
                selection
            ).properties(
                height=300
            ).configure_view(
                strokeWidth=0
            ).configure_axis(
                labelColor='#4B5563',
                titleColor='#4B5563'
            )
            
            selected = st.altair_chart(chart, use_container_width=True, on_select="rerun")
            
            if selected and selected.selection and 'product_name' in selected.selection:
                produk_terpilih = selected.selection['product_name'][0]
                st.success(f"📌 Menampilkan transaksi untuk: **{produk_terpilih}**")
                trans_produk = df_trans[df_trans['product_name'] == produk_terpilih]
                if not trans_produk.empty:
                    st.dataframe(
                        trans_produk[['timestamp', 'qty', 'total_price', 'profit']].rename(columns={
                            'timestamp': 'Waktu',
                            'qty': 'Qty',
                            'total_price': 'Total',
                            'profit': 'Laba'
                        }),
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.info("Belum ada transaksi untuk produk ini.")
            else:
                st.info("👆 Klik salah satu bar untuk melihat detail transaksi.")
        else:
            st.info("Belum ada data penjualan.")

    with right_col:
        st.subheader("🚨 Stok Menipis (< 5 pcs)")
        if not df_products.empty:
            stok_tipis = df_products[df_products['stock'] < 5]
            if not stok_tipis.empty:
                st.dataframe(stok_tipis[['name', 'stock']], use_container_width=True, hide_index=True)
            else:
                st.success("Semua stok aman!")
        else:
            st.info("Belum ada data barang.")

# =============================================
# KELOLA BARANG
# =============================================
elif menu == "📦 Kelola Barang":
    st.title("Manajemen Data Barang")
    df = load_products()
    with st.expander("➕ Tambah Barang Baru", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Nama Barang")
            buy_price = st.number_input("Harga Beli (Rp)", min_value=0, step=100)
        with col2:
            sell_price = st.number_input("Harga Jual (Rp)", min_value=0, step=100)
            stock = st.number_input("Stok Awal", min_value=0, step=1)
        with col3:
            exp_date = st.date_input("Tanggal Kadaluarsa")
        if st.button("Simpan Barang"):
            if name and buy_price > 0 and sell_price > 0:
                new_id = generate_product_id(df)
                new_row = pd.DataFrame([{
                    "id": new_id,
                    "name": name,
                    "buy_price": buy_price,
                    "sell_price": sell_price,
                    "stock": stock,
                    "exp_date": exp_date.strftime("%Y-%m-%d")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_products(df)
                st.success(f"Barang {name} berhasil ditambahkan!")
                st.rerun()
            else:
                st.error("Nama dan Harga harus diisi dengan benar!")
    st.subheader("Daftar Barang")
    edited_df = st.data_editor(
        df,
        column_config={
            "id": "ID",
            "name": "Nama Barang",
            "buy_price": st.column_config.NumberColumn("Harga Beli", format="Rp %d"),
            "sell_price": st.column_config.NumberColumn("Harga Jual", format="Rp %d"),
            "stock": st.column_config.NumberColumn("Stok", step=1),
            "exp_date": "Expired"
        },
        hide_index=True,
        num_rows="dynamic",
        disabled=["id"]
    )
    if st.button("💾 Simpan Perubahan Data"):
        save_products(edited_df)
        st.success("Data berhasil diperbarui!")
        st.rerun()

# =============================================
# KASIR / PENJUALAN
# =============================================
elif menu == "💰 Kasir / Penjualan":
    st.title("Kasir Penjualan")
    df_products = load_products()
    if df_products.empty:
        st.warning("Belum ada data barang. Silakan tambah barang dulu di menu Kelola Barang.")
    else:
        list_nama = df_products['name'].tolist()
        selected_item = st.selectbox("Pilih Barang", list_nama)
        selected_product = df_products[df_products['name'] == selected_item].iloc[0]
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Harga Satuan", f"Rp {selected_product['sell_price']:,.0f}")
            st.metric("Stok Tersedia", selected_product['stock'])
        with col2:
            qty = st.number_input("Jumlah Beli", min_value=1, max_value=int(selected_product['stock']), step=1)
            total_harga = qty * selected_product['sell_price']
            st.metric("Total Bayar", f"Rp {total_harga:,.0f}")
        if st.button("🛒 Proses Penjualan", type="primary"):
            if qty > selected_product['stock']:
                st.error("Stok tidak mencukupi!")
            else:
                profit = (selected_product['sell_price'] - selected_product['buy_price']) * qty

                df_products.loc[df_products['name'] == selected_item, 'stock'] -= qty
                save_products(df_products)

                save_transaction(
                    product_id=selected_product['id'],
                    product_name=selected_item,
                    qty=qty,
                    total_price=total_harga,
                    profit=profit
                )

                st.success(f"Penjualan {qty} {selected_item} berhasil! Total: Rp {total_harga:,.0f}")
                st.balloons()
                st.rerun()

# =============================================
# RIWAYAT TRANSAKSI
# =============================================
elif menu == "📋 Riwayat Transaksi":
    st.title("Riwayat Transaksi Penjualan")
    
    df_trans = load_transactions()
    
    if df_trans.empty:
        st.info("Belum ada transaksi yang tercatat.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            filter_date = st.date_input("Pilih Tanggal", value=datetime.now().date())
        with col2:
            st.write("")
            st.write("")
            if st.button("🔄 Tampilkan Semua"):
                filter_date = None
        
        if filter_date:
            mask = df_trans['timestamp'].dt.date == filter_date
            df_filtered = df_trans[mask]
            st.subheader(f"Transaksi Tanggal {filter_date.strftime('%d-%m-%Y')}")
        else:
            df_filtered = df_trans
            st.subheader("Semua Transaksi")
        
        if df_filtered.empty:
            st.warning("Tidak ada transaksi di tanggal ini.")
        else:
            display_df = df_filtered.copy()
            display_df['timestamp'] = display_df['timestamp'].dt.strftime("%H:%M:%S")
            display_df = display_df.rename(columns={
                'id': 'ID Transaksi',
                'product_name': 'Produk',
                'qty': 'Qty',
                'total_price': 'Total (Rp)',
                'profit': 'Laba (Rp)',
                'timestamp': 'Jam'
            })
            
            st.dataframe(
                display_df[['Jam', 'ID Transaksi', 'Produk', 'Qty', 'Total (Rp)', 'Laba (Rp)']],
                use_container_width=True,
                hide_index=True
            )
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_filtered.to_excel(writer, index=False, sheet_name='Riwayat')
            
            st.download_button(
                label="📥 Download Laporan (Excel)",
                data=buffer.getvalue(),
                file_name=f"warung_sejahtera_{filter_date.strftime('%Y%m%d') if filter_date else 'all'}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            total_penjualan = df_filtered['total_price'].sum()
            total_laba = df_filtered['profit'].sum()
            st.metric("Total Penjualan Hari Ini", f"Rp {total_penjualan:,.0f}")
            st.metric("Total Laba Hari Ini", f"Rp {total_laba:,.0f}")

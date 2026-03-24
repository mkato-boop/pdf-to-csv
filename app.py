import streamlit as st
import tabula
import pandas as pd
import tempfile, os

st.set_page_config(page_title="PDF→CSV変換ツール", page_icon="📊")
st.title("📊 PDF → CSV 変換ツール")
st.write("PDFをアップロードするとCSVに変換してダウンロードできます")

uploaded_file = st.file_uploader("PDFを選択してください", type="pdf")

if uploaded_file:
    st.info(f"📄 {uploaded_file.name} を変換中...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        dfs = tabula.read_pdf(tmp_path, pages='all', lattice=True,
                              pandas_options={'header': None})
        if dfs:
            cleaned = []
            for df in dfs:
                df = df.dropna(axis=1, how='all')
                df.columns = range(len(df.columns))
                cleaned.append(df)

            result_df = pd.concat(cleaned, ignore_index=True)

            st.success("✅ 変換完了！")
            st.dataframe(result_df.head(20))

            csv = result_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 CSVをダウンロード",
                data=csv,
                file_name=uploaded_file.name.replace('.pdf', '.csv'),
                mime='text/csv'
            )
        else:
            st.warning("⚠️ 表が見つかりませんでした")

    except Exception as e:
        st.error(f"❌ エラー: {e}")

    finally:
        os.unlink(tmp_path)

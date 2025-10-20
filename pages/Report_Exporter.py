# Export Report File

import streamlit as st
import os
from utils.excel_export import export_to_excel
from utils.pdf_export import export_pdf
from utils.data_loader import load_all_data

def run():
    st.title("📄 Export Reports")

    # Load all data
    try:
        matches, balls, players, teams = load_all_data()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return

    # Ensure reports folder exists
    os.makedirs("reports", exist_ok=True)

    # Export Player Stats to Excel
    if st.button("Export Player Stats to Excel"):
        if players.empty:
            st.warning("No player data available to export.")
        else:
            export_to_excel(players, "reports/player_stats.xlsx")
            st.success("Player stats exported to reports/player_stats.xlsx")

    # Export Team Summary to PDF
    if st.button("Export Team Summary to PDF"):
        if matches.empty:
            st.warning("No match data available to export.")
        else:
            # Prepare content for PDF
            content = "🏆 Team Summary Report\n\n"
            content += matches.head(10).to_string()  # first 10 rows

            # Encode content to avoid latin-1 errors
            content = content.encode("latin-1", errors="replace").decode("latin-1")

            export_pdf("reports/team_summary.pdf", content)
            st.success("Team summary exported to reports/team_summary.pdf")
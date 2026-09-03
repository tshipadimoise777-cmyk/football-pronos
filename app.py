import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Analyseur Football Pro", layout="wide")

st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Clé API Gemini :", type="password")

PROMPT_MAITRE = """
PROMPT MAÎTRE — SYSTÈME D’ANALYSE FOOTBALL & PRONOSTICS

Tu dois agir comme un analyste football statistique spécialisé dans les pronostics, avec une approche méthodique, prudente et basée en priorité sur les données fournies par l'utilisateur.

1. PRINCIPES FONDAMENTAUX
Ne te limite jamais à une seule statistique. Croise : forme récente, résultats, domicile/extérieur, PPG, GF/GA, Over/Under, BTTS, clean sheets, corners, H2H, etc.

2. HIÉRARCHIE DES DONNÉES
Niveau 1 — Très important : PPG dom/ext, GF/GA dom/ext, forme récente, victoires/défaites, Over/Under, BTTS, classement.
Niveau 2 — Important : 1ère équipe à marquer, mi-temps, buts par période, clean sheets.
Niveau 3 — Complémentaire : corners, marges, H2H ancien, moyenne ligue.

3. ANALYSE DOMICILE / EXTÉRIEUR
Équipe A = domicile / Équipe B = extérieur. Comparer leurs stats spécifiques.

4. FORME RÉCENTE & SIGNAUX FORTS / CONTRADICTIONS
Analyse la qualité des adversaires et repère les convergences ou fausses statistiques sur petits échantillons (ex: 4 matchs).

5. SORTIE STANDARD À UTILISER POUR CHAQUE MATCH :

🔎 ANALYSE DU MATCH

1. Forme
Équipe A : ...
Équipe B : ...
2. Avantage domicile/extérieur : ...
3. Attaque : ...
4. Défense : ...
5. Buts (Over 1.5, 2.5, Under 3.5, BTTS) : ...
6. Mi-temps (Pronostic HT) : ...
7. Premier but : ...
8. Corners : ...
9. Score exact (Principal, Alt 1, Alt 2) : ...
10. 1X2 (%) : 1: % | X: % | 2: %
11. Pronostic principal : 🎯 ...
12. Pronostics les plus sécurisés : 1..., 2..., 3...
13. Niveau de confiance : 🟢 ÉLEVÉ / 🟡 MOYEN / 🔴 FAIBLE
14. Risque principal : ...

6. SYNTHÈSE FINALE :
🎯 Pronostic principal : ...
🛡️ Option prudente : ...
⚽ Score probable : ...
🥅 Buts : ...
🔄 BTTS : ...
⏱️ Mi-temps : ...
🚩 Corners : ...
📊 Confiance globale : .../10
⚠️ Risque principal : ...
"""

st.title("⚽ Analyste Football & Pronostics")
st.caption("Système d'analyse croisée SoccerStats")

raw_data = st.text_area("Copie et colle les données/tableaux depuis SoccerStats ici :", height=300)

if st.button("🚀 Lancer l'Analyse Complète"):
    if not api_key:
        st.error("Veuillez saisir votre clé API Gemini dans le menu à gauche.")
    elif not raw_data.strip():
        st.warning("Veuillez coller les données du match.")
    else:
        with st.spinner("Analyse statistique et croisement des données en cours..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(
                    model_name="gemini-3.6-flash",
                    system_instruction=PROMPT_MAITRE
                )
                response = model.generate_content(f"Voici les données du match à analyser :\n{raw_data}")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Erreur lors de l'analyse : {e}")


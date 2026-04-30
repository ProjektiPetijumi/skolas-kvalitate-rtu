"""
Vispārējās vidējās izglītības iestāžu kvalitātes sistēmas
PAŠNOVĒRTĒŠANAS FORMA

Online rīks, kas ļauj citām Latvijas izglītības iestādēm aizpildīt
anketu un saņemt individualizētu atskaiti par kvalitātes sistēmas
stāvokli, balstoties uz maģistra darbā izstrādāto modeli.

Izstrādāts maģistra darba ietvaros:
Geide I. (2026). Kvalitātes novērtējums un starpdisciplinaritāte
vispārējās vidējās izglītības iestādēs. RTU IEVF.

Palaišana lokāli:
    pip install streamlit plotly pandas
    python -m streamlit run skolas_pasnovertesanas_forma.py

Publicēšana online (bezmaksas):
    1. GitHub repozitorijā ielādē šo failu un requirements.txt
    2. streamlit.io/cloud → Connect repository → Deploy
    3. Saņem publisku linku formā: https://[nosaukums].streamlit.app
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ─── KONFIGURĀCIJA ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Skolas kvalitātes sistēmas pašnovērtēšana",
    layout="wide"
)

# ─── AKADĒMISKĀ STILA CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
    html, body, [class*="css"], .stMarkdown, .stText,
    .stTabs, .stButton, .stSlider, .stMetric, .stRadio,
    .stSelectbox, .stNumberInput, .stTextInput, .stTextArea,
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        font-family: "Times New Roman", Times, serif !important;
    }
    h1 {
        font-size: 22pt !important;
        font-weight: bold !important;
        color: #1a1a1a !important;
        border-bottom: 1px solid #888 !important;
        padding-bottom: 8px !important;
    }
    h2, h3 { color: #2a2a2a !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] {
        font-family: "Times New Roman", Times, serif !important;
        font-size: 18pt !important;
        color: #1a1a1a !important;
    }
    .stAlert {
        background-color: #f5f5f5 !important;
        border-left: 3px solid #888 !important;
        border-radius: 0 !important;
    }
    [data-testid="stCaptionContainer"] {
        font-style: italic !important;
        color: #555 !important;
    }
    .stButton button {
        background-color: #2a2a2a !important;
        color: white !important;
        border-radius: 0 !important;
        font-family: "Times New Roman", Times, serif !important;
        font-size: 12pt !important;
    }
</style>
""", unsafe_allow_html=True)

# Krāsu palete
PELE_TUMSI = "#2a2a2a"
PELE_VIDEJI = "#5a5a5a"
PELE_GAISI = "#8a8a8a"
PELE_LOTI_GAISI = "#bababa"
AKCENTS = "#1a1a1a"

PLOTLY_LAYOUT = dict(
    font=dict(family="Times New Roman, Times, serif", size=12, color="#1a1a1a"),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE — DATU SAGLABĀŠANA STARP SOĻIEM
# ═══════════════════════════════════════════════════════════════════════════════
if "step" not in st.session_state:
    st.session_state.step = 0
if "data" not in st.session_state:
    st.session_state.data = {}

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def restart():
    st.session_state.step = 0
    st.session_state.data = {}

# ═══════════════════════════════════════════════════════════════════════════════
# VIRSRAKSTS UN APRAKSTS
# ═══════════════════════════════════════════════════════════════════════════════
st.title("Skolas kvalitātes sistēmas pašnovērtēšana")
st.markdown(
    "*Pašnovērtēšanas rīks vispārējās vidējās izglītības iestādēm — "
    "balstīts uz ISO 21001:2025 standartu un RTU IEVF maģistra darbā "
    "izstrādāto starpdisciplinaritātes integrācijas kvalitātes "
    "novērtēšanas modeli*"
)

# Progresa josla
total_steps = 5
progress = min(st.session_state.step / total_steps, 1.0)
st.progress(progress)
st.caption(f"Solis {st.session_state.step + 1} no {total_steps + 1}")
st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# 0. SOLIS — IEVADS UN INSTRUKCIJAS
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 0:
    st.subheader("Par šo pašnovērtēšanas rīku")

    st.markdown("""
    Šis rīks ļauj jūsu izglītības iestādei **patstāvīgi novērtēt** savas
    kvalitātes sistēmas stāvokli un saņemt individualizētu atskaiti ar
    konkrētiem uzlabojumu priekšlikumiem.

    **Aizpildīšana aizņem aptuveni 15–20 minūtes.**

    Pašnovērtēšana ietver piecas sadaļas:
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **1. Iestādes raksturojums**
        Pamata informācija par izglītības iestādi.

        **2. ISO 21001:2025 atbilstība**
        Pašnovērtējums septiņās standarta sadaļās.

        **3. Starpdisciplinaritātes integrācija**
        K1–K5 kritēriju pašvērtējums.
        """)
    with col2:
        st.markdown("""
        **4. Procesu un risku novērtējums**
        Galveno risku identificēšana.

        **5. Kvalitātes izmaksu pašvērtējums**
        F. Krosbija modeļa pielietojums.

        **6. Atskaite**
        Individualizēti rezultāti un priekšlikumi.
        """)

    st.markdown("---")
    st.markdown("##### Pirms sākat")
    st.info(
        "Pašnovērtēšana ir anonīma. Ievadītie dati netiek saglabāti "
        "ārpus jūsu sesijas — pēc atskaites saņemšanas un pārlūka "
        "aizvēršanas tie tiek dzēsti. Atskaiti var saglabāt PDF formātā."
    )

    st.markdown("##### Ieteicams sagatavot")
    st.markdown("""
    - Iestādes pašvērtējuma ziņojumu (pēdējais)
    - Attīstības plānu
    - Aptuvenu informāciju par gada budžetu
    - Datus par izglītojamo skaitu un personālu
    """)

    if st.button("Sākt pašnovērtēšanu →", type="primary"):
        next_step()
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 1. SOLIS — IESTĀDES RAKSTUROJUMS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    st.subheader("1. Iestādes raksturojums")
    st.markdown(
        "Pamata informācija nepieciešama atskaites kontekstualizēšanai. "
        "Iestādes nosaukums atskaitē tiks parādīts, bet dati netiks "
        "saglabāti ārējās datubāzēs."
    )

    col1, col2 = st.columns(2)
    with col1:
        nosaukums = st.text_input(
            "Iestādes nosaukums",
            value=st.session_state.data.get("nosaukums", "")
        )
        novads = st.text_input(
            "Novads / pilsēta",
            value=st.session_state.data.get("novads", "")
        )
        izglitojamo_skaits = st.number_input(
            "Izglītojamo kopējais skaits",
            min_value=1, max_value=5000,
            value=st.session_state.data.get("izglitojamo_skaits", 500)
        )
        videjas_klases = st.number_input(
            "Vidusskolas posma izglītojamo skaits (10.–12. klase)",
            min_value=0, max_value=2000,
            value=st.session_state.data.get("videjas_klases", 100)
        )

    with col2:
        personala_skaits = st.number_input(
            "Personāla skaits (pedagogi, atbalsta, administratīvais)",
            min_value=1, max_value=500,
            value=st.session_state.data.get("personala_skaits", 50)
        )
        gada_budzets = st.number_input(
            "Iestādes gada budžets (EUR, aptuveni)",
            min_value=10_000, max_value=20_000_000,
            value=st.session_state.data.get("gada_budzets", 1_500_000),
            step=10_000
        )
        ikvd_vertejums = st.selectbox(
            "Pēdējais IKVD akreditācijas vērtējums",
            ["Nav veikts", "1 (nepietiekams)", "2 (attīstības stadijā)",
             "3 (labs)", "4 (izcils)"],
            index=["Nav veikts", "1 (nepietiekams)",
                   "2 (attīstības stadijā)", "3 (labs)",
                   "4 (izcils)"].index(
                st.session_state.data.get("ikvd_vertejums", "Nav veikts"))
        )
        iso_status = st.radio(
            "ISO 21001:2025 sertifikācijas statuss",
            ["Nav un nav plānots", "Plānots tuvākajos 3 gados",
             "Sertifikācijas process notiek", "Sertificēts"],
            index=["Nav un nav plānots", "Plānots tuvākajos 3 gados",
                   "Sertifikācijas process notiek",
                   "Sertificēts"].index(
                st.session_state.data.get("iso_status",
                                          "Nav un nav plānots"))
        )

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Atpakaļ"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Tālāk →", type="primary"):
            if not nosaukums:
                st.warning("Lūdzu, ievadiet iestādes nosaukumu")
            else:
                st.session_state.data.update({
                    "nosaukums": nosaukums,
                    "novads": novads,
                    "izglitojamo_skaits": izglitojamo_skaits,
                    "videjas_klases": videjas_klases,
                    "personala_skaits": personala_skaits,
                    "gada_budzets": gada_budzets,
                    "ikvd_vertejums": ikvd_vertejums,
                    "iso_status": iso_status,
                })
                next_step()
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 2. SOLIS — ISO 21001:2025 ATBILSTĪBA
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.subheader("2. ISO 21001:2025 atbilstības pašvērtējums")
    st.markdown(
        "Novērtējiet, cik lielā mērā jūsu iestāde atbilst ISO 21001:2025 "
        "standarta prasībām katrā sadaļā. Skala: 0% (nav ieviests) līdz "
        "100% (pilnībā ieviests un dokumentēts)."
    )

    aprakstosanas = {
        "k4": ("4. Konteksts",
               "Iesaistīto pušu identificēšana, iekšējās un ārējās vides "
               "analīze, iestādes mērķu sasaiste ar kontekstu"),
        "k5": ("5. Līderība",
               "Vadības apņemšanās, kvalitātes politika, lomu un "
               "atbildību definēšana"),
        "k6": ("6. Plānošana",
               "Risku un iespēju vadība, SMART kvalitātes mērķi, "
               "izmaiņu plānošana"),
        "k7": ("7. Atbalsts",
               "Resursi, kompetence, informētība, komunikācija, "
               "dokumentētā informācija"),
        "k8": ("8. Operācijas",
               "Procesu plānošana un kontrole, izglītības pakalpojumu "
               "sniegšana"),
        "k9": ("9. Veiktspējas novērtēšana",
               "Monitorings, iekšējais audits, vadības pārskats"),
        "k10": ("10. Uzlabošana",
                "Neatbilstības, korektīvās darbības, nepārtraukta "
                "uzlabošana"),
    }

    iso_dati = {}
    for kods, (nosaukums, apraksts) in aprakstosanas.items():
        st.markdown(f"**{nosaukums}**")
        st.caption(apraksts)
        iso_dati[kods] = st.slider(
            f"Atbilstības līmenis ({nosaukums})",
            0, 100,
            st.session_state.data.get(kods, 50),
            5, format="%d%%",
            key=f"iso_{kods}",
            label_visibility="collapsed"
        )
        st.markdown("")

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Atpakaļ"):
            st.session_state.data.update(iso_dati)
            prev_step()
            st.rerun()
    with col2:
        if st.button("Tālāk →", type="primary"):
            st.session_state.data.update(iso_dati)
            next_step()
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 3. SOLIS — STARPDISCIPLINARITĀTES INTEGRĀCIJA (K1–K5)
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    st.subheader("3. Starpdisciplinaritātes integrācijas pašvērtējums")
    st.markdown(
        "Novērtējiet, cik sistemātiski iestādē tiek integrēta "
        "starpdisciplinaritāte piecos kvalitātes kritērijos (K1–K5)."
    )

    kriteriji = {
        "k1_rezultati": (
            "K1. Izglītojamo rezultāti un kompetences",
            "Vai izglītojamo sasniegumos tiek mērītas ne tikai disciplinārās, "
            "bet arī starpdisciplinārās kompetences (spēja integrēt zināšanas "
            "no vairākām jomām)?"
        ),
        "k2_process": (
            "K2. Mācību procesa kvalitāte",
            "Vai notiek regulāra starpdisciplināra mācīšana (team teaching, "
            "integrētas tēmas, kopīgi projekti)?"
        ),
        "k3_saturs": (
            "K3. Mācību satura kvalitāte",
            "Cik liels procents mācību laika tiek veltīts starpdisciplināriem "
            "projektiem (mērķis: vismaz 15%)?"
        ),
        "k4_vide": (
            "K4. Vide un resursi",
            "Vai pastāv personāla sadarbības kultūra un nepieciešamie resursi "
            "(laiks, materiāli, IT) starpdisciplinārai darbībai?"
        ),
        "k5_vadiba": (
            "K5. Vadība un kvalitātes vadības sistēma",
            "Vai starpdisciplinaritātes aktivitātes tiek sistēmiski plānotas, "
            "monitorētas un novērtētas vadības līmenī?"
        ),
    }

    sd_dati = {}
    for kods, (nosaukums, apraksts) in kriteriji.items():
        st.markdown(f"**{nosaukums}**")
        st.caption(apraksts)
        sd_dati[kods] = st.slider(
            nosaukums,
            0, 100,
            st.session_state.data.get(kods, 50),
            5, format="%d%%",
            key=f"sd_{kods}",
            label_visibility="collapsed"
        )
        st.markdown("")

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Atpakaļ"):
            st.session_state.data.update(sd_dati)
            prev_step()
            st.rerun()
    with col2:
        if st.button("Tālāk →", type="primary"):
            st.session_state.data.update(sd_dati)
            next_step()
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 4. SOLIS — RISKU UN PROCESU NOVĒRTĒJUMS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    st.subheader("4. Risku un procesu novērtējums")
    st.markdown(
        "Novērtējiet, cik lielā mērā jūsu iestādei aktuāli ir šie riski. "
        "Skala: 1 (nav aktuāls) līdz 5 (ļoti aktuāls)."
    )

    riski_saraksts = {
        "r1": "Vadības atbalsts starpdisciplinaritātei nav stratēģiskā prioritāte",
        "r2": "Personālam trūkst kompetences procesu saskaņošanā",
        "r3": "Metodiskās komisijas strādā izolēti, bez starpfunkcionālas sadarbības",
        "r4": "Personālam trūkst zināšanu par citu mācību priekšmetu saturu",
        "r5": "Pastāv risks veidot mākslīgas (ne jēgpilnas) starppriekšmetu saiknes",
        "r6": "Vērtēšanas sistēma nav adaptēta starpdisciplinaritātes mērīšanai",
        "r7": "Skola2030 satura ieviešana iestādē ir fragmentāra",
        "r8": "Trūkst kopīga plānošanas laika personālam",
        "r9": "Mācību satura pārslogotība neļauj veikt dziļu integrāciju",
        "r10": "Personālam trūkst laika starpdisciplinārai darbībai",
    }

    risku_dati = {}
    for kods, apraksts in riski_saraksts.items():
        risku_dati[kods] = st.select_slider(
            apraksts,
            options=[1, 2, 3, 4, 5],
            value=st.session_state.data.get(kods, 3),
            key=f"r_{kods}"
        )

    # Procesu integrācijas pašvērtējums
    st.markdown("##### Procesu integrācijas pašvērtējums")
    procesu_integracija = st.slider(
        "Cik labi savstarpēji integrēti ir iestādes galvenie procesi "
        "(personāla vadība, kvalitātes sistēma, mācību process, "
        "resursu pārvaldība)?",
        0, 100,
        st.session_state.data.get("procesu_integracija", 50),
        5, format="%d%%"
    )

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Atpakaļ"):
            st.session_state.data.update(risku_dati)
            st.session_state.data["procesu_integracija"] = procesu_integracija
            prev_step()
            st.rerun()
    with col2:
        if st.button("Tālāk →", type="primary"):
            st.session_state.data.update(risku_dati)
            st.session_state.data["procesu_integracija"] = procesu_integracija
            next_step()
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 5. SOLIS — KVALITĀTES IZMAKSU PAŠVĒRTĒJUMS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 5:
    st.subheader("5. Kvalitātes izmaksu pašvērtējums")
    st.markdown(
        "F. Krosbija modelis iedala kvalitātes izmaksas atbilstības "
        "(prevencija + novērtēšana) un neatbilstības (iekšējās un ārējās "
        "kļūmes) izmaksās. Norādiet aptuveno % no gada budžeta."
    )

    st.markdown("##### Atbilstības izmaksas (PoC)")
    col1, col2 = st.columns(2)
    with col1:
        poc_prev = st.slider(
            "Novēršanas izmaksas (apmācības, plānošana, kvalitātes "
            "sistēmas uzturēšana)",
            0.0, 20.0,
            st.session_state.data.get("poc_prev", 5.0),
            0.5, format="%.1f%%"
        )
    with col2:
        poc_nov = st.slider(
            "Novērtēšanas izmaksas (auditi, pašnovērtējums, mācību "
            "procesa novērošana)",
            0.0, 15.0,
            st.session_state.data.get("poc_nov", 2.5),
            0.5, format="%.1f%%"
        )

    st.markdown("##### Neatbilstības izmaksas (PoNC)")
    col1, col2 = st.columns(2)
    with col1:
        ponc_iek = st.slider(
            "Iekšējās kļūmes (vakances, stundu pārplānošana, atkārtotas "
            "konsultācijas)",
            0.0, 30.0,
            st.session_state.data.get("ponc_iek", 12.0),
            0.5, format="%.1f%%"
        )
    with col2:
        ponc_ar = st.slider(
            "Ārējās kļūmes (izglītojamo aiziešana, sūdzības, reputācijas "
            "zaudējumi)",
            0.0, 20.0,
            st.session_state.data.get("ponc_ar", 7.5),
            0.5, format="%.1f%%"
        )

    kopa = poc_prev + poc_nov + ponc_iek + ponc_ar
    poc_kopa = poc_prev + poc_nov
    ponc_kopa = ponc_iek + ponc_ar

    col1, col2, col3 = st.columns(3)
    col1.metric("Kopā PoC", f"{poc_kopa:.1f}%")
    col2.metric("Kopā PoNC", f"{ponc_kopa:.1f}%")
    col3.metric("Kopējās izmaksas", f"{kopa:.1f}%")

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Atpakaļ"):
            st.session_state.data.update({
                "poc_prev": poc_prev, "poc_nov": poc_nov,
                "ponc_iek": ponc_iek, "ponc_ar": ponc_ar
            })
            prev_step()
            st.rerun()
    with col2:
        if st.button("Ģenerēt atskaiti →", type="primary"):
            st.session_state.data.update({
                "poc_prev": poc_prev, "poc_nov": poc_nov,
                "ponc_iek": ponc_iek, "ponc_ar": ponc_ar
            })
            next_step()
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 6. SOLIS — INDIVIDUALIZĒTĀ ATSKAITE
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 6:
    d = st.session_state.data

    st.subheader(f"Pašnovērtēšanas atskaite: {d['nosaukums']}")
    st.caption(f"Atskaite ģenerēta: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

    # ── KOPĒJIE RĀDĪTĀJI ──
    st.markdown("### Kopējie rādītāji")

    iso_videja = sum([d['k4'], d['k5'], d['k6'], d['k7'], d['k8'],
                       d['k9'], d['k10']]) / 7
    sd_videja = sum([d['k1_rezultati'], d['k2_process'], d['k3_saturs'],
                      d['k4_vide'], d['k5_vadiba']]) / 5
    poc_kopa = d['poc_prev'] + d['poc_nov']
    ponc_kopa = d['ponc_iek'] + d['ponc_ar']
    kvalitates_izmaksas = poc_kopa + ponc_kopa

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("ISO 21001:2025 atbilstība", f"{iso_videja:.1f}%")
    col2.metric("Starpdisciplinaritāte", f"{sd_videja:.1f}%")
    col3.metric("Procesu integrācija", f"{d['procesu_integracija']}%")
    col4.metric("Kvalitātes izmaksas", f"{kvalitates_izmaksas:.1f}%")

    # ── ISO RADARA DIAGRAMMA ──
    st.markdown("### ISO 21001:2025 atbilstības profils")

    iso_kategorijas = ["4. Konteksts", "5. Līderība", "6. Plānošana",
                        "7. Atbalsts", "8. Operācijas",
                        "9. Veiktspēja", "10. Uzlabošana"]
    iso_vertibas = [d['k4'], d['k5'], d['k6'], d['k7'],
                     d['k8'], d['k9'], d['k10']]

    fig1 = go.Figure()
    fig1.add_trace(go.Scatterpolar(
        r=iso_vertibas + [iso_vertibas[0]],
        theta=iso_kategorijas + [iso_kategorijas[0]],
        fill='toself',
        name=d['nosaukums'],
        line=dict(color=AKCENTS, width=2),
        fillcolor='rgba(42, 42, 42, 0.15)'
    ))
    fig1.add_trace(go.Scatterpolar(
        r=[75]*8,
        theta=iso_kategorijas + [iso_kategorijas[0]],
        name='Mērķis (75%)',
        line=dict(color=PELE_GAISI, width=1, dash='dot')
    ))
    fig1.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100],
                                    gridcolor=PELE_LOTI_GAISI)),
        height=400, margin=dict(t=20, b=20),
        **PLOTLY_LAYOUT
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ── STIPRĀS UN VĀJĀS PUSES ──
    st.markdown("### Stiprās un vājās puses")
    iso_dict = dict(zip(iso_kategorijas, iso_vertibas))
    sortēts = sorted(iso_dict.items(), key=lambda x: x[1], reverse=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Trīs stiprākās jomas**")
        for nosaukums, vertiba in sortēts[:3]:
            st.markdown(f"- {nosaukums}: **{vertiba}%**")
    with col2:
        st.markdown("**Trīs prioritārās uzlabojumu jomas**")
        for nosaukums, vertiba in sortēts[-3:]:
            st.markdown(f"- {nosaukums}: **{vertiba}%**")

    # ── KVALITĀTES IZMAKSU ANALĪZE ──
    st.markdown("### Kvalitātes izmaksu struktūra (Krosbija modelis)")

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=["Atbilstības (PoC)", "Neatbilstības (PoNC)"],
        y=[poc_kopa, ponc_kopa],
        marker_color=[PELE_TUMSI, PELE_GAISI],
        text=[f"{poc_kopa:.1f}%", f"{ponc_kopa:.1f}%"],
        textposition='outside',
        textfont=dict(family="Times New Roman", size=14)
    ))
    fig2.update_layout(
        height=300, margin=dict(t=40, b=40),
        yaxis=dict(title='% no budžeta', range=[0, max(poc_kopa, ponc_kopa) * 1.3],
                   gridcolor=PELE_LOTI_GAISI),
        **PLOTLY_LAYOUT
    )
    st.plotly_chart(fig2, use_container_width=True)

    if ponc_kopa > poc_kopa:
        st.warning(
            f"**Diagnoze:** Iestādes neatbilstības izmaksas "
            f"({ponc_kopa:.1f}%) pārsniedz atbilstības izmaksas "
            f"({poc_kopa:.1f}%). Saskaņā ar F. Krosbija tēzi *Quality is "
            f"Free*, ieguldījumi prevencijā atmaksājas caur defektu "
            f"samazināšanos. Ieteicams palielināt PoC daļu par 2–4 "
            f"procentpunktiem."
        )
    else:
        st.success(
            f"**Diagnoze:** Iestādes atbilstības izmaksas ({poc_kopa:.1f}%) "
            f"pārsniedz neatbilstības izmaksas ({ponc_kopa:.1f}%), kas "
            f"liecina par labi strukturētu prevencijas pieeju."
        )

    # ── PRIORITĀRO RISKU SARAKSTS ──
    st.markdown("### Prioritārie riski")
    risku_apraksti = {
        "r1": "Vadības atbalsts nav stratēģiskā prioritāte",
        "r2": "Procesu saskaņošanas kompetences trūkums",
        "r3": "Starpfunkcionālo grupu izolētība",
        "r4": "Personāla zināšanas par citu priekšmetu",
        "r5": "Mākslīgas saiknes risks",
        "r6": "Vērtēšanas sistēma nav adaptēta",
        "r7": "Skola2030 fragmentārums",
        "r8": "Kopīga plānošanas laika trūkums",
        "r9": "Satura pārslogotība",
        "r10": "Laika resursu trūkums",
    }
    aktuali_riski = [(risku_apraksti[k], d[k]) for k in risku_apraksti
                      if d[k] >= 4]
    aktuali_riski.sort(key=lambda x: x[1], reverse=True)

    if aktuali_riski:
        for risks, vertejums in aktuali_riski[:5]:
            st.markdown(f"- **{risks}** (aktualitāte: {vertejums}/5)")
    else:
        st.markdown("*Iestādei nav konstatēti augsta līmeņa riski "
                    "(visi riski zem 4/5 līmeņa).*")

    # ── PRIORITĀRIE PRIEKŠLIKUMI ──
    st.markdown("### Prioritārie priekšlikumi")
    priekslikumi = []

    # Loģika priekšlikumu ģenerēšanai pēc datiem
    if iso_videja < 60:
        priekslikumi.append((
            "Kvalitātes rokasgrāmatas izstrāde",
            "ISO 21001:2025 atbilstības celšana sākas ar formalizētu "
            "dokumentāciju. Plānotais ieguldījums: ~2 500 EUR, termiņš: "
            "3 mēneši, atmaksāšanās: 6 mēneši."
        ))

    if sd_videja < 60:
        priekslikumi.append((
            "Starpdisciplinaritātes koordinatoru iecelšana",
            "Katrā metodiskajā komisijā nepieciešams formalizēts "
            "koordinators ar stundu slodzi. Termiņš: 1 mēnesis, "
            "izmaksas: ~5 000 EUR/gadā."
        ))

    if d['procesu_integracija'] < 65:
        priekslikumi.append((
            "Digitālā dokumentācijas platforma",
            "Vienota platforma starpstruktūru komunikācijai "
            "(MS Teams/SharePoint). Izmaksas: ~3 000 EUR, termiņš: "
            "4–6 mēneši, atmaksāšanās: 8–10 mēneši."
        ))

    if ponc_kopa > poc_kopa:
        priekslikumi.append((
            "Preventīvās kvalitātes budžeta sadaļa",
            "Atsevišķa budžeta pozīcija preventīvai kvalitātei "
            "(3% no kopējā budžeta). Sagaidāmais PoNC samazinājums: "
            "līdz ~50 000 EUR/gadā."
        ))

    if d['k3_saturs'] < 50:
        priekslikumi.append((
            "Starpdisciplinaritātes projektu reģistrs",
            "Strukturēts reģistrs ar mērķi sasniegt vismaz 15% mācību "
            "laika starpdisciplināriem projektiem. Termiņš: 2 mēneši."
        ))

    if d['poc_prev'] < 5:
        priekslikumi.append((
            "Personāla profesionālā pilnveide",
            "Sistemātiskas apmācības procesu vadībā un "
            "starpdisciplinaritātes koordinācijā. ROI ~7.2:1."
        ))

    if not priekslikumi:
        st.success(
            "Pamatojoties uz pašnovērtējumu, iestādei nav konstatētas "
            "kritiskas jomas, kas prasītu prioritārus uzlabojumus. "
            "Ieteicams uzturēt esošo praksi un veikt regulāru "
            "pašnovērtēšanu reizi gadā."
        )
    else:
        for i, (nosaukums, apraksts) in enumerate(priekslikumi, 1):
            st.markdown(f"**{i}. {nosaukums}**")
            st.markdown(apraksts)
            st.markdown("")

    # ── ATSKAITES LEJUPIELĀDE ──
    st.markdown("---")
    st.markdown("### Atskaites saglabāšana")

    # Tekstuālā atskaite
    atskaite_teksts = f"""
PAŠNOVĒRTĒŠANAS ATSKAITE

Iestāde: {d['nosaukums']}
Novads: {d['novads']}
Atskaite ģenerēta: {datetime.now().strftime('%d.%m.%Y %H:%M')}

────────────────────────────────────────────────────────
KOPĒJIE RĀDĪTĀJI
────────────────────────────────────────────────────────
ISO 21001:2025 atbilstība:        {iso_videja:.1f}%
Starpdisciplinaritātes integrācija: {sd_videja:.1f}%
Procesu integrācija:               {d['procesu_integracija']}%
Kvalitātes izmaksas (% budžeta):   {kvalitates_izmaksas:.1f}%
  - Atbilstības (PoC):             {poc_kopa:.1f}%
  - Neatbilstības (PoNC):          {ponc_kopa:.1f}%

────────────────────────────────────────────────────────
ISO 21001:2025 SADAĻAS
────────────────────────────────────────────────────────
4. Konteksts:                     {d['k4']}%
5. Līderība:                      {d['k5']}%
6. Plānošana:                     {d['k6']}%
7. Atbalsts:                      {d['k7']}%
8. Operācijas:                    {d['k8']}%
9. Veiktspējas novērtēšana:       {d['k9']}%
10. Uzlabošana:                   {d['k10']}%

────────────────────────────────────────────────────────
STARPDISCIPLINARITĀTES KRITĒRIJI
────────────────────────────────────────────────────────
K1. Izglītojamo rezultāti:        {d['k1_rezultati']}%
K2. Mācību procesa kvalitāte:     {d['k2_process']}%
K3. Mācību satura kvalitāte:      {d['k3_saturs']}%
K4. Vide un resursi:              {d['k4_vide']}%
K5. Vadība:                       {d['k5_vadiba']}%

────────────────────────────────────────────────────────
PRIORITĀRIE PRIEKŠLIKUMI
────────────────────────────────────────────────────────
"""
    for i, (nosaukums, apraksts) in enumerate(priekslikumi, 1):
        atskaite_teksts += f"\n{i}. {nosaukums}\n   {apraksts}\n"

    atskaite_teksts += f"""

────────────────────────────────────────────────────────
PAR RĪKU
────────────────────────────────────────────────────────
Pašnovērtēšana balstīta uz maģistra darba ietvaros izstrādāto
modeli: Geide I. (2026). Kvalitātes novērtējums un
starpdisciplinaritāte vispārējās vidējās izglītības
iestādēs. RTU IEVF.
"""

    st.download_button(
        label="Lejupielādēt atskaiti (TXT formātā)",
        data=atskaite_teksts,
        file_name=f"pasnovertesanas_atskaite_{d['nosaukums']}_"
                  f"{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

    st.markdown("---")
    if st.button("Sākt jaunu pašnovērtēšanu", type="primary"):
        restart()
        st.rerun()

# ─── KĀJENE ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "*Pašnovērtēšanas rīks izstrādāts maģistra darba ietvaros: "
    "Geide I. (2026). Kvalitātes novērtējums un starpdisciplinaritāte "
    "vispārējās vidējās izglītības iestādēs. RTU IEVF. "
    "Darba vadītāja: prof. Inga Lapiņa.*"
)

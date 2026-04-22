import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from data import UNIVERSITIES, TOPICS, generate_events

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CampusPulse · Madrid",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

:root {
  --bg:        #0a0e1a;
  --surface:   #111827;
  --surface2:  #1a2235;
  --accent:    #e8ff47;
  --accent2:   #47c8ff;
  --accent3:   #ff6b6b;
  --text:      #f0f4ff;
  --muted:     #8892aa;
  --border:    rgba(255,255,255,0.07);
  --radius:    14px;
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 3rem; max-width: 1300px; }

section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

div[data-baseweb="select"] > div {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text) !important;
}
div[data-baseweb="select"] span { color: var(--text) !important; }
div[data-baseweb="popover"] { background: var(--surface2) !important; }
li[role="option"] { color: var(--text) !important; background: var(--surface2) !important; }
li[role="option"]:hover { background: var(--surface) !important; }

div[data-testid="stRadio"] label {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.5rem 1.1rem;
  margin: 0.2rem;
  cursor: pointer;
  transition: all .2s;
  color: var(--text) !important;
}
div[data-testid="stRadio"] label:hover { border-color: var(--accent); }

.stButton > button {
  background: var(--accent) !important;
  color: #0a0e1a !important;
  border: none !important;
  border-radius: var(--radius) !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  padding: 0.65rem 1.8rem !important;
  transition: all .2s !important;
  box-shadow: 0 4px 20px rgba(232,255,71,0.25) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(232,255,71,0.4) !important;
}

div[data-testid="metric-container"] {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.2rem;
}
div[data-testid="metric-container"] label { color: var(--muted) !important; font-size: 0.78rem !important; letter-spacing: 0.06em; text-transform: uppercase; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: var(--accent) !important; font-family: 'Syne', sans-serif; font-size: 1.8rem !important; }

details { background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; }
summary { color: var(--text) !important; font-family: 'Syne', sans-serif; font-weight: 600; }

.stDataFrame { border-radius: var(--radius); overflow: hidden; }
hr { border-color: var(--border) !important; }
div[data-testid="stAlert"] { border-radius: var(--radius) !important; border: 1px solid var(--border) !important; }
div[data-testid="stProgress"] > div > div { background: var(--accent) !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 3px; }

.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: clamp(2.2rem, 5vw, 3.6rem);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.02em;
  margin-bottom: 0.3rem;
}
.hero-accent { color: var(--accent); }
.hero-sub {
  color: var(--muted);
  font-size: 1.05rem;
  font-weight: 300;
  margin-bottom: 2rem;
}
.section-label {
  font-family: 'Syne', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 0.6rem;
}
.event-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.4rem 1.6rem;
  margin-bottom: 1rem;
  transition: border-color .2s, box-shadow .2s;
  position: relative;
  overflow: hidden;
}
.event-card:hover {
  border-color: rgba(232,255,71,0.35);
  box-shadow: 0 4px 30px rgba(232,255,71,0.08);
}
.event-card::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 3px;
  background: var(--accent);
  border-radius: 2px 0 0 2px;
}
.event-card.blue::before { background: var(--accent2); }
.event-card.red::before  { background: var(--accent3); }

.event-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.3rem;
}
.event-meta {
  color: var(--muted);
  font-size: 0.85rem;
  margin-bottom: 0.6rem;
}
.event-desc {
  font-size: 0.92rem;
  line-height: 1.6;
  color: #c5cde0;
}
.pill {
  display: inline-block;
  background: rgba(232,255,71,0.12);
  color: var(--accent);
  border: 1px solid rgba(232,255,71,0.25);
  border-radius: 50px;
  padding: 0.18rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  margin-right: 0.4rem;
  margin-bottom: 0.4rem;
}
.pill.blue {
  background: rgba(71,200,255,0.12);
  color: var(--accent2);
  border-color: rgba(71,200,255,0.25);
}
.pill.red {
  background: rgba(255,107,107,0.12);
  color: var(--accent3);
  border-color: rgba(255,107,107,0.25);
}
.attendee-bar {
  background: rgba(255,255,255,0.05);
  border-radius: 50px;
  height: 6px;
  margin-top: 0.6rem;
  overflow: hidden;
}
.attendee-fill {
  height: 100%;
  background: var(--accent);
  border-radius: 50px;
}
.stat-row {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-top: 0.8rem;
  font-size: 0.82rem;
  color: var(--muted);
}
.stat-row span { color: var(--text); font-weight: 500; }
.sidebar-brand {
  font-family: 'Syne', sans-serif;
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  padding: 1rem 0 0.2rem;
}
.sidebar-brand span { color: var(--accent); }
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--muted);
}
.empty-icon { font-size: 3.5rem; margin-bottom: 1rem; }
.empty-title { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; color: var(--text); margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ───────────────────────────────────────────────────────────────
events_df = generate_events()

# ─── SESSION STATE ───────────────────────────────────────────────────────────
if "registrations" not in st.session_state:
    st.session_state.registrations = {}
if "saved" not in st.session_state:
    st.session_state.saved = set()
if "page" not in st.session_state:
    st.session_state.page = "Explore"

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">Campus<span>Pulse</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="color:var(--muted);font-size:0.8rem;margin-bottom:1.5rem;">Madrid · University Events</div>', unsafe_allow_html=True)
    st.divider()

    page = st.radio(
        "Navigation",
        ["🔍 Explore", "📌 Saved", "📊 Statistics", "🎓 My Profile"],
        label_visibility="collapsed"
    )
    st.session_state.page = page

    st.divider()

    st.markdown('<div class="section-label">University</div>', unsafe_allow_html=True)
    university = st.selectbox(
        "University",
        ["All"] + list(UNIVERSITIES.keys()),
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label" style="margin-top:1rem">Topic</div>', unsafe_allow_html=True)
    topic = st.selectbox(
        "Topic",
        ["All"] + list(TOPICS.keys()),
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label" style="margin-top:1rem">Period</div>', unsafe_allow_html=True)
    period = st.radio(
        "Period",
        ["This week", "This month", "This semester"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label" style="margin-top:1rem">Format</div>', unsafe_allow_html=True)
    fmt_filter = st.multiselect(
        "Format",
        ["In-person", "Online", "Hybrid"],
        default=["In-person", "Online", "Hybrid"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label" style="margin-top:1rem">Max price (€)</div>', unsafe_allow_html=True)
    max_price = st.slider("Max price", 0, 100, 100, label_visibility="collapsed")

    st.divider()
    st.markdown(f'<div style="color:var(--muted);font-size:0.8rem;text-align:center">{len(events_df)} events in the database</div>', unsafe_allow_html=True)


# ─── FILTER LOGIC ────────────────────────────────────────────────────────────
now = datetime.now()

def filter_by_period(df, period):
    if period == "This week":
        limit = now + timedelta(days=7)
    elif period == "This month":
        limit = now + timedelta(days=30)
    else:
        limit = now + timedelta(days=120)
    return df[(df["date"] >= now) & (df["date"] <= limit)]

df = events_df.copy()
if university != "All":
    df = df[df["university"] == university]
if topic != "All":
    df = df[df["topic"] == topic]
df = filter_by_period(df, period)
if fmt_filter:
    df = df[df["format"].isin(fmt_filter)]
df = df[df["price"] <= max_price]
df = df.sort_values("date")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: EXPLORE
# ════════════════════════════════════════════════════════════════════════════
if "Explore" in st.session_state.page:

    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("""
        <div class="hero-title">
            Discover events<br><span class="hero-accent">at your university</span>
        </div>
        <div class="hero-sub">Madrid · Connect, learn and participate with your university community</div>
        """, unsafe_allow_html=True)
    with col_h2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("Today", now.strftime("%d %b %Y"))
        st.metric("Events found", len(df))

    st.divider()

    # ── Featured events ──
    featured = df[df["featured"] == True].head(3)
    if len(featured) > 0:
        st.markdown('<div class="section-label">⭐ Featured events</div>', unsafe_allow_html=True)
        cols_feat = st.columns(min(3, len(featured)))
        for i, (_, ev) in enumerate(featured.iterrows()):
            with cols_feat[i]:
                pct = int(ev["attendees"] / ev["capacity"] * 100)
                color_pct = "#e8ff47" if pct < 70 else "#ff6b6b"
                st.markdown(f"""
                <div class="event-card" style="border-color:rgba(232,255,71,0.3)">
                  <div class="event-title">{ev['emoji']} {ev['title']}</div>
                  <div class="event-meta">📅 {ev['date'].strftime('%d %b · %H:%M')} &nbsp;|&nbsp; 📍 {ev['venue']}</div>
                  <div style="margin:0.4rem 0">
                    <span class="pill">{ev['topic']}</span>
                    <span class="pill blue">{ev['format']}</span>
                  </div>
                  <div class="attendee-bar"><div class="attendee-fill" style="width:{pct}%;background:{color_pct}"></div></div>
                  <div class="stat-row">
                    👥 <span>{ev['attendees']}</span>/{ev['capacity']} registered &nbsp;·&nbsp;
                    {'🆓 Free' if ev['price'] == 0 else f'💶 {ev["price"]}€'}
                  </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Full event list ──
    st.markdown(f'<div class="section-label">📋 All events ({len(df)})</div>', unsafe_allow_html=True)

    if len(df) == 0:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">🔭</div>
          <div class="empty-title">No events match your filters</div>
          <div>Try expanding the period or changing the topic</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for _, ev in df.iterrows():
            eid = ev["id"]
            registered = st.session_state.registrations.get(eid, False)
            bookmarked = eid in st.session_state.saved
            pct = int(ev["attendees"] / ev["capacity"] * 100)

            urgency = ""
            if pct >= 90:
                urgency = ' <span class="pill red">Almost full!</span>'
            elif pct >= 70:
                urgency = ' <span class="pill" style="background:rgba(255,165,0,.15);color:orange;border-color:rgba(255,165,0,.3)">Few spots left</span>'

            card_color = "blue" if registered else ""

            col_ev, col_btn = st.columns([5, 1])
            with col_ev:
                st.markdown(f"""
                <div class="event-card {card_color}">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div>
                      <div class="event-title">{ev['emoji']} {ev['title']}</div>
                      <div class="event-meta">
                        📅 {ev['date'].strftime('%A %d %b · %H:%M')} &nbsp;·&nbsp;
                        🏛️ {ev['university']} &nbsp;·&nbsp;
                        📍 {ev['venue']}
                      </div>
                    </div>
                    <div style="text-align:right;min-width:80px">
                      <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;color:{'#e8ff47' if ev['price']==0 else 'var(--text)'}">
                        {'FREE' if ev['price']==0 else f'{ev["price"]}€'}
                      </div>
                    </div>
                  </div>
                  <div style="margin:0.5rem 0">
                    <span class="pill">{ev['topic']}</span>
                    <span class="pill blue">{ev['format']}</span>
                    <span class="pill" style="background:rgba(255,255,255,.06);color:var(--muted);border-color:var(--border)">{ev['duration']}</span>
                    {urgency}
                  </div>
                  <div class="event-desc">{ev['description']}</div>
                  <div class="attendee-bar"><div class="attendee-fill" style="width:{pct}%;background:{'#e8ff47' if pct<70 else '#ff6b6b'}"></div></div>
                  <div class="stat-row">
                    👥 <span>{ev['attendees']}</span> people registered out of {ev['capacity']} spots ({pct}% full)
                    &nbsp;·&nbsp; 👤 Organised by: <span>{ev['organiser']}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with col_btn:
                st.markdown("<br><br><br>", unsafe_allow_html=True)
                btn_label = "✅ Registered" if registered else "Register"
                if st.button(btn_label, key=f"reg_{eid}"):
                    st.session_state.registrations[eid] = not registered
                    st.rerun()
                save_label = "📌" if bookmarked else "🔖"
                if st.button(save_label, key=f"sav_{eid}"):
                    if bookmarked:
                        st.session_state.saved.discard(eid)
                    else:
                        st.session_state.saved.add(eid)
                    st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# PAGE: SAVED
# ════════════════════════════════════════════════════════════════════════════
elif "Saved" in st.session_state.page:
    st.markdown('<div class="hero-title">Saved <span class="hero-accent">events</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Your personal list of events of interest</div>', unsafe_allow_html=True)
    st.divider()

    saved_ids = st.session_state.saved
    if not saved_ids:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">🔖</div>
          <div class="empty-title">No saved events yet</div>
          <div>Bookmark events from the Explore section to find them here</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df_saved = events_df[events_df["id"].isin(saved_ids)]
        for _, ev in df_saved.iterrows():
            eid = ev["id"]
            pct = int(ev["attendees"] / ev["capacity"] * 100)
            registered = st.session_state.registrations.get(eid, False)
            col_ev, col_btn = st.columns([5, 1])
            with col_ev:
                st.markdown(f"""
                <div class="event-card">
                  <div class="event-title">{ev['emoji']} {ev['title']}</div>
                  <div class="event-meta">📅 {ev['date'].strftime('%A %d %b · %H:%M')} &nbsp;·&nbsp; 🏛️ {ev['university']}</div>
                  <div style="margin:0.4rem 0"><span class="pill">{ev['topic']}</span><span class="pill blue">{ev['format']}</span></div>
                  <div class="event-desc">{ev['description']}</div>
                  <div class="stat-row">👥 <span>{ev['attendees']}</span>/{ev['capacity']} registered</div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                st.markdown("<br><br>", unsafe_allow_html=True)
                if st.button("✅ Registered" if registered else "Register", key=f"sreg_{eid}"):
                    st.session_state.registrations[eid] = not registered
                    st.rerun()
                if st.button("🗑️ Remove", key=f"sdel_{eid}"):
                    st.session_state.saved.discard(eid)
                    st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# PAGE: STATISTICS
# ════════════════════════════════════════════════════════════════════════════
elif "Statistics" in st.session_state.page:
    st.markdown('<div class="hero-title">General <span class="hero-accent">statistics</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Data on university activity across Madrid</div>', unsafe_allow_html=True)
    st.divider()

    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Total events", len(events_df))
    with k2: st.metric("Universities", events_df["university"].nunique())
    with k3: st.metric("Topics", events_df["topic"].nunique())
    with k4: st.metric("Total registrations", f"{events_df['attendees'].sum():,}")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-label">Events by university</div>', unsafe_allow_html=True)
        univ_count = events_df["university"].value_counts().reset_index()
        univ_count.columns = ["University", "Events"]
        fig = px.bar(univ_count, x="Events", y="University", orientation="h",
                     color="Events", color_continuous_scale=["#1a2235","#e8ff47"], template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_family="DM Sans", font_color="#8892aa",
                          coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0), height=380)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-label">Distribution by topic</div>', unsafe_allow_html=True)
        tem_count = events_df["topic"].value_counts().reset_index()
        tem_count.columns = ["Topic", "Events"]
        colors = ["#e8ff47","#47c8ff","#ff6b6b","#a78bfa","#34d399","#fb923c","#f472b6","#60a5fa","#fbbf24","#4ade80"]
        fig2 = px.pie(tem_count, names="Topic", values="Events",
                      color_discrete_sequence=colors, template="plotly_dark", hole=0.45)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="DM Sans", font_color="#f0f4ff",
                           margin=dict(l=0,r=0,t=10,b=0), height=380, legend=dict(font=dict(size=11)))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-label">Average occupancy by topic (%)</div>', unsafe_allow_html=True)
        events_df["occupancy"] = (events_df["attendees"] / events_df["capacity"] * 100).round(1)
        ocu = events_df.groupby("topic")["occupancy"].mean().reset_index().sort_values("occupancy", ascending=True)
        fig3 = px.bar(ocu, x="occupancy", y="topic", orientation="h",
                      color="occupancy", color_continuous_scale=["#1a2235","#47c8ff"],
                      template="plotly_dark", labels={"occupancy":"Occupancy (%)","topic":""})
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_family="DM Sans", font_color="#8892aa",
                           coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0), height=350)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-label">Events by format</div>', unsafe_allow_html=True)
        fmt_count = events_df["format"].value_counts().reset_index()
        fmt_count.columns = ["Format", "Count"]
        fig4 = px.pie(fmt_count, names="Format", values="Count",
                      color_discrete_sequence=["#e8ff47","#47c8ff","#ff6b6b"],
                      template="plotly_dark", hole=0.5)
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="DM Sans", font_color="#f0f4ff",
                           margin=dict(l=0,r=0,t=10,b=0), height=350)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-label">Top 10 most popular events</div>', unsafe_allow_html=True)
    top10 = events_df.nlargest(10, "attendees")[["title","university","topic","attendees","capacity","date"]].copy()
    top10["date"] = top10["date"].dt.strftime("%d %b %Y")
    top10.columns = ["Event","University","Topic","Attendees","Capacity","Date"]
    st.dataframe(top10, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: MY PROFILE
# ════════════════════════════════════════════════════════════════════════════
elif "Profile" in st.session_state.page:
    st.markdown('<div class="hero-title">My <span class="hero-accent">profile</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Your activity on CampusPulse</div>', unsafe_allow_html=True)
    st.divider()

    reg_ids = [k for k, v in st.session_state.registrations.items() if v]
    saved_ids = list(st.session_state.saved)

    p1, p2, p3 = st.columns(3)
    with p1: st.metric("Registered events", len(reg_ids))
    with p2: st.metric("Saved events", len(saved_ids))
    with p3:
        all_ids = reg_ids + saved_ids
        uni_count = events_df[events_df["id"].isin(all_ids)]["university"].nunique() if all_ids else 0
        st.metric("Universities explored", uni_count)

    st.markdown("<br>", unsafe_allow_html=True)

    if reg_ids:
        st.markdown('<div class="section-label">My registrations</div>', unsafe_allow_html=True)
        df_mine = events_df[events_df["id"].isin(reg_ids)].sort_values("date")
        for _, ev in df_mine.iterrows():
            days_left = (ev["date"] - now).days
            countdown = f"In {days_left} days" if days_left > 0 else "Today!"
            st.markdown(f"""
            <div class="event-card blue">
              <div style="display:flex;justify-content:space-between">
                <div>
                  <div class="event-title">{ev['emoji']} {ev['title']}</div>
                  <div class="event-meta">📅 {ev['date'].strftime('%A %d %b · %H:%M')} &nbsp;·&nbsp; 🏛️ {ev['university']}</div>
                </div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:var(--accent2);font-size:0.95rem;min-width:80px;text-align:right">{countdown}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">🎟️</div>
          <div class="empty-title">You haven't registered for any events yet</div>
          <div>Explore available events and join the ones that interest you</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("""
<div style="text-align:center;color:var(--muted);font-size:0.8rem;padding:0.5rem 0">
  CampusPulse · Madrid &nbsp;·&nbsp; Connecting the university community &nbsp;·&nbsp; 2025
</div>
""", unsafe_allow_html=True)

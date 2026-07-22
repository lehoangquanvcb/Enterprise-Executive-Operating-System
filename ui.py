
import streamlit as st
from config import COLORS

def inject_css():
    st.markdown(f"""
    <style>
    .stApp{{background:{COLORS['background']};color:{COLORS['text']}}}
    [data-testid="stSidebar"]{{background:{COLORS['surface']};border-right:1px solid {COLORS['border']}}}
    .block-container{{padding-top:.75rem;padding-bottom:2rem;max-width:1650px}}
    div[data-testid="stMetric"]{{background:linear-gradient(145deg,{COLORS['surface']},{COLORS['surface2']});
      border:1px solid {COLORS['border']};border-radius:14px;padding:14px;box-shadow:0 5px 18px rgba(0,0,0,.22)}}
    div[data-testid="stMetricLabel"]{{color:{COLORS['muted']}}}
    div[data-testid="stMetricValue"]{{color:#F8FAFC}}
    .exec-card{{background:{COLORS['surface']};border:1px solid {COLORS['border']};border-left:5px solid {COLORS['primary']};
      padding:13px 16px;border-radius:9px;margin:7px 0;color:{COLORS['text']}}}
    .critical{{border-left-color:{COLORS['critical']}}}.warning{{border-left-color:{COLORS['warning']}}}
    .positive{{border-left-color:{COLORS['positive']}}}.info{{border-left-color:{COLORS['info']}}}
    .section-label{{color:{COLORS['muted']};font-size:.78rem;text-transform:uppercase;letter-spacing:.12em;margin-top:12px}}
    .pill{{display:inline-block;background:{COLORS['surface2']};border:1px solid {COLORS['border']};padding:4px 9px;
      border-radius:999px;margin-right:6px;font-size:.8rem}}
    div[data-testid="stDataFrame"]{{border:1px solid {COLORS['border']};border-radius:10px}}
    button[data-baseweb="tab"]{{font-size:.92rem}}
    </style>""",unsafe_allow_html=True)

def dark_chart(fig,title=None):
    fig.update_layout(template="plotly_dark",paper_bgcolor=COLORS["background"],plot_bgcolor=COLORS["surface"],
        font=dict(color=COLORS["text"]),title=title,legend_title_text="",margin=dict(l=20,r=20,t=58,b=20))
    fig.update_xaxes(gridcolor=COLORS["border"],zerolinecolor=COLORS["border"])
    fig.update_yaxes(gridcolor=COLORS["border"],zerolinecolor=COLORS["border"])
    return fig

def page_header(title,subtitle=None):
    st.title(title)
    if subtitle: st.caption(subtitle)

def executive_card(topic,finding,action,owner,sla,severity="warning"):
    st.markdown(f'<div class="exec-card {severity}"><b>{topic}</b> — {finding}<br>'
                f'<b>Action:</b> {action} · <b>Owner:</b> {owner} · <b>SLA:</b> {sla}</div>',
                unsafe_allow_html=True)

def metric_row(items):
    cols=st.columns(len(items))
    for c,(label,value,delta) in zip(cols,items):
        c.metric(label,value,delta)

def download_df(df,label,filename):
    st.download_button(label,df.to_csv(index=False).encode("utf-8-sig"),filename,"text/csv",use_container_width=True)

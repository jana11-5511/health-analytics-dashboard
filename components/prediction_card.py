"""Prediction result card used in the calculator view."""
import streamlit as st

from services.model import ModelResult
from styles.theme import ACCENT, ACCENT_3, LINE, MUTED, TEXT, WARN


def render_prediction_card(pred: float, global_avg: float, mr: ModelResult) -> None:
    diff = pred - global_avg
    diff_color = ACCENT_3 if diff >= 0 else WARN
    diff_sign = "+" if diff >= 0 else ""
    pct = (pred - 40) / (90 - 40) * 100
    lo = max(40, pred - 2 * mr.rmse_cv)
    hi = min(90, pred + 2 * mr.rmse_cv)

    st.markdown(f"""
    <div style="background:#FFFFFF; border-radius:16px; border:1px solid {LINE};
                box-shadow:0 4px 20px rgba(0,0,0,0.05); padding: 2rem 1.5rem;
                margin-top:0.5rem; color:{TEXT};">
        <div style="text-align:center;">
            <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase;
                        letter-spacing:0.08em; color:{MUTED}; margin-bottom:0.4rem;">
                Estimación del modelo
            </div>
            <div style="font-size:4.2rem; font-weight:900; color:{ACCENT_3};
                        letter-spacing:-0.04em; line-height:1;">
                {pred:.1f}
                <span style="font-size:1.2rem; font-weight:500; color:{MUTED};">años</span>
            </div>
            <div style="font-size:0.9rem; font-weight:600; color:{diff_color}; margin-top:0.5rem;">
                {diff_sign}{diff:.1f} años vs. media global 2019
            </div>
        </div>
        <div style="margin: 1.5rem 0 1rem 0;">
            <div style="display:flex; justify-content:space-between; font-size:0.7rem;
                        color:{MUTED}; margin-bottom:5px;">
                <span>40 años</span><span>65 años</span><span>90 años</span>
            </div>
            <div style="height:12px; background:#EFF2F7; border-radius:99px; overflow:hidden;">
                <div style="height:100%; width:{pct:.1f}%;
                            background:linear-gradient(90deg, {ACCENT} 0%, {ACCENT_3} 100%);
                            border-radius:99px;"></div>
            </div>
        </div>
        <div style="display:flex; gap:1rem; margin-top:1.5rem;">
            <div style="flex:1; background:#F8FAFC; border-radius:12px; padding:0.9rem;
                        text-align:center; border:1px solid {LINE};">
                <div style="font-size:0.65rem; font-weight:700; text-transform:uppercase;
                            color:{MUTED};">IC Aprox. 95% (±2·RMSE CV)</div>
                <div style="font-size:1rem; font-weight:700; color:{TEXT}; margin-top:0.2rem;">
                    {lo:.1f} – {hi:.1f}
                </div>
            </div>
            <div style="flex:1; background:#F8FAFC; border-radius:12px; padding:0.9rem;
                        text-align:center; border:1px solid {LINE};">
                <div style="font-size:0.65rem; font-weight:700; text-transform:uppercase;
                            color:{MUTED};">RMSE CV GroupKFold(5)</div>
                <div style="font-size:1rem; font-weight:700; color:{TEXT}; margin-top:0.2rem;">
                    ± {mr.rmse_cv:.2f} años
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

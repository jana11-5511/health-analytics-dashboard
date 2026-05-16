"""Generic UI building blocks."""
import streamlit as st

from styles.theme import MUTED, TEXT


def page_header(title: str, subtitle: str, caption: str = "") -> None:
    st.title(title)
    st.markdown(
        f"<p class='page-subtitle'>{subtitle}</p>",
        unsafe_allow_html=True,
    )

    if caption:
        st.caption(caption)


def section_header(title: str, subtitle: str = "") -> None:
    st.markdown(f"""
    <div style="margin: 1.5rem 0 0.6rem 0;">
        <div style="font-size:0.65rem; font-weight:700; text-transform:uppercase;
                    letter-spacing:0.1em; color:{MUTED}; margin-bottom:0.3rem;">
            {subtitle}
        </div>
        <div style="font-size:1rem; font-weight:700; color:{TEXT}; letter-spacing:-0.01em;">
            {title}
        </div>
        <div class="divider" style="margin-top:0.5rem;"></div>
    </div>
    """, unsafe_allow_html=True)


def info_box(text: str) -> None:
    st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)

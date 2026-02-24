import streamlit as st
import bot
import auth


# ------------------------
# Require authentication
# ------------------------
auth.login()


# ------------------------
# Page config
# ------------------------
st.set_page_config(
    page_title="Telegram Sarvam Bot Controller",
    page_icon="🤖",
    layout="centered"
)


# ------------------------
# Title
# ------------------------
st.title("🤖 Telegram Sarvam Bot Controller")


# ------------------------
# Control buttons
# ------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ Start Bot", use_container_width=True):
        bot.start_bot()
        st.success("Bot started successfully")

with col2:
    if st.button("⏹️ Stop Bot", use_container_width=True):
        bot.stop_bot()
        st.warning("Bot stopped")

with col3:
    if st.button("🚪 Logout", use_container_width=True):
        auth.logout()


# ------------------------
# Status display
# ------------------------
st.divider()

status = bot.bot_status()

if status:
    st.success("Status: Running")
else:
    st.error("Status: Stopped")


# ------------------------
# Footer
# ------------------------
st.divider()
st.caption("Sarvam AI Telegram Bot Controller")
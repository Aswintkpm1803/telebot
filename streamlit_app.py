import streamlit as st
import bot

st.title("Telegram Sarvam Bot Controller")

if st.button("Start Bot"):
    bot.start_bot()
    st.success("Bot started")

if st.button("Stop Bot"):
    bot.stop_bot()
    st.warning("Bot stopped")

st.write("Status:", "Running" if bot.bot_status() else "Stopped")
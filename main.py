#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import telebot
from collections import Counter

# ================= CONFIG =================

TOKEN = "8411389818:AAHxBGyonXph2yDJdxXcKft_t9PZjKVUt78"
CHAT_ID = "-1002066596552"

URL = "https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/current/1"

HIST_LEN = 10
SLEEP_TIME = 2.2
MIN_PROB = 0.70
MAX_GALE = 2

bot = telebot.TeleBot(TOKEN)

# ================= SESSION =================

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://blaze.bet.br",
    "Origin": "https://blaze.bet.br"
})

# ================= RUNTIME =================

historico = []
ultimo_id = None
entrada = None
gale = 0

# ================= UTIL =================

def color_to_emoji(v):
    if v == 1 or v == "red":
        return "🔴"
    if v == 2 or v == "black":
        return "⚫"
    return None

def send(msg):
    try:
        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
    except:
        pass

def probabilidade(hist):
    cnt = Counter(hist)
    total = cnt["🔴"] + cnt["⚫"]
    if total == 0:
        return None

    p_red = cnt["🔴"] / total
    p_black = cnt["⚫"] / total

    if p_red >= MIN_PROB:
        return "⚫", p_red, p_black
    if p_black >= MIN_PROB:
        return "🔴", p_red, p_black

    return None

# ================= START =================

send("🤖 *BOT PROBABILIDADE INICIADO*\n📡 Histórico ao vivo (10 rodadas)")

while True:
    try:
        data = session.get(URL, timeout=10).json()
    except:
        time.sleep(SLEEP_TIME)
        continue

    game_id = data.get("id")
    color = color_to_emoji(data.get("color"))

    if not game_id or game_id == ultimo_id or not color:
        time.sleep(SLEEP_TIME)
        continue

    ultimo_id = game_id

    historico.append(color)
    historico = historico[-HIST_LEN:]

    hist_str = " ".join(historico)

    # ================= FECHAMENTO =================
    if entrada:
        if color == entrada:
            send(f"🟢 *GREEN*\nHistórico: {hist_str}")
            entrada = None
            gale = 0
        else:
            gale += 1
            if gale > MAX_GALE:
                send(f"🔴 *LOSS*\nHistórico: {hist_str}")
                entrada = None
                gale = 0

    # ================= NOVA ANÁLISE =================
    if entrada is None and len(historico) >= HIST_LEN:
        res = probabilidade(historico)
        if res:
            entrada_cor, p_red, p_black = res

            send(
                "⚠️ *PRÉ-SINAL DETECTADO*\n"
                f"Histórico: {hist_str}\n"
                f"🔴 {p_red*100:.1f}% | ⚫ {p_black*100:.1f}%"
            )

            time.sleep(SLEEP_TIME)

            entrada = entrada_cor
            gale = 0

            send(
                "🎯 *ENTRADA POR PROBABILIDADE*\n"
                f"Histórico: {hist_str}\n"
                f"🔴 {p_red*100:.1f}% | ⚫ {p_black*100:.1f}%\n"
                f"Entrada: *{entrada}*\n"
                f"Gale: até {MAX_GALE}"
            )

    time.sleep(SLEEP_TIME)

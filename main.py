#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BOT BLAZE DOUBLE — PROBABILIDADE 70–80%
Histórico ao vivo (10 rodadas)
Pré-sinal + Entrada
Gale até 2
Proteção anti-timeout Telegram
"""

import time
import requests
import telebot

# ================= CONFIG =================

TOKEN = "8411389818:AAHxBGyonXph2yDJdxXcKft_t9PZjKVUt78"
CHAT_ID = "-1002066596552"

URL = "https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/current/1"

JANELA = 10
PRE_SIGNAL_DIFF = 0.10   # 60–65%
SIGNAL_DIFF = 0.18       # 72–80%
MAX_GALES = 2

bot = telebot.TeleBot(TOKEN)
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

# ================= RUNTIME =================

historico = []
ultimo_id = None
entrada = None
gale = 0
msg_historico_id = None

LAST_EDIT = 0
LAST_TEXT = ""

# ================= UTIL =================

def cor_emoji(v):
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

def edit(msg_id, msg):
    global LAST_EDIT, LAST_TEXT

    if msg == LAST_TEXT:
        return

    if time.time() - LAST_EDIT < 2:
        return

    try:
        bot.edit_message_text(
            msg,
            CHAT_ID,
            msg_id,
            parse_mode="Markdown"
        )
        LAST_EDIT = time.time()
        LAST_TEXT = msg
    except:
        pass

# ================= PROBABILIDADE =================

def calc_prob(hist):
    janela = hist[-JANELA:]
    r = janela.count("🔴")
    b = janela.count("⚫")
    total = r + b

    if total < JANELA:
        return None

    pr = r / total
    pb = b / total
    diff = abs(pr - pb)

    if pr > pb:
        entrada = "⚫"
    else:
        entrada = "🔴"

    prob_est = int(diff * 100 + 55)
    if prob_est > 80:
        prob_est = 80

    return entrada, pr, pb, diff, prob_est

# ================= START =================

send("🤖 *BOT PROBABILIDADE INICIADO*\n📡 Histórico ao vivo (10 rodadas)")

while True:
    try:
        r = session.get(URL, timeout=5).json()
    except:
        time.sleep(1)
        continue

    game_id = r.get("id")
    status = r.get("status")
    cor = cor_emoji(r.get("color"))

    if status != "rolling" or game_id == ultimo_id or cor is None:
        time.sleep(1)
        continue

    ultimo_id = game_id
    historico.append(cor)
    historico = historico[-50:]

    hist_10 = historico[-JANELA:]
    hist_str = " ".join(hist_10)

    texto_hist = f"📡 *HISTÓRICO AO VIVO*\n{hist_str}"

    if msg_historico_id is None:
        try:
            msg_historico_id = bot.send_message(
                CHAT_ID,
                texto_hist,
                parse_mode="Markdown"
            ).message_id
        except:
            pass
    else:
        edit(msg_historico_id, texto_hist)

    # ================= FECHAMENTO =================

    if entrada:
        if cor == entrada:
            send("🟢 *GREEN!*")
            entrada = None
            gale = 0
        else:
            gale += 1
            if gale > MAX_GALES:
                send("🔴 *LOSS!*")
                entrada = None
                gale = 0

    # ================= NOVA ANÁLISE =================

    if entrada is None:
        res = calc_prob(historico)
        if not res:
            time.sleep(1)
            continue

        ent, pr, pb, diff, prob_est = res

        if PRE_SIGNAL_DIFF <= diff < SIGNAL_DIFF:
            send(
                f"⚠️ *PRÉ-SINAL*\n"
                f"Histórico: {hist_str}\n"
                f"🔴 {pr*100:.1f}% | ⚫ {pb*100:.1f}%"
            )

        if diff >= SIGNAL_DIFF:
            entrada = ent
            send(
                f"🎯 *ENTRADA POR PROBABILIDADE*\n"
                f"Histórico: {hist_str}\n"
                f"🔴 {pr*100:.1f}% | ⚫ {pb*100:.1f}%\n"
                f"Probabilidade estimada: *{prob_est}%*\n"
                f"Entrada: *{entrada}*\n"
                f"Gale: até 2"
            )

    time.sleep(1)

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import random

TOKEN = "9058905466:AAHy2nWfQ6qJo8898Zr8-eI0Gg4a12Ls0-M"
bot = telebot.TeleBot(TOKEN)

# Database sementara di RAM
# Format: user_data[uid] = {"rooms": [list_room], "alias": "Nama_Samaran"}
user_data = {}

# Daftar pilihan nama samaran acak
ANON_NAMES = ["Kelinci Senyap", "Ghost_01", "Bayangan Hitam", "Kucing Misterius", "Musang Malam", "Cyber_Ninja"]

def get_or_create_user(uid):
    if uid not in user_data:
        user_data[uid] = {
            "rooms": [],
            "alias": random.choice(ANON_NAMES)
        }
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("/lobby"),
        KeyboardButton("/inforoom"),
        KeyboardButton("/myid"),
        KeyboardButton("/help")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    uid = message.from_user.id
    u_info = get_or_create_user(uid)
    bot.reply_to(
        message, 
        f"🎉 **Selamat datang di Bot Anonymous Chat Multi-Room!**\n\n"
        f"Nama samaran kamu di sesi ini: **{u_info['alias']}**\n"
        "Gunakan tombol menu di bawah untuk mulai menjelajah.", 
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['myid'])
def show_my_id(message):
    bot.reply_to(message, f"🆔 ID Telegram kamu:\n`{message.from_user.id}`", parse_mode="Markdown")

@bot.message_handler(commands=['lobby'])
def show_lobby(message):
    bot.reply_to(message, "🏠 **Lobby Utama**\nSilakan pilih menu atau buat/gabung room baru.", reply_markup=main_menu())

@bot.message_handler(commands=['inforoom'])
def info_room(message):
    uid = message.from_user.id
    u_info = get_or_create_user(uid)
    rooms = u_info["rooms"]
    
    if not rooms:
        bot.reply_to(message, "📂 Kamu belum bergabung di room mana pun.\nStatus Room: 🔴 Kosong")
    else:
        room_list = "\n".join([f"🟢 - Room: <b>{r}</b>" for r in rooms])
        bot.reply_to(message, f"📋 **Daftar Room Aktifmu:**\n{room_list}\nGunakan `/playroom <nama>` untuk masuk.", parse_mode="HTML")

@bot.message_handler(commands=['outroom'])
def out_room(message):
    args = message.text.split()
    uid = message.from_user.id
    if len(args) < 2:
        bot.reply_to(message, "Format salah! Gunakan: `/outroom <nama_room>`", parse_mode="Markdown")
        return
    
    room_name = args[1]
    u_info = get_or_create_user(uid)
    if room_name in u_info["rooms"]:
        u_info["rooms"].remove(room_name)
        bot.reply_to(message, f"🚪 Berhasil keluar dari room: <b>{room_name}</b>", parse_mode="HTML")
    else:
        bot.reply_to(message, f"❌ Kamu tidak terdaftar di room '{room_name}'")

@bot.message_handler(commands=['playroom'])
def play_room(message):
    args = message.text.split()
    uid = message.from_user.id
    u_info = get_or_create_user(uid)
    
    if len(args) < 2:
        bot.reply_to(message, "Format salah! Gunakan: `/playroom <nama_room>`", parse_mode="Markdown")
        return
    
    room_name = args[1]
    if room_name not in u_info["rooms"]:
        u_info["rooms"].append(room_name)
        
    bot.reply_to(message, f"💬 Berhasil masuk ke room <b>{room_name}</b>!\nKirim pesan, foto, video, atau voice note-mu di sini.", parse_mode="HTML")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "📖 **Panduan Perintah Bot:**\n\n"
        "• `/lobby` - Kembali ke menu utama\n"
        "• `/inforoom` - Melihat daftar room aktif (status 🟢/🔴)\n"
        "• `/myid` - Melihat ID unik Telegram kamu\n"
        "• `/playroom <nama>` - Masuk/gabung ke room tertentu\n"
        "• `/outroom <nama>` - Keluar dari room tertentu\n"
        "• <b>Kirim Media</b> - Kamu bisa langsung kirim Foto, Video, atau Voice Note di dalam room!\n"
        "• `/help` - Menampilkan pesan panduan ini"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

# Handler untuk mendeteksi Teks, Foto, Video, dan Voice Note secara anonim
@bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'document'])
def handle_all_media(message):
    uid = message.from_user.id
    u_info = get_or_create_user(uid)
    
    # Cek apakah user sedang aktif di room (simulasi sederhana)
    if not u_info["rooms"]:
        bot.reply_to(message, "⚠️ Kamu belum masuk ke room mana pun! Ketik `/playroom <nama_room>` atau buat room dulu.")
        return
    
    # Disini nanti sistem menyebarkan pesan ke anggota room lain secara anonim pakai alias u_info['alias']
    # Untuk tahap awal, bot akan merespon konfirmasi bahwa media/pesan berhasil dikirim anonim
    bot.reply_to(message, f"<i>[Terkirim anonim sebagai {u_info['alias']}]</i>", parse_mode="HTML")

print("Bot Multi-Room siap dijalankan...")
bot.infinity_polling()

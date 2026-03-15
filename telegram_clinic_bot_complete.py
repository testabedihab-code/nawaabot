#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Clinic Management System Bot
بوت تلغرام نظام إدارة العيادة
"""

import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

# ============================================
# 🔧 الإعدادات
# ============================================

TELEGRAM_TOKEN = "8655171413:AAGMNPwcLjO5JDnVZXqAL1YoTgYmg3xy240"

# احصل على مفتاح API من متغير البيئة أو من متغير عام
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    print("❌ خطأ: لم يتم العثور على ANTHROPIC_API_KEY")
    print("يرجى تعيين متغير البيئة: ANTHROPIC_API_KEY")
    sys.exit(1)

# ============================================
# 📚 نص النظام (System Prompt)
# ============================================

SYSTEM_PROMPT = """You are a professional Sales Assistant for the "Clinic Management System" created by NOTE Software Company. Your role is to provide helpful, accurate, and professional information about the system's features and capabilities to potential clients and existing users.

## CLINIC MANAGEMENT SYSTEM OVERVIEW

The Clinic Management System is a comprehensive, modern, and user-friendly platform designed to streamline clinic operations. It includes three main modules: an Appointment Booking System, Nurse Dashboard, and Doctor Dashboard. The system is built with modern web technologies, features Arabic language support (RTL), responsive mobile design, and real-time data management with Firebase.

---

## 1. APPOINTMENT BOOKING SYSTEM (Patient-Facing)

### Key Features:
- **Dual Calendar View**: Patients can choose between a weekly pill-style view or a monthly grid calendar
- **Smart Date Selection**: Only allows selection of future dates; past and weekend dates are disabled
- **Time Period Selection**: Morning (صباحي) and Evening (مسائي) time slots with visual icons and animations
- **Visit Type Selection**: Multiple appointment types available (General, Checkup, Consultation, Follow-up, etc.)
- **Patient Information Form**: 
  - Name (minimum 2 characters)
  - Phone number (validated for Saudi format: 05XXXXXXXX)
  - Birth date/Age
  - Address
  - Optional notes field
- **Real-Time Validation**: Form field validation with error messages displayed in Arabic
- **Success Confirmation Screen**: Shows booking confirmation with all appointment details
- **Toast Notifications**: Real-time success/error notifications
- **Responsive Design**: Fully optimized for mobile, tablet, and desktop
- **Firebase Integration**: Appointments stored in real-time Firebase database
- **Professional UI/UX**:
  - Teal color scheme (#0d6b63, #0a4f49)
  - Smooth animations and transitions
  - Hero section with doctor photo placeholder
  - Statistics section showing key metrics
  - Smooth scrolling and focus management

### Technical Specifications:
- Language: Arabic (RTL layout)
- Framework: Vanilla HTML5, CSS3, JavaScript
- Database: Firebase Realtime Database
- Fonts: Tajawal (Arabic), DM Mono
- Mobile-First Design: Responsive from 320px to desktop

---

## 2. NURSE DASHBOARD

### Key Features:

#### Appointment Management:
- **Appointments Tab**: View all appointments in a detailed list format
- **Filtering Options**: Filter by status (All, Confirmed, Pending, Completed, Cancelled) and by date ranges
- **Search Functionality**: Search appointments by patient name or phone number
- **Appointment Details**:
  - Patient name, phone, birth date
  - Visit type and appointment date/time
  - Current status with color-coded indicators
  - Address and notes

#### Patient Management:
- **Patient Records**: Complete patient profile management
- **Contact Information**: Phone number, date of birth, address
- **Appointment History**: View all past and future appointments for each patient
- **Notes**: Add and manage patient notes
- **Patient Card Design**: Clean, organized card layout with all essential information

#### Statistics & Analytics:
- **Total Patients**: Count of all registered patients
- **Pending Appointments**: Number of appointments awaiting confirmation
- **Completed Appointments**: Count of finished appointments
- **Appointment Rate**: Visual representation of appointment completion rate
- **Interactive Stats**: Hover effects and real-time updates

#### Smart Archive Feature:
- **Period Comparison**: Compare appointment data across different time periods
- **Patient Timeline**: Visual timeline of patient interactions
- **Report Tab**: Time-range selectors for generating reports
- **Color-Coded Cards**: Different colors for appointment status

---

## 3. DOCTOR DASHBOARD

### Key Features:
- **Compact Month Calendar**: Mini calendar for quick date navigation
- **Calendar Grid**: Visual appointment density indicators
- **Color-Coded Appointments**: Priority levels (low/medium/high)
- **Day Selection**: Click dates to see detailed daily agenda
- **Daily Schedule**: All appointments for selected day in chronological order
- **Patient Book (Directory)**: Complete list of all patients
- **Search Function**: Search patients by name or phone
- **Patient Details Modal**: Full patient information and history
- **Notes Management**: Add and edit notes for each patient visit
- **Statistics Section**: Patient counts, appointment metrics, completion rates
- **Auto-Refresh**: Dashboard updates automatically every 5 seconds

---

## SYSTEM CAPABILITIES & BENEFITS

### For Clinics:
✓ Complete appointment management workflow
✓ Efficient nurse operations with smart filtering
✓ Doctor access to patient history and notes
✓ Real-time data synchronization
✓ Professional, modern interface
✓ Mobile-responsive design
✓ Automated appointment confirmation process

### For Staff:
✓ Easy-to-use, intuitive dashboards
✓ Minimal training required
✓ Real-time notifications and updates
✓ Quick patient information access
✓ Efficient appointment navigation

### For Patients:
✓ Simple, streamlined booking process
✓ Flexible date and time selection
✓ Instant confirmation
✓ Mobile app compatible

---

## TONE & COMMUNICATION GUIDELINES

- Always be professional and courteous
- Respond in Arabic when customer uses Arabic
- Respond in English when customer uses English
- Be specific about features and benefits
- Admit when you don't have specific information
- Recommend contacting NOTE Software Company for technical/commercial details
- Provide examples when explaining features
- Ask clarifying questions to better serve customer needs
- Focus on customer benefits and pain-point solutions

You are knowledgeable, professional, and customer-focused."""

# ============================================
# 💾 تخزين المحادثات
# ============================================

conversation_history = {}

# ============================================
# 🤖 الدوال الرئيسية
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """أمر /start - البداية"""
    user_id = update.effective_user.id
    conversation_history[user_id] = []
    
    welcome_text = """👋 مرحباً بك في نظام إدارة العيادة!

أنا مساعدك في التعرف على نظام إدارة العيادة من NOTE Software Company.

أستطيع مساعدتك في:
✓ شرح مميزات النظام
✓ الإجابة على أسئلتك عن الحجز والمواعيد
✓ معلومات عن لوحات تحكم الممرضات والأطباء
✓ توضيح الميزات التقنية
✓ والمزيد!

اسأل أي سؤال وسأكون سعيداً بمساعدتك! 😊

استخدم /help لمعرفة المواضيع المتاحة"""
    
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """أمر /help - المساعدة"""
    help_text = """📚 المواضيع التي يمكنك السؤال عنها:

1️⃣ **نظام الحجز** - كيفية عمل نظام حجز المواعيد للمرضى
2️⃣ **لوحة الممرضة** - إدارة المواعيد والمرضى
3️⃣ **لوحة الطبيب** - جدول المواعيد والملاحظات
4️⃣ **المميزات التقنية** - Firebase, الواجهات الحديثة, RTL
5️⃣ **الأمان والبيانات** - حماية البيانات والتخزين
6️⃣ **التكامل والتخصيص** - الإمكانيات التقنية
7️⃣ **الأسعار والتطبيق** - للتواصل مع الشركة

اكتب سؤالك وسأجيب عليه بشكل مفصل! 💬"""
    
    await update.message.reply_text(help_text)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """أمر /about - معلومات النظام"""
    about_text = """ℹ️ **عن نظام إدارة العيادة**

نظام إدارة العيادة من NOTE Software Company هو حل شامل وحديث لتنظيم عمليات العيادات.

**المكونات الرئيسية:**
1. نظام حجز المواعيد (للمرضى)
2. لوحة تحكم الممرضات (إدارة المواعيد والمرضى)
3. لوحة تحكم الأطباء (الجدول والملاحظات)

**المميزات:**
✨ دعم كامل للغة العربية (RTL)
✨ تصميم متجاوب مع جميع الأجهزة
✨ تكامل مع Firebase للبيانات الفورية
✨ واجهة حديثة وسهلة الاستخدام
✨ إمكانيات عمل بدون إنترنت

للمزيد من المعلومات، اسأل عن موضوع محدد! 📱"""
    
    await update.message.reply_text(about_text)


async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """أمر /clear - مسح السجل"""
    user_id = update.effective_user.id
    conversation_history[user_id] = []
    await update.message.reply_text("✅ تم مسح السجل. بدء محادثة جديدة!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج الرسائل - يستخدم Claude AI"""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # إظهار "يكتب..."
    await update.message.chat.send_action("typing")
    
    # إضافة الرسالة للسجل
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    conversation_history[user_id].append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # إنشاء عميل Anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        # استدعاء Claude API
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=conversation_history[user_id]
        )
        
        assistant_message = response.content[0].text
        
        # إضافة الرد للسجل
        conversation_history[user_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        # تقسيم الرد إذا كان طويلاً (حد أقصى 4096 حرف)
        if len(assistant_message) > 4096:
            messages = [assistant_message[i:i+4096] for i in range(0, len(assistant_message), 4096)]
            for msg in messages:
                await update.message.reply_text(msg)
        else:
            await update.message.reply_text(assistant_message)
            
    except anthropic.APIError as e:
        error_message = f"❌ خطأ في الاتصال: {str(e)}\n\nيرجى التأكد من مفتاح API والاتصال بالإنترنت."
        await update.message.reply_text(error_message)
        # إزالة الرسالة من السجل في حالة الخطأ
        if user_id in conversation_history and conversation_history[user_id]:
            conversation_history[user_id].pop()
    except Exception as e:
        error_message = f"❌ حدث خطأ غير متوقع: {str(e)}"
        await update.message.reply_text(error_message)
        if user_id in conversation_history and conversation_history[user_id]:
            conversation_history[user_id].pop()


# ============================================
# 🚀 تشغيل البوت
# ============================================

def main():
    """تشغيل البوت الرئيسي"""
    print("=" * 50)
    print("🤖 بوت تلغرام نظام إدارة العيادة")
    print("Clinic Management System Telegram Bot")
    print("=" * 50)
    
    # إنشء التطبيق
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("clear", clear_history))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("\n✅ تم تحميل المعالجات")
    print("🚀 البوت يعمل الآن...")
    print("⏹️  اضغط Ctrl+C للإيقاف\n")
    
    # بدء البوت
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

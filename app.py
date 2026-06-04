from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# كلمة السر الخاصة بك لإدارة الموقع (يمكنك تغييرها)
ADMIN_PASSWORD = "132"

# بيانات الموقع التي يمكن تعديلها من لوحة التحكم
site_data = {
    "welcome_msg": "==================================================\n🤖 مرحباً بك في نظام الفحص والمحاكاة الذكي v3.5 🤖\n==================================================\n\n[+] تم الاتصال بالسيرفر بنجاح... [ONLINE]\n[+] بيئة العمل آمنة وجاهزة للتجربة 🚀\n\nمهمتنا هنا هي مساعدتك على احتراف تطبيق Termux وتخطي كل العقبات.\n\n💡 جرب الآن كتابة الأوامر التالية في الشاشة:\n• اكتب [termux-style] لتغيير شكل وألوان الترمينال بالكامل 🎨\n• اكتب [pkg install tools] لمحاكاة تثبيت الأدوات الأساسية 📦\n• أو ببساطة: الصق أي كود خطأ (Error) يواجهك في هاتفك هنا ليقوم النظام بتحليله وإعطائك الحل فوراً!\n\n~ ابدأ بكتابة أول أمر الآن، ودعنا نتعلم معاً...",
    "custom_tip": "💡 نصيحة: اكتب 'termux-style' لرؤية أنماط الشكل، أو الصق خطأ واجهك ليقوم السيرفر بحله!"
}

# 🔥 قاموس الأخطاء المطور الذي يحتوي على أخطائك الحقيقية
ERROR_SOLUTIONS = {
    "permission denied": "❌ خطأ في الصلاحيات!\n💡 التشخيص: تيرمكس لا يملك صلاحية الوصول لذاكرة الهاتف الداخلية.\n➡️ الحل: اكتب الأمر التالي لإعطائه الصلاحية:\ntermux-setup-storage",
    
    "not installed": "❌ خطأ عدم وجود حزمة الـ SSH!\n💡 التشخيص: الأداة غير مثبتة في نسختك الحالية وتيرمكس يحتاج لتثبيتها.\n➡️ الحل: اكتب هذا الأمر لتثبيت حزمة الاتصال الآمن:\npkg install openssh -y",
    
    "ffmpeg": "❌ خطأ تعطل التحديثات والمستودعات (Repository Error)!\n💡 التشخيص: السيرفر الافتراضي الذي يحاول تحميل حزمة ffmpeg يواجه عطلاً.\n➡️ الحل: اكتب الأمر التالي وغير السيرفر الافتراضي إلى سيرفر آخر مستقر:\ntermux-change-repo",
    
    "modulenotfounderror": "❌ خطأ مكتبة بايثون مفقودة (Module Not Found)!\n💡 التشخيص: سكربت البايثون الخاص بك يحتاج مكتبة خارجية لم تقم بتحميلها بعد.\n➡️ الحل: ثبت المكتبة الناقصة عبر أداة pip (مثال لـ speech_recognition):\npip install speech_recognition"
}

@app.route('/')
def home():
    return render_template('index.html', welcome=site_data["welcome_msg"], tip=site_data["custom_tip"])

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            new_welcome = request.form.get('welcome_msg')
            new_tip = request.form.get('custom_tip')
            if new_welcome: site_data["welcome_msg"] = new_welcome
            if new_tip: site_data["custom_tip"] = new_tip
            msg = "✅ تم تحديث بيانات ومحتوى الموقع بنجاح!"
        else:
            msg = "❌ كلمة السر خاطئة! لا يمكن التعديل."
    return render_template('admin.html', current_welcome=site_data["welcome_msg"], current_tip=site_data["custom_tip"], message=msg)

@app.route('/terminal-input', methods=['POST'])
def terminal_input():
    user_text = request.form.get('text', '').lower().strip()
    response = ""
    action = "print"

    if user_text == "clear":
        action = "clear"
    elif user_text == "ls":
        response = "📁 tools_box  📁 themes  📄 app.py  📄 templates"
    elif user_text == "pkg install tools":
        action = "install_animation"
        response = "جاري تثبيت الحزم الأساسية (git, python, nano, curl)..."
    elif user_text == "termux-style":
        response = "🎨 [قائمة الأنماط المتاحة]:\n1) اكتب 'style 1' (Cyberpunk 🌌)\n2) اكتب 'style 2' (Matrix 🟢)\n3) اكتب 'style 3' (Dracula 🧛)"
    elif user_text == "style 1": action = "change_theme_cyber"; response = "🌌 تم تطبيق نمط Cyberpunk!"
    elif user_text == "style 2": action = "change_theme_matrix"; response = "🟢 تم تطبيق نمط Matrix!"
    elif user_text == "style 3": action = "change_theme_dracula"; response = "🧛 تم تطبيق نمط Dracula!"
    else:
        # فحص ذكي للنص إذا كان يحتوي على أي خطأ من الأخطاء المضافة
        found_solution = False
        for error_key, solution in ERROR_SOLUTIONS.items():
            if error_key in user_text:
                response = solution
                found_solution = True
                break
        if not found_solution:
            response = f"termux: {user_text}: command not found\n{site_data['custom_tip']}"

    return jsonify({"output": response, "action": action})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

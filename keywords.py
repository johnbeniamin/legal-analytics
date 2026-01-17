from collections import Counter
from nltk import ngrams

# === إعدادات التحكم ===
# دي النسبة المئوية اللي هنعتبر الكلمة بعدها "مهمة"
# 0.1% تعني: الكلمة لازم تظهر مرة واحدة على الأقل في كل 1000 كلمة
MIN_PERCENTAGE = 0.1 

# 1. قراءة الملف
with open('data.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 2. القائمة السوداء
stop_words = ["في", "من", "على", "أن", "أو", "هذا", "هذه", "تم", "التي", "الذي", "عن", "كان", "لها", "ذلك", "فى", "و", "بها", "لا", "إلى", "ما", "مع", "كل"]

# 3. التنظيف
text = text.replace("،", " ")
text = text.replace("(", " ")
text = text.replace(")", " ")
text = text.replace("-", " ")
text = text.replace(".", " ")
text = text.replace(":", " ")
text = text.replace("\n", " ")

# 4. التقطيع والفلترة
all_words_raw = text.split() # كل الكلمات قبل الفلترة (عشان نحسب النسبة الصح)
total_count = len(all_words_raw) # العدد الإجمالي (مثلاً 13000)

clean_words = [word for word in all_words_raw if word not in stop_words]

# 5. الحسابات
word_count = Counter(clean_words)

# === المعادلة الذكية ===
# هنا هنحسب النسبة المئوية لكل كلمة ونفلتر بناء عليها
analyzed_data = []

for word, freq in word_count.most_common():
    percentage = (freq / total_count) * 100 # معادلة النسبة المئوية
    
    # الشرط: لو نسبة الكلمة أكبر من الحد الأدنى اللي حطيناه فوق
    if percentage >= MIN_PERCENTAGE:
        analyzed_data.append((word, freq, percentage))

# الطباعة بشكل جدول شيك
print(f"--- تقرير تحليل النص ---")
print(f"إجمالي عدد كلمات الملف: {total_count} كلمة")
print(f"عدد الكلمات المميزة (بدون تكرار): {len(word_count)}")
print("-" * 50)
print(f"{'الكلمة':<15} | {'التكرار':<10} | {'النسبة المئوية'}")
print("-" * 50)

for word, freq, pct in analyzed_data[:30]: # عرض أهم 30 نتيجة
    print(f"{word:<15} | {freq:<10} | {pct:.2f}%")
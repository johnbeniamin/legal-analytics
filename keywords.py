from collections import Counter
from nltk import ngrams
import pandas as pd  # استدعينا وحش البيانات

# === إعدادات التحكم ===
MIN_PERCENTAGE = 0.1 

# 1. قراءة الملف
with open('data.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 2. القائمة السوداء
stop_words = ["في", "من", "على", "أن", "أو", "هذا", "هذه", "تم", "التي", "الذي", "عن", "كان", "لها", "ذلك", "فى", "و", "بها", "لا", "إلى", "ما", "مع", "كل", "أنه"]

# 3. التنظيف
text = text.replace("،", " ")
text = text.replace("(", " ")
text = text.replace(")", " ")
text = text.replace("-", " ")
text = text.replace(".", " ")
text = text.replace(":", " ")
text = text.replace("\n", " ")
text = text.replace('"', " ")

# 4. التقطيع والفلترة
all_words_raw = text.split()
total_count = len(all_words_raw)
clean_words = [word for word in all_words_raw if word not in stop_words]

# 5. الحسابات (الكلمات الفردية)
word_count = Counter(clean_words)
analyzed_data = []

for word, freq in word_count.most_common():
    percentage = (freq / total_count) * 100
    if percentage >= MIN_PERCENTAGE:
        analyzed_data.append({"العبارة": word, "التكرار": freq, "النوع": "كلمة فردية", "النسبة": f"{percentage:.2f}%"})

# 6. الحسابات (العبارات المركبة)
grams = ngrams(clean_words, 2)
phrases = [" ".join(gram) for gram in grams]
phrase_count = Counter(phrases)

for phrase, freq in phrase_count.most_common():
    if freq >= 2: # شرط بسيط للعبارات
        percentage = (freq / total_count) * 100
        analyzed_data.append({"العبارة": phrase, "التكرار": freq, "النوع": "عبارة مركبة", "النسبة": f"{percentage:.2f}%"})

# === 7. التصدير للإكسل (الجزء الجديد) ===
# تحويل القائمة لجدول بيانات
df = pd.read_json(pd.Series(analyzed_data).to_json(orient='values'))

# حفظ الملف
output_filename = "legal_report.xlsx"
df.to_excel(output_filename, index=False)

print(f"تم إنشاء التقرير بنجاح: {output_filename}")
print(f"إجمالي النتائج المستخرجة: {len(analyzed_data)}")
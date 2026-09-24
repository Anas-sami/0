import os
from transformers import pipeline

class NLPEngine:
    def __init__(self):
        """
        تحميل نموذج لغوي خفيف لتحليل النصوص ونبرة الملاحظات
        """
        try:
            # نموذج سريع وصغير الحجم (~250MB) لتصنيف النصوص ونبرة المخاطر
            self.classifier = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
        except Exception as e:
            print(f"[تحذير] تعذر تحميل النموذج اللغوي محلياً: {e}")
            self.classifier = None

    def analyze_severity(self, notes: str) -> str:
        """
        تحديد مستوى الخطورة بناءً على الكلمات المفتاحية وتحليل النص
        """
        high_risk_keywords = ["fire", "smoke", "accident", "broken", "danger", "urgent", "leak", "damage", "خطر", "حادث", "كسر", "عطل"]
        low_notes = notes.lower()

        # فحص الكلمات الحساسة
        if any(keyword in low_notes for keyword in high_risk_keywords):
            return "CRITICAL"

        # استخدام النموذج اللغوي لتقييم النبرة إذا كان متاحاً
        if self.classifier and notes.strip():
            try:
                result = self.classifier(notes[:512])[0]
                if result['label'] == 'NEGATIVE' and result['score'] > 0.85:
                    return "HIGH"
                elif result['label'] == 'NEGATIVE':
                    return "MEDIUM"
            except Exception:
                pass

        return "NORMAL"

    def generate_audit_report(self, title: str, notes: str, detected_objects: str, confidence: float) -> dict:
        """
        توليد تقرير تفتيش فني مهيكل ومؤتمت يدمج الرؤية الحاسوبية والنصوص
        """
        severity = self.analyze_severity(notes)

        # صياغة التقرير الإداري التنفيذي
        report_text = (
            f"=== تقرير التفتيش الذكي المؤتمت ===\n"
            f"عنوان العملية: {title}\n"
            f"مستوى الخطورة والحالة: [{severity}]\n"
            f"العناصر المكتشفة بصرياً: {detected_objects}\n"
            f"متوسط دقة الرؤية الحاسوبية: {int(confidence * 100)}%\n"
            f"ملاحظات المفتش الميداني: {notes if notes else 'لا توجد ملاحظات مدخلة'}\n"
            f"التوصية التشغيلية: "
        )

        if severity in ["CRITICAL", "HIGH"]:
            report_text += "يتطلب تدخلاً فورياً وإرسال فريق صيانة للموقع بسبب رصد مؤشرات خطورة مرتفعة."
        elif severity == "MEDIUM":
            report_text += "إدراج السجل في جدول المتابعة الدورية خلال 48 ساعة."
        else:
            report_text += "العملية طبيعية، لا توجد ملاحظات تستدعي الإجراءات الطارئة."

        return {
            "severity": severity,
            "detailed_report": report_text
        }
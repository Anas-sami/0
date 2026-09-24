import os
import cv2
from ultralytics import YOLO

class VisionEngine:
    def __init__(self, model_name: str = "yolov8n.pt", conf_threshold: float = 0.35):
        """
        تحميل نموذج خفيف مسبق التدريب وتحديد حد أدنى لنسبة الثقة
        """
        self.model = YOLO(model_name)
        self.conf_threshold = conf_threshold

    def analyze_image(self, image_path: str) -> dict:
        """
        معالجة الصورة، استخراج العناصر، ورسم مربعات التحديد
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        # تشغيل عملية الاستدلال (Inference)
        results = self.model(image_path, conf=self.conf_threshold)[0]

        detected_items = []
        total_conf = 0.0

        for box in results.boxes:
            cls_id = int(box.cls[0].item())
            label = self.model.names[cls_id]
            conf = round(float(box.conf[0].item()), 2)
            detected_items.append(f"{label} ({int(conf * 100)}%)")
            total_conf += conf

        # حساب متوسط نسبة الثقة وتجهيز الملخص
        total_objects = len(detected_items)
        avg_confidence = round(total_conf / total_objects, 2) if total_objects > 0 else 0.0
        summary_text = ", ".join(detected_items) if total_objects > 0 else "No specific objects detected"

        # رسم مربعات الكشف وحفظ الصورة الناتجة
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.basename(image_path)
        annotated_path = os.path.join(output_dir, f"analyzed_{filename}")
        cv2.imwrite(annotated_path, results.plot())

        return {
            "summary": summary_text,
            "confidence_score": avg_confidence,
            "annotated_path": annotated_path,
            "detected_count": total_objects
        }
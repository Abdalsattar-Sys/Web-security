import cv2
import os
from datetime import datetime

# إنشاء ملف CSV للحضور إذا لم يكن موجودًا
if not os.path.exists("attendance.csv"):
    with open("attendance.csv", 'w', encoding='utf-8') as f:
        f.write("Student Name,Date,Time\n")

# تهيئة مجلد تخزين الصور
if not os.path.exists("data"):
    os.makedirs("data")

# تسجيل آخر وقت تم تسجيل الحضور فيه
last_seen = {}

def capture_images(student_name):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    count = 0

    print(f"بدء التقاط صور للطالب: {student_name}. اضغط 'q' للخروج.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("لا يمكن الوصول إلى الكاميرا.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi = gray[y:y + h, x:x + w]
            file_path = f"data/{student_name}_{count}.jpg"
            cv2.imwrite(file_path, roi)
            count += 1
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("التقاط الصور", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 1:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"تم التقاط {count} صورة وحفظها في المجلد 'data/'.")

def recognize_faces():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    known_faces = {}
    for file_name in os.listdir("data"):
        if file_name.endswith(".jpg"):
            name = file_name.split("_")[0]
            img_path = os.path.join("data", file_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            known_faces[name] = img

    cap = cv2.VideoCapture(0)
    print("بدء التعرف على الحضور. اضغط 'q' للخروج.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("لا يمكن الوصول إلى الكاميرا.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi = gray[y:y + h, x:x + w]
            name = "غير معروف"
            for student_name, saved_face in known_faces.items():
                res = cv2.matchTemplate(roi, saved_face, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                if max_val > 0.3:  # تعديل قيمة التشابه حسب الحاجة
                    name = student_name
                    break

            if name != "غير معروف":
                now = datetime.now()
                # التحقق من مرور دقيقة واحدة على الأقل قبل تسجيل الحضور مجددًا
                if name not in last_seen or (now - last_seen[name]).seconds > 60:
                    last_seen[name] = now
                    with open('attendance.csv', 'a', encoding='utf-8') as f:
                        date_string = now.strftime('%Y-%m-%d')
                        time_string = now.strftime('%H:%M:%S')
                        f.write(f'{name},{date_string},{time_string}\n')
                        print(f"تم تسجيل الحضور للطالب: {name}.")
            #screen size
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
         #tital
        cv2.imshow("نظام الحضور", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

while True:
    print("\nنظام تسجيل الحضور باستخدام التعرف على الوجه")
    print("1. إضافة طالب جديد")
    print("2. بدء تسجيل الحضور")
    print("3. الخروج")

    choice = input("اختر العملية (1-3): ")

    if choice == '1':
        student_name = input("أدخل اسم الطالب: ")
        capture_images(student_name)

    elif choice == '2':
        recognize_faces()

    elif choice == '3':
        print("شكراً لاستخدام النظام!")
        break

    else:
        print("اختيار غير صالح. الرجاء المحاولة مرة أخرى.")

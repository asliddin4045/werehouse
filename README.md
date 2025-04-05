# Werehouse API

Werehouse API – ishlab chiqarish korxonasida mahsulotlar tayyorlash uchun kerak bo‘lgan xomashyolarni omborga kiritilgan partiyalar asosida hisoblab, taqsimlashni avtomatlashtiruvchi tizim. Django REST Framework asosida yozilgan ushbu loyiha foydalanuvchi tomonidan kiritilgan mahsulot kodi va miqdor asosida, har bir mahsulot uchun kerakli xomashyo miqdorini ombordagi mavjud partiyalar bo‘yicha aniqlaydi.

## Texnologiyalar

- **Python 3.10+**
- **Django 4.x / Django REST Framework**
- **SQLite3** (yoki boshqa bazalar)
- **Swagger** – API hujjatlari uchun
- **Management Commands** – ma’lumotlar bazasini to‘ldirish

## Loyihaning Xususiyatlari

- **Mahsulotlar** va **xomashyolar**:  
  - *Product*: mahsulot nomi va product_code  
  - *Material*: xomashyo nomi  
  - *ProductMaterial*: mahsulot tayyorlash uchun kerak bo‘lgan xomashyo miqdori  
  - *Warehouse*: ombordagi xomashyolar partiyalari (remainder va price)

- **Xomashyo taqsimoti hisoblash:**  
  - Bir xil product_code ostida kiritilgan mahsulotlar uchun (masalan, Ko'ylak va Shim) kiritilgan buyurtma miqdori asosida multiplier qo‘llanadi.  
    - Masalan, agar buyurtma { "product_code": 238923, "quantity": 10 } bo‘lsa:
      - **Ko'ylak**: multiplier = 3, ishlab chiqarish miqdori 10 × 3 = 30 dona  
      - **Shim**: multiplier = 2, ishlab chiqarish miqdori 10 × 2 = 20 dona
  - Ombordagi xomashyolar partiyalari hisobga olinib, agar bir partiya avvalgi mahsulot tomonidan band qilingan bo‘lsa, keyingi mahsulot uchun u hisobga olinmaydi. Agar yetarli miqdor bo‘lmasa, natijada shu material uchun `"warehouse_id": null` va `"price": null"` qaytariladi.

- **Swagger hujjatlari:**  
  API interfeysini hujjatlashtirish uchun [Swagger](http://127.0.0.1:8000/swagger/) dan foydalaniladi.

## O‘rnatish

1. Repository-ni klon qiling:
   ```bash
   git clone https://github.com/asliddin4045/werehouse.git
   cd werehouse
   
2.Virtual muhit yarating va uni faollashtiring:
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

3.Talab qilinadigan paketlarni o‘rnating:
pip install -r requirements.txt

4.Migratsiyalarni bajaring:
python manage.py makemigrations
python manage.py migrate

5.Superuser yarating (agar admin panelga kirish kerak bo‘lsa):
python manage.py createsuperuser

6.Serverni ishga tushuring:
python manage.py runserver

Ma'lumotlar Bazasi To‘ldirish
Loyiha ma’lumotlar bazasini to‘ldirish uchun custom management command (populate_db) yozilgan. Buni quyidagicha ishga tushiring:
python manage.py populate_db

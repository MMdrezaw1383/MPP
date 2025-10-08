#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tello Drone Controller
=====================

کنترل کننده پهپاد تلو با استفاده از کیبورد
نیازمندی‌ها:
- djitellopy
- pygame

نحوه استفاده:

کلیدهای کنترل:
- T: برخاستن (Takeoff)
- L: فرود آمدن (Landing)
- W/S: حرکت جلو/عقب
- A/D: حرکت چپ/راست
- ↑/↓: حرکت بالا/پایین
- ←/→: چرخش چپ/راست
- ESC: توقف اضطراری

تاریخ: 2025
"""

from bidi.algorithm import get_display
import arabic_reshaper
import pygame
import time
import os
import sys

def to_rtl(text):
    '''تبدیل متن های فارسی به rtl'''
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    print(bidi_text)

def render_persian_text(font, text, color):
    """
    تبدیل متن فارسی به شکل صحیح و RTL و رندر آن با pygame.
    """
    # شکل‌دهی حروف فارسی
    reshaped = arabic_reshaper.reshape(text)
    # ترتیب صحیح حروف برای RTL
    bidi_text = get_display(reshaped)
    # بازگرداندن Surface برای blit
    return font.render(bidi_text, True, color)



# کتابخانه‌های مورد نیاز برای پهپاد تلو
try:
    from djitellopy import Tello
    TELLO_AVAILABLE = True
    to_rtl("✅ کتابخانه djitellopy پیدا شد - اتصال به پهپاد واقعی")
except ImportError:
    TELLO_AVAILABLE = False
    to_rtl("❌ کتابخانه djitellopy پیدا نشد!")
    to_rtl("برای نصب از دستور زیر استفاده کنید:")
    to_rtl("pip install djitellopy")
    sys.exit(1)

# تنظیمات کنترل
SPEED = 60          # سرعت حرکت پهپاد (0-100)
FPS = 30            # فریم در ثانیه برای نمایش
CONNECTION_TIMEOUT = 10  # مهلت زمانی اتصال به ثانیه




class TelloController:
    """
    کلاس کنترل کننده پهپاد تلو
    
    این کلاس اتصال به پهپاد، نمایش وضعیت و کنترل با کیبورد را مدیریت می‌کند.
    """

    def __init__(self):
        """مقداردهی اولیه کنترل کننده"""
        
        # مقداردهی pygame
        self.init_pygame()
        
        # مقداردهی پهپاد
        self.init_tello()
        
        # متغیرهای سرعت حرکت
        self.for_back_velocity = 0      # جلو/عقب
        self.left_right_velocity = 0    # چپ/راست
        self.up_down_velocity = 0       # بالا/پایین
        self.yaw_velocity = 0           # چرخش

        # وضعیت پرواز
        self.is_flying = False
        self.send_rc = True
        self.battery_level = 0
        self.connected = False
        
        # کلیدهای فشرده شده (برای نمایش)
        self.pressed_keys = set()
        
        # اتصال به پهپاد
        self.connect_to_drone()

    def init_pygame(self):
        """مقداردهی pygame و پنجره نمایش"""
        
        # تنظیمات ویژه برای macOS
        if sys.platform == "darwin":
            os.environ['SDL_VIDEODRIVER'] = 'cocoa'
        
        # مقداردهی pygame
        pygame.init()
        pygame.mixer.quit()  # غیرفعال کردن صدا
        
        # تنظیم پنجره نمایش
        width, height = 900, 700
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption("کنترل کننده پهپاد تلو - Tello Drone Controller")
        
        # رنگ پس‌زمینه
        self.screen.fill((20, 25, 40))
        pygame.display.flip()
        
        # فونت‌ها برای نمایش متن
        self.font_title = pygame.font.Font("Vazirmatn.ttf", 42)
        self.font_large = pygame.font.Font("Vazirmatn.ttf", 32)
        self.font_medium = pygame.font.Font("Vazirmatn.ttf", 24)
        self.font_small = pygame.font.Font("Vazirmatn.ttf", 18)

    def init_tello(self):
        """مقداردهی پهپاد تلو"""
        
        if not TELLO_AVAILABLE:
            to_rtl("❌ کتابخانه djitellopy در دسترس نیست!")
            sys.exit(1)
            
        self.tello = Tello()

    def connect_to_drone(self):
        """اتصال به پهپاد تلو"""
        
        to_rtl("🔄 در حال اتصال به پهپاد تلو...")
        to_rtl("   لطفاً مطمئن شوید که:")
        to_rtl("   1. پهپاد روشن است")
        to_rtl("   2. کامپیوتر به WiFi پهپاد متصل است")
        to_rtl("   3. نام شبکه معمولاً TELLO-XXXXXX است")
        
        try:
            # اتصال به پهپاد
            self.tello.connect()
            
            # دریافت اطلاعات باتری
            self.battery_level = self.tello.get_battery()
            self.connected = True
            
            # غیرفعال کردن استریم ویدیو (در صورت روشن بودن)
            self.tello.streamoff()
            
            to_rtl("✅ اتصال برقرار شد!")
            to_rtl(f"🔋 سطح باتری: {self.battery_level}%")
            
            # بررسی سطح باتری
            if self.battery_level < 20:
                to_rtl("⚠️ هشدار: سطح باتری کم است!")
                to_rtl("   توصیه می‌شود پهپاد را شارژ کنید")
            elif self.battery_level < 50:
                to_rtl("⚠️ توجه: سطح باتری متوسط است")
                
        except Exception as e:
            to_rtl(f"❌ خطا در اتصال: {e}")
            to_rtl("\n🔧 راهکارهای احتمالی:")
            to_rtl("   1. مطمئن شوید پهپاد روشن است")
            to_rtl("   2. به WiFi پهپاد متصل شوید")
            to_rtl("   3. پهپاد را نزدیک‌تر آورید")
            to_rtl("   4. پهپاد را خاموش و روشن کنید")
            self.connected = False
            
            # در صورت عدم اتصال، خروج از برنامه
            to_rtl("\nادامه می‌دهید؟ (y/N): ")
            response = input()
            if response.lower() != 'y':
                sys.exit(1)

    def draw_ui(self):
        """نمایش رابط کاربری با وضعیت فعلی"""
        
        # پاک کردن صفحه
        self.screen.fill((20, 25, 40))
        
        # عنوان اصلی
        title_text = "کنترل کننده پهپاد تلو"
        title_surface = render_persian_text(self.font_title, title_text, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(450, 50))
        self.screen.blit(title_surface, title_rect)
        
        subtitle_text = "Tello Drone Controller"
        subtitle_surface = render_persian_text(self.font_medium, subtitle_text, (200, 200, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(450, 85))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # وضعیت اتصال
        status_color = (50, 255, 50) if self.connected else (255, 100, 100)
        status_text = "🟢 متصل" if self.connected else "🔴 قطع شده"
        status_surface = render_persian_text(self.font_large, status_text, status_color)
        status_rect = status_surface.get_rect(center=(450, 130))
        self.screen.blit(status_surface, status_rect)
        
        # وضعیت پرواز
        flight_color = (255, 255, 50) if self.is_flying else (150, 150, 150)
        flight_text = "🚁 در حال پرواز" if self.is_flying else "🛬 روی زمین"
        flight_surface = render_persian_text(self.font_large, flight_text, flight_color)
        flight_rect = flight_surface.get_rect(center=(450, 170))
        self.screen.blit(flight_surface, flight_rect)
        
        # سطح باتری
        if self.battery_level < 20:
            battery_color = (255, 50, 50)
            battery_icon = "🔴"
        elif self.battery_level < 50:
            battery_color = (255, 255, 50)
            battery_icon = "🟡"
        else:
            battery_color = (50, 255, 50)
            battery_icon = "🟢"
            
        battery_text = f"{battery_icon} باتری: {self.battery_level}%"
        battery_surface = render_persian_text(self.font_large, battery_text, battery_color)

        battery_rect = battery_surface.get_rect(center=(450, 210))
        self.screen.blit(battery_surface, battery_rect)
        
        # سرعت‌های فعلی
        vel_start_y = 270
        vel_texts = [
            ("جلو/عقب:", self.for_back_velocity),
            ("چپ/راست:", self.left_right_velocity), 
            ("بالا/پایین:", self.up_down_velocity),
            ("چرخش:", self.yaw_velocity)
        ]
        
        for i, (label, value) in enumerate(vel_texts):
            color = (100, 255, 255) if abs(value) > 0 else (150, 150, 150)
            text = f"{label} {value:4d}"

            vel_surface = render_persian_text(self.font_small,text, color)
            self.screen.blit(vel_surface, (300, vel_start_y + i * 30))
        
        # دستورالعمل‌ها
        instructions_fa = [
            "دستورالعمل کنترل:",
            "T - برخاستن (Takeoff)",
            "L - فرود آمدن (Landing)", 
            "W/S - جلو/عقب",
            "A/D - چپ/راست",
            "↑/↓ - بالا/پایین",
            "←/→ - چرخش چپ/راست",
            "ESC - توقف اضطراری"
        ]
        
        instructions_en = [
            "CONTROLS:",
            "T - Takeoff",
            "L - Land",
            "W/S - Forward/Back", 
            "A/D - Left/Right",
            "↑/↓ - Up/Down",
            "←/→ - Rotate Left/Right", 
            "ESC - Emergency Stop"
        ]
        
        # نمایش دستورالعمل‌ها (فارسی و انگلیسی)
        start_y = 420
        for i, (fa_text, en_text) in enumerate(zip(instructions_fa, instructions_en)):
            if i == 0:  # عنوان
                color = (255, 255, 255)
                font = self.font_medium
            else:
                color = (200, 200, 200)
                font = self.font_small
                
            # متن فارسی
            fa_surface = render_persian_text(font,fa_text, color)
            self.screen.blit(fa_surface, (50, start_y + i * 28))
            
            # متن انگلیسی
            en_surface = font.render(en_text, True, color)
            self.screen.blit(en_surface, (350, start_y + i * 28))
        
        # کلیدهای فشرده شده
        if self.pressed_keys:
            pressed_text = f"کلیدهای فعال: {sorted(self.pressed_keys)}"
            pressed_surface = render_persian_text(self.font_small,pressed_text, (255, 255, 100))
            self.screen.blit(pressed_surface, (50, 650))
        
        # هشدارهای ایمنی
        warnings_y = 680
        if not self.connected:
            warning_text = "⚠️ اتصال برقرار نیست - کنترل غیرفعال"
            warning_surface = render_persian_text(self.font_small, warning_text, (255, 100, 100))
            self.screen.blit(warning_surface, (50, warnings_y))
        elif self.battery_level < 20:
            warning_text = "⚠️ باتری کم - هرچه زودتر فرود آمدن توصیه می‌شود"
            warning_surface = render_persian_text(self.font_small, warning_text, (255, 100, 100))
            self.screen.blit(warning_surface, (50, warnings_y))

    def handle_key_down(self, key):
        """مدیریت فشردن کلیدها"""
        
        # افزودن نام کلید به لیست کلیدهای فشرده شده
        key_name = pygame.key.name(key).upper()
        self.pressed_keys.add(key_name)
        
        # برخاستن
        if key == pygame.K_t and not self.is_flying and self.connected:
            if self.battery_level < 10:
                to_rtl("❌ باتری خیلی کم است! نمی‌توان پرواز کرد")
                return
                
            to_rtl("🚁 در حال برخاستن...")
            try:
                self.tello.takeoff()
                self.is_flying = True
                to_rtl("✅ برخاستن موفق")
            except Exception as e:
                to_rtl(f"❌ خطا در برخاستن: {e}")
                
        # فرود آمدن
        elif key == pygame.K_l and self.is_flying:
            to_rtl("🛬 در حال فرود...")
            try:
                self.tello.land()
                self.is_flying = False
                to_rtl("✅ فرود موفق")
            except Exception as e:
                to_rtl(f"❌ خطا در فرود: {e}")

        # کنترل‌های حرکت - فقط در صورت پرواز
        elif self.is_flying and self.connected:
            if key == pygame.K_w:
                self.for_back_velocity = SPEED
                to_rtl("➡️ حرکت جلو")
            elif key == pygame.K_s:
                self.for_back_velocity = -SPEED
                to_rtl("⬅️ حرکت عقب")
            elif key == pygame.K_a:
                self.left_right_velocity = -SPEED
                to_rtl("⬅️ حرکت چپ")
            elif key == pygame.K_d:
                self.left_right_velocity = SPEED
                to_rtl("➡️ حرکت راست")
            elif key == pygame.K_UP:
                self.up_down_velocity = SPEED
                to_rtl("⬆️ حرکت بالا")
            elif key == pygame.K_DOWN:
                self.up_down_velocity = -SPEED
                to_rtl("⬇️ حرکت پایین")
            elif key == pygame.K_LEFT:
                self.yaw_velocity = -SPEED
                to_rtl("↩️ چرخش چپ")
            elif key == pygame.K_RIGHT:
                self.yaw_velocity = SPEED
                to_rtl("↪️ چرخش راست")
        
        # توقف اضطراری
        elif key == pygame.K_ESCAPE:
            to_rtl("🚨 توقف اضطراری فعال شد!")
            if self.is_flying and self.connected:
                try:
                    self.tello.emergency()
                    self.is_flying = False
                    to_rtl("✅ دستور اضطراری ارسال شد")
                except Exception as e:
                    to_rtl(f"❌ خطا در دستور اضطراری: {e}")
            self.send_rc = False

    def handle_key_up(self, key):
        """مدیریت رها کردن کلیدها"""
        
        # حذف نام کلید از لیست کلیدهای فشرده شده
        key_name = pygame.key.name(key).upper()
        self.pressed_keys.discard(key_name)
        
        # توقف حرکات
        if key in (pygame.K_w, pygame.K_s):
            self.for_back_velocity = 0
        elif key in (pygame.K_a, pygame.K_d):
            self.left_right_velocity = 0
        elif key in (pygame.K_UP, pygame.K_DOWN):
            self.up_down_velocity = 0
        elif key in (pygame.K_LEFT, pygame.K_RIGHT):
            self.yaw_velocity = 0

    def update_battery(self):
        """به‌روزرسانی سطح باتری"""
        
        if self.connected:
            try:
                self.battery_level = self.tello.get_battery()
            except Exception as e:
                to_rtl(f"خطا در خواندن باتری: {e}")

    def run(self):
        """حلقه اصلی برنامه"""
        
        clock = pygame.time.Clock()
        battery_update_counter = 0
        
        to_rtl("✅ کنترل کننده فعال شد")
        to_rtl("📺 پنجره نمایش باید قابل مشاهده باشد")
        
        if not self.connected:
            to_rtl("⚠️ اتصال برقرار نیست - فقط نمایش فعال است")
        else:
            to_rtl("🎮 آماده کنترل!")
        
        while self.send_rc:
            # مدیریت رویدادهای pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send_rc = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.handle_key_up(event.key)
            
            # ارسال دستورات کنترل از راه دور
            if self.is_flying and self.connected:
                try:
                    self.tello.send_rc_control(
                        self.left_right_velocity,
                        self.for_back_velocity, 
                        self.up_down_velocity,
                        self.yaw_velocity
                    )
                except Exception as e:
                    to_rtl(f"خطا در ارسال دستور: {e}")
                    self.connected = False
            
            # به‌روزرسانی باتری (هر 3 ثانیه)
            battery_update_counter += 1
            if battery_update_counter >= (FPS * 3):  # هر 3 ثانیه
                self.update_battery()
                battery_update_counter = 0
            
            # به‌روزرسانی نمایش
            self.draw_ui()
            pygame.display.flip()
            
            # محدود کردن FPS
            clock.tick(FPS)
        
        # پاکسازی قبل از خروج
        self.cleanup()

    def cleanup(self):
        """پاکسازی منابع قبل از خروج"""
        
        to_rtl("🧹 در حال پاکسازی...")
        
        # اگر پهپاد در حال پرواز است، فرود آمدن
        if self.is_flying and self.connected:
            to_rtl("🛬 فرود نهایی...")
            try:
                self.tello.land()
                time.sleep(2)  # صبر برای تکمیل فرود
                to_rtl("✅ فرود نهایی انجام شد")
            except Exception as e:
                to_rtl(f"❌ خطا در فرود نهایی: {e}")
        
        # بستن pygame
        pygame.quit()
        to_rtl("✅ کنترل کننده بسته شد")

def check_requirements():
    """بررسی نیازمندی‌ها"""
    
    to_rtl("🔍 بررسی نیازمندی‌ها...")
    
    # بررسی pygame
    try:
        import pygame
        to_rtl("✅ pygame موجود است")
    except ImportError:
        to_rtl("❌ pygame نصب نیست!")
        to_rtl("برای نصب: pip install pygame")
        return False
    
    # بررسی djitellopy
    if not TELLO_AVAILABLE:
        to_rtl("❌ djitellopy نصب نیست!")
        to_rtl("برای نصب: pip install djitellopy")
        return False
    else:
        to_rtl("✅ djitellopy موجود است")
    
    return True

def main():
    """تابع اصلی برنامه"""
    
    to_rtl("🚁 کنترل کننده پهپاد تلو")
    to_rtl("=" * 40)
    
    # بررسی نیازمندی‌ها
    if not check_requirements():
        to_rtl("\n❌ نیازمندی‌ها برآورده نیست!")
        to_rtl("لطفاً کتابخانه‌های مورد نیاز را نصب کنید و دوباره تلاش کنید")
        return
    
    try:
        # ایجاد و اجرای کنترل کننده
        controller = TelloController()
        controller.run()
        
    except KeyboardInterrupt:
        to_rtl("\n🛑 برنامه توسط کاربر متوقف شد")
        
    except Exception as e:
        to_rtl(f"\n❌ خطای غیرمنتظره: {e}")
        
        # تلاش برای پاکسازی اضطراری
        try:
            if 'controller' in locals() and hasattr(controller, 'tello'):
                if controller.is_flying and controller.connected:
                    to_rtl("🚨 تلاش برای فرود اضطراری...")
                    controller.tello.land()
        except:
            pass
    
    to_rtl("👋 خروج از برنامه")

if __name__ == "__main__":
    main()
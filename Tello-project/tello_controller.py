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
    python tello_controller.py

کلیدهای کنترل:
- T: برخاستن (Takeoff)
- L: فرود آمدن (Landing)
- W/S: حرکت جلو/عقب
- A/D: حرکت چپ/راست
- ↑/↓: حرکت بالا/پایین
- ←/→: چرخش چپ/راست
- ESC: توقف اضطراری

تاریخ:2025
"""

import pygame
import time
import os
import sys

# کتابخانه‌های مورد نیاز برای پهپاد تلو
try:
    from djitellopy import Tello
    TELLO_AVAILABLE = True
    print("✅ کتابخانه djitellopy پیدا شد - اتصال به پهپاد واقعی")
except ImportError:
    TELLO_AVAILABLE = False
    print("❌ کتابخانه djitellopy پیدا نشد!")
    print("برای نصب از دستور زیر استفاده کنید:")
    print("pip install djitellopy")
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
        self.font_title = pygame.font.Font(None, 42)
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

    def init_tello(self):
        """مقداردهی پهپاد تلو"""
        
        if not TELLO_AVAILABLE:
            print("❌ کتابخانه djitellopy در دسترس نیست!")
            sys.exit(1)
            
        self.tello = Tello()

    def connect_to_drone(self):
        """اتصال به پهپاد تلو"""
        
        print("🔄 در حال اتصال به پهپاد تلو...")
        print("   لطفاً مطمئن شوید که:")
        print("   1. پهپاد روشن است")
        print("   2. کامپیوتر به WiFi پهپاد متصل است")
        print("   3. نام شبکه معمولاً TELLO-XXXXXX است")
        
        try:
            # اتصال به پهپاد
            self.tello.connect()
            
            # دریافت اطلاعات باتری
            self.battery_level = self.tello.get_battery()
            self.connected = True
            
            # غیرفعال کردن استریم ویدیو (در صورت روشن بودن)
            self.tello.streamoff()
            
            print("✅ اتصال برقرار شد!")
            print(f"🔋 سطح باتری: {self.battery_level}%")
            
            # بررسی سطح باتری
            if self.battery_level < 20:
                print("⚠️ هشدار: سطح باتری کم است!")
                print("   توصیه می‌شود پهپاد را شارژ کنید")
            elif self.battery_level < 50:
                print("⚠️ توجه: سطح باتری متوسط است")
                
        except Exception as e:
            print(f"❌ خطا در اتصال: {e}")
            print("\n🔧 راهکارهای احتمالی:")
            print("   1. مطمئن شوید پهپاد روشن است")
            print("   2. به WiFi پهپاد متصل شوید")
            print("   3. پهپاد را نزدیک‌تر آورید")
            print("   4. پهپاد را خاموش و روشن کنید")
            self.connected = False
            
            # در صورت عدم اتصال، خروج از برنامه
            response = input("\nادامه می‌دهید؟ (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)

    def draw_ui(self):
        """نمایش رابط کاربری با وضعیت فعلی"""
        
        # پاک کردن صفحه
        self.screen.fill((20, 25, 40))
        
        # عنوان اصلی
        title_text = "کنترل کننده پهپاد تلو"
        title_surface = self.font_title.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(450, 50))
        self.screen.blit(title_surface, title_rect)
        
        subtitle_text = "Tello Drone Controller"
        subtitle_surface = self.font_medium.render(subtitle_text, True, (200, 200, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(450, 85))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # وضعیت اتصال
        status_color = (50, 255, 50) if self.connected else (255, 100, 100)
        status_text = "🟢 متصل" if self.connected else "🔴 قطع شده"
        status_surface = self.font_large.render(status_text, True, status_color)
        status_rect = status_surface.get_rect(center=(450, 130))
        self.screen.blit(status_surface, status_rect)
        
        # وضعیت پرواز
        flight_color = (255, 255, 50) if self.is_flying else (150, 150, 150)
        flight_text = "🚁 در حال پرواز" if self.is_flying else "🛬 روی زمین"
        flight_surface = self.font_large.render(flight_text, True, flight_color)
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
        battery_surface = self.font_large.render(battery_text, True, battery_color)
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
            vel_surface = self.font_medium.render(text, True, color)
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
            fa_surface = font.render(fa_text, True, color)
            self.screen.blit(fa_surface, (50, start_y + i * 28))
            
            # متن انگلیسی
            en_surface = font.render(en_text, True, color)
            self.screen.blit(en_surface, (350, start_y + i * 28))
        
        # کلیدهای فشرده شده
        if self.pressed_keys:
            pressed_text = f"کلیدهای فعال: {', '.join(sorted(self.pressed_keys))}"
            pressed_surface = self.font_small.render(pressed_text, True, (255, 255, 100))
            self.screen.blit(pressed_surface, (50, 650))
        
        # هشدارهای ایمنی
        warnings_y = 680
        if not self.connected:
            warning_text = "⚠️ اتصال برقرار نیست - کنترل غیرفعال"
            warning_surface = self.font_small.render(warning_text, True, (255, 100, 100))
            self.screen.blit(warning_surface, (50, warnings_y))
        elif self.battery_level < 20:
            warning_text = "⚠️ باتری کم - هرچه زودتر فرود آمدن توصیه می‌شود"
            warning_surface = self.font_small.render(warning_text, True, (255, 100, 100))
            self.screen.blit(warning_surface, (50, warnings_y))

    def handle_key_down(self, key):
        """مدیریت فشردن کلیدها"""
        
        # افزودن نام کلید به لیست کلیدهای فشرده شده
        key_name = pygame.key.name(key).upper()
        self.pressed_keys.add(key_name)
        
        # برخاستن
        if key == pygame.K_t and not self.is_flying and self.connected:
            if self.battery_level < 10:
                print("❌ باتری خیلی کم است! نمی‌توان پرواز کرد")
                return
                
            print("🚁 در حال برخاستن...")
            try:
                self.tello.takeoff()
                self.is_flying = True
                print("✅ برخاستن موفق")
            except Exception as e:
                print(f"❌ خطا در برخاستن: {e}")
                
        # فرود آمدن
        elif key == pygame.K_l and self.is_flying:
            print("🛬 در حال فرود...")
            try:
                self.tello.land()
                self.is_flying = False
                print("✅ فرود موفق")
            except Exception as e:
                print(f"❌ خطا در فرود: {e}")

        # کنترل‌های حرکت - فقط در صورت پرواز
        elif self.is_flying and self.connected:
            if key == pygame.K_w:
                self.for_back_velocity = SPEED
                print("➡️ حرکت جلو")
            elif key == pygame.K_s:
                self.for_back_velocity = -SPEED
                print("⬅️ حرکت عقب")
            elif key == pygame.K_a:
                self.left_right_velocity = -SPEED
                print("⬅️ حرکت چپ")
            elif key == pygame.K_d:
                self.left_right_velocity = SPEED
                print("➡️ حرکت راست")
            elif key == pygame.K_UP:
                self.up_down_velocity = SPEED
                print("⬆️ حرکت بالا")
            elif key == pygame.K_DOWN:
                self.up_down_velocity = -SPEED
                print("⬇️ حرکت پایین")
            elif key == pygame.K_LEFT:
                self.yaw_velocity = -SPEED
                print("↩️ چرخش چپ")
            elif key == pygame.K_RIGHT:
                self.yaw_velocity = SPEED
                print("↪️ چرخش راست")
        
        # توقف اضطراری
        elif key == pygame.K_ESCAPE:
            print("🚨 توقف اضطراری فعال شد!")
            if self.is_flying and self.connected:
                try:
                    self.tello.emergency()
                    self.is_flying = False
                    print("✅ دستور اضطراری ارسال شد")
                except Exception as e:
                    print(f"❌ خطا در دستور اضطراری: {e}")
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
                print(f"خطا در خواندن باتری: {e}")

    def run(self):
        """حلقه اصلی برنامه"""
        
        clock = pygame.time.Clock()
        battery_update_counter = 0
        
        print("✅ کنترل کننده فعال شد")
        print("📺 پنجره نمایش باید قابل مشاهده باشد")
        
        if not self.connected:
            print("⚠️ اتصال برقرار نیست - فقط نمایش فعال است")
        else:
            print("🎮 آماده کنترل!")
        
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
                    print(f"خطا در ارسال دستور: {e}")
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
        
        print("🧹 در حال پاکسازی...")
        
        # اگر پهپاد در حال پرواز است، فرود آمدن
        if self.is_flying and self.connected:
            print("🛬 فرود نهایی...")
            try:
                self.tello.land()
                time.sleep(2)  # صبر برای تکمیل فرود
                print("✅ فرود نهایی انجام شد")
            except Exception as e:
                print(f"❌ خطا در فرود نهایی: {e}")
        
        # بستن pygame
        pygame.quit()
        print("✅ کنترل کننده بسته شد")

def check_requirements():
    """بررسی نیازمندی‌ها"""
    
    print("🔍 بررسی نیازمندی‌ها...")
    
    # بررسی pygame
    try:
        import pygame
        print("✅ pygame موجود است")
    except ImportError:
        print("❌ pygame نصب نیست!")
        print("برای نصب: pip install pygame")
        return False
    
    # بررسی djitellopy
    if not TELLO_AVAILABLE:
        print("❌ djitellopy نصب نیست!")
        print("برای نصب: pip install djitellopy")
        return False
    else:
        print("✅ djitellopy موجود است")
    
    return True

def main():
    """تابع اصلی برنامه"""
    
    print("🚁 کنترل کننده پهپاد تلو")
    print("=" * 40)
    
    # بررسی نیازمندی‌ها
    if not check_requirements():
        print("\n❌ نیازمندی‌ها برآورده نیست!")
        print("لطفاً کتابخانه‌های مورد نیاز را نصب کنید و دوباره تلاش کنید")
        return
    
    try:
        # ایجاد و اجرای کنترل کننده
        controller = TelloController()
        controller.run()
        
    except KeyboardInterrupt:
        print("\n🛑 برنامه توسط کاربر متوقف شد")
        
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {e}")
        
        # تلاش برای پاکسازی اضطراری
        try:
            if 'controller' in locals() and hasattr(controller, 'tello'):
                if controller.is_flying and controller.connected:
                    print("🚨 تلاش برای فرود اضطراری...")
                    controller.tello.land()
        except:
            pass
    
    print("👋 خروج از برنامه")

if __name__ == "__main__":
    main()

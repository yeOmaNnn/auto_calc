import os
import time
import pyautogui
from PIL import Image


class CalculatorAutomation:
    def __init__(self, os_type="windows", button_images_dir="buttons"):
        self.os_type = os_type.lower()
        self.button_images_dir = button_images_dir

    def open_calculator(self):
        if self.os_type == "windows":
            os.system("start calc")
        elif self.os_type == "macos":
            os.system("open -a Calculator")
        elif self.os_type == "linux":
            os.system("gnome-calculator")
        else:
            raise ValueError("Unsupported OS type. Use 'windows', 'macos', or 'linux'.")
        time.sleep(2)

    def close_calculator(self):
        if self.os_type == "windows":
            os.system("taskkill /IM Calculator.exe /F")
        else:
            pyautogui.hotkey("alt", "f4")

    def validate_image_dimensions(self, button_image_path):
        screen_width, screen_height = pyautogui.size()
        with Image.open(button_image_path) as img:
            img_width, img_height = img.size
            if img_width > screen_width or img_height > screen_height:
                raise ValueError(
                    f"Размеры кнопки ({img_width}x{img_height}) превышают размеры экрана ({screen_width}x{screen_height})."
                )

    def find_and_click(self, button, confidence=0.9):
        button_image_path = f"{self.button_images_dir}/{button}.png"
        self.validate_image_dimensions(button_image_path)
        location = pyautogui.locateOnScreen(button_image_path, confidence=confidence)
        if location:
            pyautogui.click(pyautogui.center(location))
        else:
            raise FileNotFoundError(f"Кнопка '{button}' не найдена на экране.")

    def press_sequence(self, sequence):
        for button in sequence:
            self.find_and_click(button)

    def calculate(self, first_number, operation, second_number):
        sequence = list(str(first_number)) + [operation] + list(str(second_number)) + ["="]
        self.press_sequence(sequence)


if __name__ == "__main__":
    calculator = CalculatorAutomation(os_type="windows", button_images_dir="buttons")

    try:

        calculator.open_calculator()


        examples = [
            (12, "+", 7),
            (45, "-", 23),
            (6, "multiply", 9),
            (81, "divide", 9),
        ]

        for example in examples:
            first_number, operation, second_number = example
            print(f"Выполняем: {first_number} {operation} {second_number}")
            calculator.calculate(first_number, operation, second_number)
            time.sleep(2)

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except ValueError as e:
        print(f"Ошибка проверки размеров: {e}")
    finally:
        calculator.close_calculator()
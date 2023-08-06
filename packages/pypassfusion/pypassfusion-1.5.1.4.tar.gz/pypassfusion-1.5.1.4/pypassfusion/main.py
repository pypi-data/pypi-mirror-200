import random
import os
import tkinter as tk
from tkinter import filedialog
from .menu import main_menu
from .menu import sub_menu


def get_password_chars():
    chars = ''
    while True:
        user_choice = input("Do you want lowercase characters (lower), uppercase characters (upper), or both (both)? ")
        if user_choice.lower() == 'lower':
            chars += 'abcdefghijklmnopqrstuvwxyz'
            break
        elif user_choice.lower() == 'upper':
            chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            break
        elif user_choice.lower() == 'both':
            chars += 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            break
        else:
            print("Invalid choice, please enter 'lower', 'upper', or 'both'")
    return chars


def get_password_nums():
    user_choice = input("Do you want numbers in your password (yes/no)? ")
    if user_choice.lower() == 'yes':
        return '123456789'
    else:
        return ''


def get_password_symbols():
    user_choice = input("Do you want symbols in your password (yes/no)? ")
    if user_choice.lower() == 'yes':
        return '@#$%&'
    else:
        return ''


def generate_password(length, chars, nums, symbols):
    password = ''
    total_chars = 0

    if not nums and not symbols:
        char_nums = [int(length * 1)  # char occurrence #
                     ]
        total_chars = sum(char_nums)

        if len(password) != total_chars:
            for i in range(length):
                if char_nums[0] > 0:
                    password += random.choice(chars)
                    char_nums[0] -= 1

    elif not nums:
        char_nums = [int(length * 0.5)  # char occurrence #
                     , int(length * 0.5)  # symbol occurrence #
                     ]
        total_chars = sum(char_nums)
        if total_chars < length:
            char_nums[0] += length - total_chars

        password_list = []
        for i in range(char_nums[0]):
            password_list.append(random.choice(chars))
        for j in range(char_nums[1]):
            password_list.append(random.choice(symbols))
        random.shuffle(password_list)
        password = ''.join(password_list)

    elif not symbols:
        char_nums = [int(length * 0.5)  # char occurrence #
                     , int(length * 0.5)  # num occurrence #
                     ]
        total_chars = sum(char_nums)
        if total_chars < length:
            char_nums[0] += length - total_chars

        password_list = []
        for i in range(char_nums[0]):
            password_list.append(random.choice(chars))
        for j in range(char_nums[1]):
            password_list.append(random.choice(nums))
        random.shuffle(password_list)
        password = ''.join(password_list)


    else:
        char_nums = [int(length * 0.4)  # char occurrence #
                     , int(length * 0.3)  # num occurrence #
                     , int(length * 0.3)  # symbol occurrence #
                     ]
        total_chars = sum(char_nums)
        if total_chars < length:
            char_nums[0] += length - total_chars

        password_list = []
        for i in range(char_nums[0]):
            password_list.append(random.choice(chars))
        for j in range(char_nums[1]):
            password_list.append(random.choice(nums))
        for k in range(char_nums[2]):
            password_list.append(random.choice(symbols))
        random.shuffle(password_list)
        password = ''.join(password_list)

    return password




def main():
    password = ""
    while True:
        main_menu()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            pass_length = int(input("Please enter a length for your password: "))
            chars = get_password_chars()
            nums = get_password_nums()
            symbols = get_password_symbols()
            password = generate_password(pass_length, chars, nums, symbols)

            print("\n================================")
            print("Password generated successfully!")
            print("================================")
        elif choice == 2:
            added_pass = ''
            while True:
                sub_menu()
                sub_choice = int(input("Enter your choice: "))

                if sub_choice == 1:
                    while True:
                        user_pass = input("Provide Your password: ")
                        if user_pass:
                            added_pass += user_pass
                            print("\n================================")
                            print("Password added successfully!")
                            print("================================")
                            break
                        else:
                            print("The password field can't be empty!")
                            continue
                elif sub_choice == 2:
                    if added_pass:
                        print("\n================================")
                        print(f"Added password is: {added_pass}")
                        print("================================")
                    else:
                        print("\n================================")
                        print("No Password has been added Yet!")
                        print("================================")
                elif sub_choice == 3:
                    if added_pass:
                        root = tk.Tk()
                        root.withdraw()
                        root.wm_attributes("-topmost", True)

                        file_path = filedialog.asksaveasfilename(initialdir="/", title="Save Password File",
                                                                    filetypes=[("Text Files", "*.txt")])

                        if not file_path.endswith(".txt"):
                            file_path += ".txt"

                        if os.path.exists(file_path):
                            with open(file_path, "a") as f:
                                title = input("Enter a title for the password: ")
                                f.write(f"{title}: {added_pass}\n")
                                print("\n================================")
                                print("Password saved successfully!")
                                print("================================")
                        else:
                            with open(file_path, "w") as f:
                                title = input("Enter a title for the password: ")
                                f.write(f"{title}: {added_pass}\n")
                                print("\n================================")
                                print("Password saved successfully!")
                                print("================================")
                    else:
                        print("\n================================")
                        print("No Password has been added to save yet!")
                        print("================================")
                elif sub_choice == 4:
                    break
        elif choice == 3:
            if password:
                print("\n================================")
                print("Generated password: ", password)
                print("================================")
            else:
                print("\n================================")
                print("No password has been generated yet!")
                print("================================")

        elif choice == 4:
            if password:
                root = tk.Tk()
                root.withdraw()
                root.wm_attributes("-topmost", True)

                file_path = filedialog.asksaveasfilename(initialdir="/", title="Save Password File", filetypes=[("Text Files", "*.txt")])

                if not file_path.endswith(".txt"):
                    file_path += ".txt"

                if os.path.exists(file_path):
                    with open(file_path, "a") as f:
                        title = input("Enter a title for the password: ")
                        f.write(f"{title}: {password}\n")
                        print("\n================================")
                        print("Password saved successfully!")
                        print("================================")
                else:
                    with open(file_path, "w") as f:
                        title = input("Enter a title for the password: ")
                        f.write(f"{title}: {password}\n")
                        print("\n================================")
                        print("Password saved successfully!")
                        print("================================")
            else:
                print("\n================================")
                print("No Password has been generated to save yet!")
                print("================================")
        elif choice == 5:
            print("Thanks for using the app!\u2764\ufe0f")
            break

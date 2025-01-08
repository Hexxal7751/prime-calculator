import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import math
import time
import threading

stop_thread = threading.Event()  # Use threading.Event to signal stop.

def format_time(seconds):
    units = [('day', 24 * 60 * 60), ('hour', 60 * 60), ('minute', 60), ('second', 1)]
    parts = []
    for unit_name, unit_size in units:
        if seconds >= unit_size:
            unit_count, seconds = divmod(seconds, unit_size)
            parts.append(f"{unit_count} {unit_name}" + ("s" if unit_count != 1 else ""))
    return ', '.join(parts)

def open_prime_factoriser():
    def prime_factors():
        def calculate_factors():
            num_str = entry.get()
            if not num_str.isdigit():
                result_label.config(text="Error: Please enter a valid number.", fg="orange")
                return

            num = int(num_str)
            factors = []
            i = 2
            while i * i <= num:
                if num % i:
                    i += 1
                else:
                    num //= i
                    factors.append(i)
            if num > 1:
                factors.append(num)

            factors_str = ' x '.join(map(str, factors))

            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if not file_path:
                result_label.config(text="Error: File saving cancelled.", fg="red")
                return

            with open(file_path, 'w') as file:
                file.write(f"Prime factors of {num_str}:\n{factors_str}")
        
            result_label.config(text=f"Result saved to: {file_path}", fg="green")

        threading.Thread(target=calculate_factors).start()    

    root = tk.Tk()
    root.title("Prime Factoriser")
    root.geometry("350x190")
    root.resizable(False, False)

    root.iconbitmap('icon_PF.ico')

    input_label = tk.Label(root, text="Enter the number to Factorise:")
    input_label.pack(pady=5)

    entry = tk.Entry(root, width=40)
    entry.pack(pady=5)

    check_button = tk.Button(root, text="Factorise", command=prime_factors)
    check_button.pack(pady=5)

    progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
    progress.pack(pady=5)

    estimated_time_label = tk.Label(root, text="")
    estimated_time_label.pack(pady=5)

    result_label = tk.Label(root, text="")
    result_label.pack(pady=5)

    root.mainloop()
    

def open_divisible_numbers_finder():
    def find_divisible_numbers():
        def calculate_numbers():
            stop_thread = threading.Event()  # Use threading.Event to signal stop.
            nonlocal active_thread
            active_thread = True
            stop_thread.clear()  # Reset the stop signal

            num_str = entry.get()
            if not num_str.isdigit() or int(num_str) <= 0:
                safe_update(result_label, "config", text="Error: Enter a positive integer.", fg="orange")
                return

            num = int(num_str)
            divisible_by = []
            sqrt_num = math.isqrt(num)
            start_time = time.time()

            for i in range(1, sqrt_num + 1):
                if stop_thread.is_set():
                    safe_update(result_label, "config", text="Process stopped by the user.", fg="red")
                    break

                if num % i == 0:
                    divisible_by.append(i)
                    if i != num // i:
                        divisible_by.append(num // i)

                progress['value'] = (i / sqrt_num) * 100
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    remaining_time = elapsed_time / (i / sqrt_num) - elapsed_time
                    safe_update(estimated_time_label, "config", text=f"Estimated time: {format_time(remaining_time)}")

                root.update_idletasks()

            if not stop_thread.is_set():
                divisible_by.sort()
                result = f"{num} is {'a prime number' if len(divisible_by) == 2 else 'NOT a prime number. Divisible by: ' + str(divisible_by)}"
                file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
                if file_path:
                    with open(file_path, 'w') as file:
                        file.write(result)
                    safe_update(result_label, "config", text=f"Result saved to: {file_path}", fg="green")
                else:
                    safe_update(result_label, "config", text="Error: File saving canceled.", fg="red")

            progress['value'] = 0

        threading.Thread(target=calculate_numbers).start()

        def safe_update(widget, method, *args, **kwargs):
            if widget.winfo_exists():
                getattr(widget, method)(*args, **kwargs)


    def on_close():
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to close?"):
            stop_thread.set()
            root.destroy()

    root = tk.Tk()
    root.title("Divisible Numbers Finder")
    root.geometry("350x190")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", on_close)

    root.iconbitmap('icon_DNF.ico')

    active_thread = False

    input_label = tk.Label(root, text="Enter a number:")
    input_label.pack(pady=5)

    entry = tk.Entry(root, width=40)
    entry.pack(pady=5)

    check_button = tk.Button(root, text="Find Divisible Numbers", command=find_divisible_numbers)
    check_button.pack(pady=5)

    progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
    progress.pack(pady=5)

    estimated_time_label = tk.Label(root, text="")
    estimated_time_label.pack(pady=5)

    result_label = tk.Label(root, text="")
    result_label.pack(pady=5)

    root.mainloop()



def open_coprime_checker():
    def check_coprime():
        def primer():
            num1_str = num1_entry.get()
            num2_str = num2_entry.get()

            if not (num1_str.isdigit() and num2_str.isdigit()):
                result_label.config(text="Error: Please enter valid numbers.", fg="orange")
                return

            num1 = int(num1_str)
            num2 = int(num2_str)
            gcd = math.gcd(num1, num2)
            num3 = int(num1 / gcd)
            num4 = int(num2 / gcd)

            if gcd == 1:
                result = f"{num1} and {num2} are co-prime."
            else:
                result = f"{num1} and {num2} are NOT Co-primes. Their highest common factor (HCF) is {gcd}.\nIf simplified, {num3} and {num4} are Co-Primes"

            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if not file_path:
                result_label.config(text="Error: File saving cancelled.", fg="red")
                return

            with open(file_path, 'w') as file:
                file.write(result)
                file.write('\n')
            result_label.config(text=f"Result saved to: {file_path}", fg="green")

        threading.Thread(target=primer).start()    

    root = tk.Tk()
    root.title("Co-Prime Checker")
    root.geometry("350x190")
    root.resizable(False, False)

    root.iconbitmap('icon_CPC.ico')

    num1_label = tk.Label(root, text="Enter the first number:")
    num1_label.pack(pady=5)

    num1_entry = tk.Entry(root, width=40)
    num1_entry.pack(pady=5)

    num2_label = tk.Label(root, text="Enter the second number:")
    num2_label.pack(pady=5)

    num2_entry = tk.Entry(root, width=40)
    num2_entry.pack(pady=5)

    check_button = tk.Button(root, text="Check Co-Primality", command=check_coprime)
    check_button.pack(pady=5)

    result_label = tk.Label(root, text="")
    result_label.pack(pady=5)

    root.mainloop()



def open_twin_prime_generator():
    def generate_twin_primes():
        def generator():
            stop_thread = threading.Event()  # Use threading.Event to signal stop.
            nonlocal stop_flag
            stop_flag = False

            def is_prime(n):
                if n <= 1:
                    return False
                if n <= 3:
                    return True
                if n % 2 == 0 or n % 3 == 0:
                    return False
                i = 5
                while i * i <= n:
                    if n % i == 0 or n % (i + 2) == 0:
                        return False
                    i += 6
                return True

            def find_next_twin_prime(n):
                i = n + 1
                while not stop_flag:
                    if is_prime(i) and is_prime(i + 2):
                        return i, i + 2
                    i += 1
                return None, None

            root.after(0, lambda: start_button.config(state=tk.DISABLED))
            root.after(0, lambda: stop_button.config(state=tk.NORMAL))

            num_str = entry.get()
            if not num_str.isdigit() or int(num_str) <= 0:
                safe_update(result_label, "config", text="Error: Enter a positive integer.", fg="orange")
                root.after(0, lambda: start_button.config(state=tk.NORMAL))
                root.after(0, lambda: stop_button.config(state=tk.DISABLED))
                return

            n = int(num_str)
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if not file_path:
                safe_update(result_label, "config", text="Error: File saving canceled.", fg="red")
                root.after(0, lambda: start_button.config(state=tk.NORMAL))
                root.after(0, lambda: stop_button.config(state=tk.DISABLED))
                return

            with open(file_path, 'w') as file:
                while not stop_flag:
                    twin_prime_pair = find_next_twin_prime(n)
                    if twin_prime_pair[0] is None:
                        break
                    file.write(f"{twin_prime_pair[0]} - {twin_prime_pair[1]}\n")
                    safe_update(result_label, "config", text=f"Last twin prime pair: {twin_prime_pair[0]} - {twin_prime_pair[1]}")
                    n = twin_prime_pair[1]

            safe_update(result_label, "config", text="Twin prime generation stopped.")
            root.after(0, lambda: start_button.config(state=tk.NORMAL))
            root.after(0, lambda: stop_button.config(state=tk.DISABLED))

        threading.Thread(target=generator).start()

        def safe_update(widget, method, *args, **kwargs):
            if widget.winfo_exists():
                getattr(widget, method)(*args, **kwargs)


    def stop_generation():
        nonlocal stop_flag
        stop_flag = True

    root = tk.Tk()
    root.title("Twin Prime Generator")
    root.geometry("350x220")
    root.resizable(False, False)

    root.iconbitmap('icon_TPG.ico')

    stop_flag = False

    input_label = tk.Label(root, text="Start from number:")
    input_label.pack(pady=5)

    entry = tk.Entry(root, width=40)
    entry.pack(pady=5)

    start_button = tk.Button(root, text="Start Generation", command=generate_twin_primes)
    start_button.pack(pady=5)

    stop_button = tk.Button(root, text="Stop Generation", command=stop_generation, state=tk.DISABLED)
    stop_button.pack(pady=5)

    result_label = tk.Label(root, text="")
    result_label.pack(pady=5)

    root.mainloop()




def open_credits_window():
    if 'credits_window' in globals() and credits_window.winfo_exists():
        credits_window.lift()
        credits_window.focus_force()
    else:
        credits_window = tk.Toplevel(root)
        credits_window.title("Credits")
        credits_window.geometry("400x160")
        credits_window.resizable(False, False)
        credits_label = tk.Label(credits_window, text="Copyright © Hexxal.7751\n\nDiscord: Hexxal#7751\nYoutube: youtube.com/@Hexxal7751\n\nDeveloped solely by Hexxal.7751\n\nIcons & splashes credits goes to Microsoft Windows")
        credits_label.pack(pady=20)


# Create the main menu window
root = tk.Tk()
root.title("Main Menu")
root.geometry("250x250")
root.resizable(False, False)

root.iconbitmap('icon.ico')

# Functionality buttons
prime_factoriser_button = tk.Button(root, text="Prime Factoriser", fg="red", command=open_prime_factoriser)
prime_factoriser_button.pack(pady=15)

divisible_numbers_finder_button = tk.Button(root, text="Divisible Numbers Finder", fg="green", command=open_divisible_numbers_finder)
divisible_numbers_finder_button.pack(pady=15)

coprime_checker_button = tk.Button(root, text="Co-Prime Checker", fg="blue", command=open_coprime_checker)
coprime_checker_button.pack(pady=15)

twin_prime_generator_button = tk.Button(root, text="Twin Prime Generator", fg="orange", command=open_twin_prime_generator)
twin_prime_generator_button.pack(pady=15)

credits_button = tk.Button(root, text="Credits", command=open_credits_window, fg="cyan", bg="dark blue")
credits_button.place(relx=0.5, rely=0.9, anchor='n')

# Start the Tkinter event loop
root.mainloop()

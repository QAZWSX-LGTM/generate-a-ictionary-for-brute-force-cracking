import multiprocessing
from itertools import product
import os

number_English_mixture = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
                          , 'a', 'b', 'c', 'd', 'e', 'f','h', 'i', 'j', 'k', 'l', 'm'
                          , 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
                          , 'A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'L', 'M'
                          , 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

English = ['a', 'b', 'c', 'd', 'e', 'f', 'h', 'i', 'j', 'k', 'l', 'm'
           , 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
           , 'A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'L', 'M' , 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def worker(prefixes, chars, length, batch_size, proc_idx, progress_queue=None):
    for prefix in prefixes:
        buffer = []
        file_index = 1
        file_path = f'./dictionary_{proc_idx}_{file_index}.txt'
        with open(file_path, 'w', buffering=1024*1024*8) as file:
            for idx, item in enumerate(product(chars, repeat=length-len(prefix)), 1):
                buffer.append(prefix + ''.join(item) + '\n')
                if idx % batch_size == 0:
                    file.writelines(buffer)
                    buffer.clear()
                    file_index += 1
                    file_path = f'./dictionary_{proc_idx}_{file_index}.txt'
                    file = open(file_path, 'w', buffering=1024*1024*8)
                if progress_queue and idx % 100000 == 0:
                    progress_queue.put(100000)
            if buffer:
                file.writelines(buffer)
                if progress_queue:
                    progress_queue.put(idx % 100000)

def generate_a_ictionary_for_brute_force_cracking():
    """
    生成用于暴力破解的字典。Generate dictionary for brute force cracking.
    用户可选择生成仅数字、仅英文字母、仅大写英文字母、仅小写英文字母或数字与英文字母混合的组合，并输入生成几位的词典。
    User can choose to generate only numbers, only letters, only uppercase letters, only lowercase letters, or a mix, and input the length.
    """
    try:
        print("请选择要生成的字典类型：\n1. 仅数字\n2. 仅英文字母\n3. 仅大写英文字母\n4. 仅小写英文字母\n5. 数字和英文字母混合"
              "\nPlease select the type to generate:\n1. Numbers only\n2. Letters only\n3. Uppercase letters only\n4. Lowercase letters only\n5. Numbers and letters mixed")
        while True:
            choice = input("请输入选项(1/2/3/4/5): "
                          "\nPlease enter your choice (1/2/3/4/5): ")
            if choice in {'1', '2', '3', '4', '5'}:
                break
            print("无效选项，请重新输入。\nInvalid option, please enter 1/2/3/4/5.")

        length = int(input("请输入要生成几位的词典（正整数）: "
                              "\nPlease enter the length (positive integer): "))
        if length <= 0:
            print("请输入正整数。"
                  "\nPlease enter a positive integer.")
            return
    except Exception as e:
        print(f"输入异常：{e}\nInput error: {e}\n程序即将退出。\nProgram will exit.")
        return

    chars = number if choice == '1' else [c for c in English] if choice == '2' else [c for c in English if c.isupper()] if choice == '3' else [c for c in English if c.islower()] if choice == '4' else number_English_mixture if choice == '5' else None
    if not chars:
        print("无效选项。"
              "\nInvalid option.")
        return

    try:
        for cur_length in range(1, length + 1):
            total = len(chars) ** cur_length
            print(f"\n正在生成 {cur_length} 位的词典，共 {total} 条记录。"
                  f"\nGenerating dictionary of length {cur_length}, total {total} records.")

            cpu_count = multiprocessing.cpu_count()
            batch_size = 14344392
            prefix_len = 1 if cur_length <= 4 else 2
            all_prefixes = [''.join(p) for p in product(chars, repeat=prefix_len)]
            chunk_size = (len(all_prefixes) + cpu_count - 1) // cpu_count
            prefix_chunks = [all_prefixes[i*chunk_size:(i+1)*chunk_size] for i in range(cpu_count)]

            manager = multiprocessing.Manager()
            progress_queue = manager.Queue()
            pool = multiprocessing.Pool(cpu_count)
            for idx, chunk in enumerate(prefix_chunks):
                pool.apply_async(worker, (chunk, chars, cur_length, batch_size, f'{cur_length}_{idx+1}', progress_queue))
            pool.close()
            generated = 0
            while generated < total:
                try:
                    generated += progress_queue.get(timeout=600)
                except Exception as e:
                    print(f"进程通信异常：{e}\nProcess communication error: {e}")
                    break
                print(f"\r已生成 {generated}/{total} 条..."
                      f"\rGenerated {generated}/{total} records...", end='', flush=True)
            pool.join()
            print(f"\n{cur_length} 位词典生成完成。"
                  f"\nDictionary of length {cur_length} generated.")
        print("\n全部生成完成。"
              "\nAll dictionaries generated.")
    except Exception as e:
        print(f"生成过程中发生异常：{e}\nException during generation: {e}\n程序即将退出。\nProgram will exit.")
    return

# ---------------------------
# 程序说明 / Program Description
# ---------------------------
'''
本程序用于批量生成用于暴力破解的密码字典文件，支持以下功能：
1. 支持生成仅数字、仅英文字母、仅大写英文字母、仅小写英文字母、数字和英文字母混合的多种组合。
2. 用户可自定义生成密码的位数，自动分批写入多个txt文件，适合大规模字典生成。
3. 支持多进程加速，充分利用多核CPU资源。
4. 兼容Windows命令行和pyinstaller打包为exe后直接双击运行。
5. 具备输入校验和异常处理，防止误操作导致程序崩溃或死循环。

This program generates password dictionary files for brute-force cracking, with the following features:
1. Supports generating combinations of numbers only, letters only, uppercase only, lowercase only, or mixed numbers and letters.
2. User can specify the length of the password, and the program will automatically split output into multiple txt files for large-scale generation.
3. Utilizes multiprocessing to speed up generation and make full use of multi-core CPUs.
4. Compatible with Windows command line and can be packaged as an exe with pyinstaller for double-click execution.
5. Input validation and exception handling are included to prevent crashes or infinite loops due to invalid input.
'''
# ---------------------------

if __name__ == "__main__":
    import multiprocessing
    import sys
    print('''此程序用于批量生成用于暴力破解的密码字典文件，支持以下功能：
1. 支持生成仅数字、仅英文字母、仅大写英文字母、仅小写英文字母、数字和英文字母混合的多种组合。
2. 用户可自定义生成密码的位数，自动分批写入多个txt文件，适合大规模字典生成。
3. 支持多进程加速，充分利用多核CPU资源。
4. 兼容Windows命令行和pyinstaller打包为exe后直接双击运行。
5. 具备输入校验和异常处理，防止误操作导致程序崩溃或死循环。

This program generates password dictionary files for brute-force cracking, with the following features:
1. Supports generating combinations of numbers only, letters only, uppercase only, lowercase only, or mixed numbers and letters.
2. User can specify the length of the password, and the program will automatically split output into multiple txt files for large-scale generation.
3. Utilizes multiprocessing to speed up generation and make full use of multi-core CPUs.
4. Compatible with Windows command line and can be packaged as an exe with pyinstaller for double-click execution.
5. Input validation and exception handling are included to prevent crashes or infinite loops due to invalid input.
''')
    multiprocessing.freeze_support()
    generate_a_ictionary_for_brute_force_cracking()
    output_dir = os.path.abspath(os.path.dirname(__file__))
    print(f"字典生成成功。\nDictionary generated successfully。\n词典文件已保存在：{output_dir}\nDictionary files are saved in: {output_dir}")
    sys.exit(0)
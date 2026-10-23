from functions.get_file_content import get_file_content


def print_text_info(work_dir, file_path):
    result = get_file_content(work_dir, file_path)
    print(result[:2100])
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    print()


print_text_info("calculator", "lorem.txt")
print_text_info("calculator", "main.py")
print_text_info("calculator", "pkg/calculator.py")
print_text_info("calculator", "/bin/cat")
print_text_info("calculator", "pkg/does_not_exist.py")

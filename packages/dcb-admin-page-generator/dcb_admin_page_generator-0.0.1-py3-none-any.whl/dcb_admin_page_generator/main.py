# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def generate_page_list():
    # Use a breakpoint in the code line below to debug your script.
    yapi_url = input('请输入获取数据链接的YapiURL')
    print(f'Hi, ')  # Press Ctrl+F8 to toggle the breakpoint.


def generate_page_add():
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, ')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_name = input('输入文件名')
    page_type = input('请输入想要生成的Page Type')
    if page_type == 'list':
        generate_page_list()
    elif page_type == 'add':
        generate_page_add()


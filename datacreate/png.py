import os
# from pdf2image import convert_from_path
from PIL import Image

def convert_ps_to_png(filename, output_png_path):
    img = Image.open(filename)

    # output_png_name = filename.split('.')[0]
    filename = os.path.basename(filename)
    filename = filename.split(".")[0]
    output_png_name = filename.split("/")[-1] + ".png"

    print(output_png_name)
    img.save(output_png_name)

    try:
        # 将文件移动到 'pictures' 文件夹
        os.rename(output_png_name, f"{output_png_path}/{output_png_name}")
    except FileNotFoundError:
        pass  # 处理文件不存在的情况

if __name__ == "__main__":
    # 定義.ps檔案所在的目錄
    input_folder = "/home/xiangwei/chien/rnafold/datacreate/up45down9_pictures"

    # 定義輸出的.png檔案所在的目錄
    output_folder = "/home/xiangwei/chien/rnafold/datacreate/up45down9_pictures_png"


    # 遍歷指定目錄下的所有.ps檔案
    for filename in os.listdir(input_folder):
        if filename.endswith(".ps"):
            ps_file_path = os.path.join(input_folder, filename)

            # 執行轉換
            convert_ps_to_png(ps_file_path, output_folder)


    # 遍歷資料夾內的所有檔案
    # for filename in os.listdir(input_folder):
    #     if filename.endswith(".png"):  # 檢查是否是 .png 檔案
    #         file_path = os.path.join(input_folder, filename)  # 檔案的完整路徑
    #         os.remove(file_path)  # 刪除檔案


# -------------------test--------------------
# from PIL import Image

# ps_file_path = "/home/xiangwei/chien/rnafold/datacreate/own_S08_11_pictures/2_ss.ps"
# output_png_path = "2_ss.png"

# img = Image.open(ps_file_path)
# img.save(output_png_path)

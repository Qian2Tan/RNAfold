import os
from pdf2image import convert_from_path

def convert_ps_to_png(ps_file_path, output_png_path):
    # 將.ps檔案轉換為.pdf檔案
    pdf_file_path = os.path.splitext(ps_file_path)[0] + ".pdf"
    os.system(f"ps2pdf {ps_file_path} {pdf_file_path}")

    # 將.pdf檔案轉換為.png檔案
    images = convert_from_path(pdf_file_path)

    # 保存每一頁的.png檔案
    for i, image in enumerate(images):
        png_page_path = f"{output_png_path}_{i + 1}.png"
        image.save(png_page_path, "PNG")
        print(f"已轉換: {ps_file_path} -> {png_page_path}")

    # 刪除中間生成的.pdf檔案
    os.remove(pdf_file_path)

if __name__ == "__main__":
    # 定義.ps檔案所在的目錄
    input_folder = "/home/xiangwei/chien/rnafold/datacreate/up45down9_pictures"

    # 定義輸出的.png檔案所在的目錄
    output_folder = "/home/xiangwei/chien/rnafold/datacreate/up45down9_pictures_png"

    # 遍歷指定目錄下的所有.ps檔案
    for filename in os.listdir(input_folder):
        if filename.endswith(".ps"):
            ps_file_path = os.path.join(input_folder, filename)

            # 產生對應的.png檔案名稱
            output_png_path = os.path.join(output_folder, os.path.splitext(filename)[0])

            # 執行轉換
            convert_ps_to_png(ps_file_path, output_png_path)
import sys, tinify
from pathlib import Path

def hint(func):
    count = 1
    def call_func(source, total, width, height):
        nonlocal count
        print(f"({count}/{total})图片<{source}>正在压缩处理中，请稍后...")
        func(source, width, height)
        count += 1
        if count-1 == total:
            print("全部处理完成~")
    return call_func

@hint
def compress_(source, width, height):
    if not tinify.key:
        print("未指定密匙，请在https://tinify.cn/developers申请。")
    else:    
        optimize = tinify.from_file(source)

        if width and height:
            optimize = optimize.resize(method="fit", width=width, height=height)
        if width and not height:
            optimize = optimize.resize(method="scale", width=width)
        if not width and height:
            optimize = optimize.resize(method="scale", height=height)
        
        optimize.to_file("opt_" + source.split('\\')[-1])

def compress(*images):
    if not images:
        images = []
        print("开始优化当前文件夹下所有的jpg/png/webp图片...")
        p = Path('.')
        jpgs = list(p.glob("*.jpg")) + list(p.glob("*.jpeg"))
        pngs = list(p.glob("*.png"))
        webps = list(p.glob("*.webp"))
        for each in jpgs + pngs + webps:
            images.append(str(each))
        
    if images:
        size = input("请输入尺寸（宽度 高度）：")
        if size:
            width, height = size.split()
            width, height = int(width), int(height)
        else:
            width = 0
            height = 0
            
        total = len(images)
        for each in images:
            compress_(each, total, width, height)
    else:
        print("没有找到可以压缩的图片。")
    
if __name__ == "__main__":
    if sys.argv[1:]:
        images = sys.argv[1:]
    else:
        images = input("请输入需要压缩的图片名称（回车优化当前文件夹）：").split()

    compress(*images)

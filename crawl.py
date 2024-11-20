import argparse
import os

import requests
from bs4 import BeautifulSoup


class Args:
    url = "https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/"
    img_dir = "dataset/images"
    img_cnt = 1000


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=Args.url)
    parser.add_argument("--img-dir", default=Args.img_dir)
    parser.add_argument("--img-cnt", default=Args.img_cnt, type=int)
    return parser.parse_args()


def crawl(args: Args):
    remain_cnt = args.img_cnt - len(os.listdir(args.img_dir))
    # Crawl images
    for _ in range(remain_cnt):
        r = requests.get(args.url)
        soup = BeautifulSoup(r.text, "html.parser")
        img_url = soup.find_all(
            "img", src=lambda x: x and x.startswith("auth_img.php")
        )[0]["src"]
        img_data = requests.get(args.url + img_url).content
        img_path = os.path.join(args.img_dir, img_url.split("-")[1] + ".png")
        with open(img_path, "wb") as img_file:
            img_file.write(img_data)


def main():
    args = parse_args()

    # Create directory if not exist
    os.makedirs(args.img_dir, exist_ok=True)

    # Print current images
    print("images before crawl: {}".format(len(os.listdir(args.img_dir))))
    # Crawl images
    crawl(args)
    # Print current images
    print("images after crawl: {}".format(len(os.listdir(args.img_dir))))


if __name__ == "__main__":
    main()

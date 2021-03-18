# -*- encoding: utf -*-
"""
Create on 2020/12/14 17:21
@author: Xiao Yijia
"""


def dictionairy():
    # 声明字典
    key_value = {}

    # 初始化
    key_value[2] = 56
    key_value[1] = 2
    key_value[5] = 12
    key_value[4] = 24
    key_value[6] = 18
    key_value[3] = 323

    print("按值(value)排序:")
    sorted_kv = sorted(key_value.items(), key=lambda kv: (kv[1], kv[0]))
    print(type(sorted_kv))
    for k, v in sorted_kv:
        print("key:{}; value: {}".format(k, v))


def main():
    dictionairy()


if __name__ == "__main__":
    main()

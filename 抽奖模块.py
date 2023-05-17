import random
def lottery():
    # 定义奖品列表和对应的中奖概率
    prizes = ['一等奖', '二等奖', '三等奖', '谢谢参与']
    probability = [0.1, 0.2, 0.3, 0.4]
    # 生成随机数
    num = random.random()
    # 根据随机数和中奖概率来确定中奖结果
    for i in range(len(prizes)):
        if num < probability[i]:
            return prizes[i]
        else:
            num -= probability[i]
    return None
# 测试代码
result = lottery()
if result is not None:
    print('恭喜您获得了：', result)
else:
    print('很遗憾，您没有中奖。')
if __name__ == '__main__':
    lottery()

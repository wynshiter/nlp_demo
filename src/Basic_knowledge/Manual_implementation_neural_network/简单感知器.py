


'''
1. 处理单个输入
2. 处理2分类
'''

class Perceptron(object):
    '''
    初始化参数lr（用于调整训练步长，即 learning），iterations（迭代次数），权重w 与 bias 偏执
    '''
    def __init__(self,eta=0.01,iterations=10):
        self.lr = eta
        self.iterations = iterations
        self.w = 0.0
        self.bias = 0.0


#'''
#公式：
#Δw = lr * (y - y') * x
#Δbias = lr * (y - y')
#'''
    def fit(self,X,Y):
        for _ in range(self.iterations):
            for i in range(len(X)):
                x = X[i]
                y = Y[i]
                #首先获得真实值 y 与预测值 y' 的偏差，乘以一个较小的参数
                # 【lr 值过小导致训练时间过长，难以判断是否收敛】
                # 【lr 值过大则容易造成步长过大而无法收敛】
                update = self.lr * (y - self.predict(x))
                self.w += update * x
                self.bias += update

# y'(预测值) = w * x + bias
    def net_input(self,x):
        return self.w * x + self.bias

    def predict(self,x):
        return 1.0 if self.net_input(x) > 0.0 else 0.0



x = [1, 2, 3, 10, 20, -2, -10, -100, -5, -20]
y = [1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]

model = Perceptron(0.01,10)
model.fit(x,y)

test_x = [30, 40, -20, -60]
for i in range(len(test_x)):
    print('input {} => predict: {}'.format(test_x[i],model.predict(test_x[i])))

print(model.w)
print(model.bias)
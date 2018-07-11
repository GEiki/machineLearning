import csv
import random




def operatedata():
    o_user = 0
    with open(dataFile) as f:
        print('loading')
        reader = csv.reader(f)
        i = 0
        for row in reader:
            i += 1
            if i == 100000:
                break
            if row[0] == o_user:
                itemdict = userDict.get(o_user)
                itemdict[row[1]] = row[3]
            else:
                o_user = row[0]
                itemdict = {row[1]: row[3]}
                userDict[o_user] = itemdict


    set_score()  # 为用户行为赋值
    # 将数据分成测试集和训练集
    for user in userDict:
        num = len(userDict[user])/2
        i = 0
        for item in userDict[user]:
            item_dict = userDict[user]
            if i < num:
                if user not in trainData:
                    trainData[user] = {}
                tmp = trainData[user]
                tmp[item] = item_dict[item]
            else:
                if user not in testData:
                    testData[user] = {}
                tmp = testData[user]
                tmp[item] = item_dict[item]
            i += 1


    return


def set_score():
    for user in userDict:
        item_dict = userDict[user]
        for item in item_dict:
            if item_dict[item] == 'pv':
                item_dict[item] = 5
            elif item_dict[item] == 'fav':
                item_dict[item] = 10
            elif item_dict[item] == 'cart':
                item_dict[item] = 15
            elif item_dict[item] == 'buy':
                item_dict[item] = 20


def get_dtistance (user1: dict, user2: dict):
    distance = 0
    for key in list(user1.keys()):
        if key not in list(user1.keys()) or key not in list(user2.keys()):
            distance += 0
        else:
            distance = user1.get(key) * user2.get(key)

    return distance


def rand_cent(k):
    print('随机获取聚类中心')
    r_klist = []
    key_list = list(userDict.keys())
    for i in range(1, k):
        num = random.randint(0, len(key_list)-1)
        r_klist.append(key_list[num])
    print(r_klist)
    return r_klist


def is_centers_change(pre_dict, now_dict):
    pre_list = list(pre_dict.keys())
    now_list = list(now_dict.keys())
    # 没变 1
    # 变了 -1
    if len(pre_list) != len(now_list):
        return -1
    for i in range(1, len(pre_list)):
        if pre_list[i] != now_list[i]:
            return -1
    return 1


def find_cluster(clusters: list, user: dict):
    dis = 0
    count = ''
    for f_cluster in clusters:
        tmp_dis = get_dtistance(userDict[f_cluster], user)
        if tmp_dis >= dis:
            count = f_cluster
            dis = tmp_dis
    return count


def update_cluster_center(n_dict: dict):
    for u_cluster in list(n_dict.keys()):
        dis_list = {}
        for u_user in n_dict[u_cluster]:
            dis = 0
            for o_user in n_dict[u_cluster]:
                if u_user == o_user:
                    continue
                dis += get_dtistance(trainData[u_user], trainData[o_user])
            dis_list[u_user] = dis/len(n_dict)
        new_cluster = get_new_cluster(dis_list)
        n_dict[new_cluster] = n_dict.pop(u_cluster)
        n_dict[new_cluster].append(u_cluster)
    return n_dict


def get_new_cluster(user_dis_dict: dict):  # {'用户序号'：'与聚类中其他用户的平均距离'}
    max_dis = 0
    res_cluster = ''
    for user in user_dis_dict:
        if user_dis_dict[user] >= max_dis:
            max_dis = user_dis_dict[user]
            res_cluster = user

    return res_cluster


# 生成推荐列表
def recommend(user_name):
    for cluster in now_dict:
        cluster_dict = now_dict[cluster]
        for user in cluster_dict:# 找出用户所在簇
            if user == user_name:
                return get_recommend_item(cluster_dict,user_name)


def get_recommend_item(m_dict, r_user):
    res_list = []
    for user in m_dict:
        if user != r_user:  # 用户不是推荐用户
            for u_item in userDict[user]:
                if u_item not in trainData[r_user]:  # 商品为被推荐用户所没有
                    res_list.append(u_item)
                    break
    return res_list


# 计算准确率
def calc_accuracy(recommend_list, test_data):
    print("推荐列表："+str(recommend_list))
    count = 0
    for item in test_data[user_name]:
        if item in recommend_list:
            count += 1
    print('准确率：'+str((count/len(test_data[user_name])*100))+'%')


if __name__ == '__main__':
    userDict = {}  # {"用户序号"：{"商品序号"：'用户行为'...}...}
    dataFile = 'D:/Data/UserBehavior.csv'
    trainData = {}
    testData = {}
    operatedata()
    kList = rand_cent(15)  # ['聚类中心用户序号'...]
    pre_dict = {}  # {'聚类中心用户序号':['用户序号'...]...}
    now_dict = {}  # {'聚类中心用户序号':['用户序号'...]...}
    # 初始化
    print('初始化')
    for user_1 in trainData:
        if user_1 in kList:
            continue
        cluster = find_cluster(kList, trainData[user_1])
        if cluster not in now_dict:
            now_dict[cluster] = []
            now_dict[cluster].append(user_1)
        else:
            now_dict[cluster].append(user_1)
    print('聚类中心: '+str(now_dict.keys()))
    while is_centers_change(pre_dict, now_dict) == -1:
        if len(pre_dict) != 0:
            print('重新分配聚类中心')
            print('聚类中心：'+str(now_dict.keys()))
            for cluster in list(now_dict.keys()):
                for user_2 in now_dict[cluster]:
                    m_cluster = find_cluster(list(now_dict.keys()), userDict[user_2])
                    now_dict[cluster].remove(user_2)
                    now_dict[m_cluster].append(user_2)
        print('更新聚类中心')
        pre_dict = now_dict
        tmp = now_dict.copy()
        now_dict = update_cluster_center(tmp)

    # 计算准确率
    user_name = '1' # 推荐的用户名
    rom_list = recommend(user_name)
    calc_accuracy(rom_list, testData)



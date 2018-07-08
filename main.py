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
            if i == 10000000:
                break
            if row[0] == o_user:
                itemdict = userDict.get(o_user)
                itemdict[row[1]] = row[3]
            else:
                o_user = row[0]
                itemdict = {row[1]: row[3]}
                userDict[o_user] = itemdict
    return


def get_dtistance (user1: dict, user2: dict):
    distance = 0
    for key in list(user1.keys()):
        if key not in list(user1.keys()):
            distance += 0
        elif user2.get(key) == 'pv':
            distance += 1
        elif user2.get(key) == 'buy':
            distance += 50
        elif user2.get(key) == 'cart':
            distance += 25
        elif user2.get(key) == 'fav':
            distance += 15
    return distance


def rand_cent(k):
    print('随机获取聚类中心')
    r_klist = []
    key_list = list(userDict.keys())
    for i in range(1, k):
        num = random.randint(0, len(key_list))
        r_klist.append(key_list[num])
    print(r_klist)
    return r_klist


def is_centers_change(pre_dict, now_dict):
    pre_list = list(pre_dict.keys())
    now_list = list(now_dict.keys())
    print(pre_list)
    print(now_list)
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
        dis_list = {}  # {'用户序号'：'与聚类中心的距离'
        for u_user in n_dict[u_cluster]:
            dis_list[u_user] = get_dtistance(userDict[u_cluster], userDict[u_user])
        new_cluster = get_new_cluster(dis_list)
        n_dict[new_cluster] = n_dict.pop(u_cluster)
        n_dict[new_cluster].append(u_cluster)
    print(n_dict.keys())
    return n_dict


def get_new_cluster(user_dis_dict: dict):  # {'用户序号'：'与聚类中心的距离'}
    k = 0
    # 计算平均距离
    for n in user_dis_dict:
        k += user_dis_dict[n]
    mean = k/len(user_dis_dict)
    # 获取最接近平均距离的用户作为新的中心
    g_res = 999
    res_user = {}
    for g_user in user_dis_dict:
        if abs(user_dis_dict[g_user] - mean) < g_res:
            g_res = abs(user_dis_dict[g_user] - mean)
            res_user = g_user
    return res_user


if __name__ == '__main__':
    userDict = {}  # {"用户序号"：{"商品序号"：'用户行为'...}...}
    dataFile = 'D:/Data/UserBehavior.csv'
    operatedata()
    kList = rand_cent(8)  # ['聚类中心用户序号'...]
    pre_dict = {}  # {'聚类中心用户序号':['用户序号'...]...}
    now_dict = {}  # {'聚类中心用户序号':['用户序号'...]...}
    # 初始化
    print('初始化')
    for user_1 in userDict:
        if user_1 in kList:
            continue
        cluster = find_cluster(kList, userDict[user_1])
        if cluster not in now_dict:
            now_dict[cluster] = []
            now_dict[cluster].append(user_1)
        else:
            now_dict[cluster].append(user_1)
    print(now_dict.keys())
    while is_centers_change(pre_dict, now_dict) == -1:
        if len(pre_dict) != 0:
            print('重新分配聚类中心')
            print(now_dict.keys())
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




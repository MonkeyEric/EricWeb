# coding:utf-8
def findMedianSortedArrays(nums1, nums2):
    """
    :type nums1: List[int]
    :type nums2: List[int]
    :rtype: float
    """
    li = nums2 + nums1
    li = sorted(li)
    # 奇数
    if len(li) % 2 != 0:
        index = int((len(li) + 1) / 2 - 1)
        return float(li[index])
    # 偶数
    if len(li) % 2 == 0:
        index = int((len(li) / 2) - 1)
        return float((li[index] + li[index + 1]) / 2)


def main():
    grid = [[1, 2, 3], [4, 5, 6]]
    m = len(grid[0])  # 行
    n = len(grid)  # 列
    # 重新创建一个array
    # dp = [[0] * m] * n
    dp = [[0] * m for i in range(n)]
    dp[0][0] = grid[0][0]

    for i in range(1, n):
        # 初始化最左边的列
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    print(dp)
    # 初始化最上边的行
    for j in range(1, m):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    print(dp)
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j]

    print(dp[n - 1][m - 1])

